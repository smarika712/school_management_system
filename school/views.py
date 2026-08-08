import django.http
from django.shortcuts import render ,redirect ,get_object_or_404
import uuid
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from django.db.models import Q
from django.core.paginator import Paginator

from accounts.decorators import role_required
from .models import Student,Teacher,Course,Grade,StudentDocument
from .forms import StudentForm
from django.contrib import messages

from django.http import JsonResponse
from .utils import (
    compress_image,
    generate_thumbnail,
    validate_file_size,
    validate_image_type,
    get_file_size_display,
)

@login_required
def home_view(request):
    from cms.models import Banner,GalleryCategory,GalleryImage,Event,Announcement,Testimonials
    context={
        'banners':Banner.objects.filter(is_active=True)[:5],
        'featured_images':GalleryCategory.objects.filter(is_featured=True)[:8],
        'upcoming_events':Event.objects.filter(is_published=True)[:4],
        'announcements':Announcement.objects.filter(is_published=True)[:4],
        'testimonials': Testimonials.objects.filter(is_active=True)[:6],
        'total_students':Student.objects.filter(status='active').count(),
        'total_teachers': Teacher.objects.filter(is_active=True).count(),
        'total_courses':Course.objects.filter(is_active=True).count(),
        
    }
    return render(request, 'school/home.html', context)

@login_required
@role_required('admin', 'teacher')
def student_list_view(request):
    students=Student.objects.all()
    search=request.GET.get('search','').strip()
    status=request.GET.get('status','')
    
    
    if search:
        students=students.filter(
            Q(first_name__icontains=search)|
            Q(last_name__icontains=search)|
            Q(student_id__icontains=search)|
            Q(email__icontains=search)
        )
        
    if status:
        students=students.filter(status=status)
        
    students=students.order_by('-enrollment_date')
    paginator=Paginator(students,15)
    page=request.GET.get('page')
    students=paginator.get_page(page)
    
    return render(request,'school/students/students_list.html',{
        'students':students,'search':search,
        'status_choices':Student.STATUS_CHOICES,'selected_status':status
    })


@login_required
def student_detail_view(request,pk):
    student=get_object_or_404(Student,pk=pk)
    return render(request,'school/students/student_detail.html',{
        'student':student,
        'graded':student.grades.select_related('course').all(),
        'documents':student.documents.all(),
        'courses':student.courses.all(),
    })
    
@login_required
@role_required('admin')
def student_create_view(request):
    if request.method=="POST":
        form=StudentForm(request.POST,request.FILES)
        if form.is_valid():
            student=form.save(commit=False)
            if 'profile_photo' in request.FILES:
                photo=request.FILES['profile_photo']
                compressed=compress_image(photo)
                student.profile_photo.save(photo.name,compressed,save=False)
                student.save()
                messages.success(request,f'Student {student.full_name} added.')
                return redirect('student_detail',pk=student.pk)
            else:
                form=StudentForm()
                return render(request,'school/students/student_form.html',{
                    'form':form,
                    'title':'Add New Srudent'})

@login_required
@role_required('admin')
def student_update_view(request,pk):
    student=get_object_or_404(Student,pk=pk)
    if request.method=="POST":
        form=StudentForm(request.POST,request.FILES,instance=student)
        if form.is_valid():
            student=form.save(commit=False)
            if 'profile_photo' in request.FILES:
                photo=request.FILES['profile_photo']
                compressed=compress_image(photo)
                student.profile_photo.save(photo.name,compressed,save=False)
            student.save()
            messages.success(request,f'Student {student.full_name} updated.')
            return redirect('student_detail',pk=student.pk)
    else:
        form=StudentForm(instance=student)

    return render(request,'school/students/student_form.html',{
        'form':form,'student':student,
        'title':f'Edit Student {student.full_name}'
    })

def student_delete_view(request,pk):
    student=get_object_or_404(Student,pk=pk)
    if request.method=="POST":
        name=student.full_name
        student.delete()
        messages.redirect(request,'school/students/student_confirm_delete.html',{'student':student})


