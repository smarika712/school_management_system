from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Student(models.Model):
    GENDER_CHOICES= [('M','Male'),('F','female'), ('O','OTHER')]
    STATUS_CHOICES=[
        ('active','Active'),('inactive','Inactive'),
        ('graduated','Graduated'),('transferred','Transferred'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True , blank= True)
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    email = models.EmailField(unique= True)
    phone= models.CharField( max_length=20, blank= True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address= models.TextField(blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    enrollment_date = models.DateField(auto_now_add= True)
    profile_photo= models.ImageField(upload_to='students/photos/%y/%m', blank=True, null = True)
    status= models.CharField(max_length=15, choices=STATUS_CHOICES, default="active")
    parent_name = models.CharField( max_length=200, blank= True)
    parent_phone= models.CharField(max_length=20, blank= True)
    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True)
    
    class Meta:
        ordering = ['-enrollment_date']
        
    def __str__(self):
        return f'{self.first_name}{self.last_name}({self.student_id})'
   
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})
    
    @property
    def full_name(self):
        return f'{self.first_name}{self.last_name}'
    
class Teacher(models.Model):
    DEPARTMENT_CHOICES =[
        ('science','Science'), ('mathematics','Mathematics'),
        ('english','English'), ('social','Social studeis'),
        ('arts','Arts'),('physical','Physical'),
        ('tech','Technology'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True , blank= True)
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    email = models.EmailField(unique= True)
    phone= models.CharField( max_length=20, blank= True)
    date_of_birth = models.DateField()
    department= models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    address= models.TextField(blank=True)
    teacher_id = models.CharField(max_length=20, unique=True)
    qualification = models.CharField(max_length=200)  
    profile_photo= models.ImageField(upload_to='teachers/photos/%y/%m', blank=True, null = True)
    hire_date= models.DateField()
    bio= models.TextField(blank= True)
    is_active= models.BooleanField(default= True)
    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['first_name']
        
    def __str__(self):
        return f'{self.first_name}{self.last_name}({self.get_department_display()})'
   
    def get_absolute_url(self):
        return reverse('teacher_detail', kwargs={'pk': self.pk})
    
    @property
    def full_name(self):
        return f'{self.first_name} - {self.last_name}'
    
class Course(models.Model):
    name= models.CharField(max_length=200)    
    slug= models.SlugField(max_length=200, unique=True, blank=True)
    code= models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True,related_name="courses")
    description = models.TextField(blank=True)
    students=models.ManyToManyField(Student)
    credits= models.PositiveIntegerField(default=3)
    max_students= models.PositiveIntegerField(default=30)
    thumbnail = models.ImageField(upload_to='courses/thumbnail/%Y/%m', blank=True, null=True)
    is_active= models.BooleanField(default= True)
    created_at= models.DateTimeField(auto_now_add=True)
    uploaded_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['code']
        
    def __str__(self):
        return f'{self.code}{self.code}'
   
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
        super().save(*args, **kwargs)
    
class Grade(models.Model):
    GRADE_CHOICES=[
        ('A+', 'A+'), ('A','A'),('A-','A-'),
        ('B+', 'B+'), ('B','B'),('B-','B-'),
        ('C+', 'C+'), ('C','C'),('C-','C-'),
        ('D+', 'D+'), ('D','D'),('D-','D-'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
    related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
    related_name='grades')
    grade= models.CharField(max_length=2, choices=GRADE_CHOICES)
    marks= models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    remarks= models.TextField( blank=True)   
    date_assigned= models.DateTimeField(auto_now_add= True)
    
    class Meta:
        unique_together = ('student','course')
        ordering=['-date_assigned']
        
    def __str__(self):
        return f'{self.student.full_name} - {self.course.name}:{self.grade}'
        
        
class StudentDocument(models.Model):
    DOCUMENT_TYPES=[
        ('birth_cert','Birth Certificate'),('transfer','Transfer Certificate'),
        ('marksheet','Marksheet'),('id_proof','ID proof'),('other','Other'),
        
    ]
    
    student= models.ForeignKey(Student, on_delete= models.CASCADE,
    related_name='documents')
    document_type=models.CharField(max_length=100)
    title= models.CharField(max_length=20, choices= DOCUMENT_TYPES, default='other')
    file= models.FileField(upload_to='students/documents/%Y/%m')
    uploaded_at= models.DateField(auto_now_add=True)
    
    class Meta:
        ordering= ['-uploaded_at']
        
        def __str__(self):
            return f'{self.student.full_name} - {self.title}'