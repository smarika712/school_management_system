from django.contrib import admin
from .models import Student,Teacher,Course,Grade,StudentDocument
# Register your models here.

class StudentDocumentInline(admin.TabularInline):
    model= StudentDocument
    extra=0
    readonly_fields=('uploaded_at',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id','full_name_display','email','status','enrollment_date','has_photo')
    list_filter = ('status','gender','enrollment_date')
    search_fields = ('first_name','last_name','student_id','email')
    ordering = ('-enrollment_date',)
    list_editable=('status',)
    readonly_fields=('enrollment_date','created_at','updated_at')
    inlines=[StudentDocumentInline]
    fieldsets=(
        ('Personal Information',{
            'fields':('first_name','last_name','email','phone','date_of_birth','gender','profile_photo')}),
        ('Academic Info',{'fields':('student_id','enrollment_date','status')}),
        ('Contact & Family',{'fields':(
            'address','parent_name','parent_phone')}),
        ('Timespamps',{'classes':(
            'collapse',),'fields':('created_at','updated_at')}),
    )
    
    def full_name_display(self,obj):
        return obj.full_name
    full_name_display.short_description='Name'
    
    def has_photo(self,obj):
        return bool(obj.profile_photo)
    has_photo.boolean=True
    has_photo.short_description='Photo'
    
    
    
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display=('teacher_id','full_name_display','department','qualification','is_active')
    list_filter=('department','is_active','hire_date')
    search_fields=('first_name','last_name','teacher_id')
    list_editable=('is_active',)
    readonly_fields=('hire_date','created_at','updated_at')
    fieldsets=(('Personal Info',{'fields':('user','first_name','last_name','email',
            'phone','date_of_birth','profile_photo')}),
        ('Professional Info',{'fields':('teacher_id','department','qualification','hire_date','bio')}),
        ('Status',{'fields':('is_active',)}),
        )
        
    def full_name_display(self,obj):
        return obj.full_name
    full_name_display.short_description='Name'
        
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=('code','name','teacher','credits','max_students','is_active')
    list_filter=('is_active','teacher','credits')
    search_fields=('code','name')
    prepopulated_fields={'slug':('name',)}
    filter_horizontal=('students',)
    readonly_fields=('created_at','uploaded_at')
    
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display=('student','course','grade','marks','date_assigned')
    list_filter=('grade','course')
    search_fields=('student__first_name','student__last_name')
    readonly_fields=('date_assigned',)
        
    
@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display=('student','title','document_type','uploaded_at')
    list_filter=('document_type',)
    
    search_fields=('student__first_name','student__last_name','title')
    readonly_fields=('uploaded_at',)