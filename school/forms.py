from django import forms
from django.core.exceptions import ValidationError
from .models import Student,Teacher,Course,Grade
from datetime import date
# from .models import StudentForm
class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=[
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'address',
            'student_id',
            'profile_photo',
            'status',
            'parent_name',
            'parent_phone',
        ]
        
        widgets={
        
            'date_of_birth':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'address':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'student_id':forms.TextInput(attrs={'class':'form-control'}),
            'parent_name':forms.TextInput(attrs={'class':'form-control'}),
            'parent_phone':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-select'}),
            'status':forms.Select(attrs={'class':'form-select'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        
        
        }
        
    def clean_date_of_birth(self):
        dob=self.cleaned_data.get('date_of_birth')
        if dob and dob>date.today():
            raise ValidationError('Date of birth cannot be in the future.')
        return dob
    
# ram@gmail.com
    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs=Student.objects.filter(email=email)
        if self.instance:
            qs=qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('A student with this email already exists.')
        return email
        

class Teacherform(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=[
            'first_name','last_name','email','phone','date_of_birth',
            'department','teacher_id','qualification',
            'hire_date','profile_photo','bio',
        ]
        widgets={
            'date_of_birth':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'hire_date':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'bio':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'first_name':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'last_name':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'email':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'phone':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'teacher_id':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'qualifications':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'department':forms.Select(attrs={'class':'form-select'}),
            'profile_photo':forms.ClearableFileInput(attrs={'class':'form-control','accept':'image/*'}),
            }
        
class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=['name','code','description','teacher','credits','max_students','thumbnail']
        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'code':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'teacher':forms.Select(attrs={'class':'form-select'}),
            'credits':forms.NumberInput(attrs={'class':'form-control'}),
            'max_students':forms.NumberInput(attrs={'class':'form-control'}),
            'thumbnail':forms.ClearableFileInput(attrs={'class':'form-control',
            'accept':'image/*'}),
            
        }
        
class GradeForm(forms.ModelForm):
    class Meta:
        model=Grade
        fields=['student','course','grade','marks','remarks']
        widgets={
            'student':forms.Select(attrs={'class':'form-select'}),
            'course':forms.Select(attrs={'class':'form-select'}),
            'grade':forms.TextInput(attrs={'class':'form-control'}),
            'marks':forms.NumberInput(attrs={'class':'form-control'}),
            'remarks':forms.Textarea(attrs={'rows':3,'class':'form-control'}),
        }
            