def student_document_upload_view(request,pk):
    student=get_object_or_404(Student,pk=pk)
    if request.method=="POST":
        title=request.POST.get('title','')
        doc_type=request.POST.get('document_type','')
        file=request.FILES.get('file')
        if file:
            StudentDocument.objects.create(
                student=student,title=title,document_type=doc_type,file=file)
        else:
            messages.error(request,'Please select a file.')
        return redirect('student_detail',pk=pk)
    
@login_required
def teacher_list_view(request):
    teachers=Teacher.objects.filter(is_active=True)
    search=request.GET.get('search','')
    if search:
        teachers=teachers.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search)
            
        )
        
    paginator=Paginator(teachers,15)
    teacher=paginator.get_page(request.GET.get('page'))
    return render(request,'school/teachers/teacher_list.html',{'teachers':teachers })

@login_required
def teacher_detail_view(request,pk):
    teacher=get_object_or_404(Teacher,pk=pk)
    return render(request,'school/teachers/teacher_detail.html',{
        'teacher':teacher,'courses':teacher.courses.all()
        })
    
@login_required
def course_list_view(request):
    courses=Course.objects.filter(is_active=True).select_related('teacher')
    search = request.GET.get('search', '')
    if search:
        courses=courses.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search)
        )  
    paginator=Paginator(courses,15)
    courses=paginator.get_page(request.GET.get('page'))
    return render(request,'school/courses/course_list.html',{'courses':courses})   

@login_required    
def course_detail_view(request,pk):
    course=get_object_or_404(Course,pk=pk)
    return render(request,'school/courses/course_detail.html',{
        'course':course,'grades':course.grades.select_related('student').all()
        })
    

@login_required
@require_POST
def upload_image(request):
    """Handle AJAX image upload with compressing and thumbnail generation"""
    if 'file' not in request.FILES:
        return JsonResponse({'error':'No file provided'} ,status=400)
    uploaded_file=request.FILES['file']
    valid ,error_msg=validate_file_size(uploaded_file,max_size_mb=10)
        
    if not valid:
            
        return JsonResponse({ 'error':error_msg},status=400)
    valid ,error_msg=validate_image_type(uploaded_file)
                
    if not valid:
                    
        return JsonResponse({ 'error':error_msg},status=400)
                
        
    try:
        compressed=compress_image(uploaded_file)
        thumbnail=generate_thumbnail(uploaded_file)
        unique_id = uuid.uuid4().hex
        filename = f'uploads/{unique_id}.jpg'
        
        # filename=f'uploads/{uuid.uuid4().hex}.jpg'
        thumb_filename = f'uploads/thumb_{unique_id}.jpg'
        filepath = default_storage.save(filename, compressed)
        thumb_path=default_storage.save(thumb_filename, thumbnail)
        return JsonResponse({
            'success':True,
                    
            'url':default_storage.url(filepath),
            'thumbnail_url':default_storage.url(thumb_path),
            'original_size':get_file_size_display(uploaded_file.size),
            'compressed_size':get_file_size_display(compressed.size),
                })
    except Exception as e:
        return JsonResponse({'error':f'upload Failed:{str(e)},status=500'})


@login_required
@require_POST

def upload_document(request):
    """Handle document file upload"""
    if 'file' not in request.FILES:
        return JsonResponse({
            'error':'No file provided'
        } ,status=400)
    uploaded_file= request.FILES['file']
    valid ,error_msg=validate_file_size(uploaded_file,max_size_mb=10)
    if not valid:
        return JsonResponse({ 'error':error_msg},status=400)
    try:
        ext=uploaded_file.name.split('.')
        filename=f'document/{uuid.uuid4().hex}.{ext}'    
        filepath=default_storage.save(filename,uploaded_file)
        
        return JsonResponse({
            'success':True,
            'url':default_storage.url(filepath),
            'filename':uploaded_file.name,
            'size':get_file_size_display(uploaded_file.size),
                        }
                    )
    except Exception as e:
        return JsonResponse({'error':f'upload Failed:{str(e)},status=500'})