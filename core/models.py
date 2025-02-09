# core/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,default='student')
    
    objects = CustomUserManager()  # Attach CustomUserManager to the model

from django.db import models
from django.conf import settings  # Assuming CustomUser is the user model

class Department(models.Model):
    name = models.CharField(max_length=100)  # Department name

    def __str__(self): 
        return self.name


  # Program model representing the different FYUGP pathways
class Programme(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Subject(models.Model):
    name = models.CharField(max_length=100)  # Subject name, e.g., "Mathematics", "Physics", "Chemistry"

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,default='')  # First name
    last_name = models.CharField(max_length=30,default='')   # Last name
    phone_number = models.CharField(max_length=15,default='')  # Phone number
    address = models.TextField(default='')  # Address
    dob = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/')
    programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    board = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)  # Part III subjects studied in Plus Two
    semester = models.IntegerField(default=1)
    approved = models.BooleanField(default=False)
  

    def __str__(self):
        return f"{self.user.username} - {self.programme.name}"
class Course(models.Model):
    TYPE_CHOICES = [
        ('DSC', 'Discipline-Specific Core'),
        ('DSE', 'Discipline-Specific Elective'),
        ('AEC', 'Ability Enhancement Compulsory Course'),
        ('SEC', 'Skill Enhancement Course'),
        ('MDC', 'Multi-Disciplinary Course'),
    ]

    name = models.CharField(max_length=100)
    course_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    credit = models.IntegerField(default=2)
    semester = models.IntegerField(default=1)
    availability = models.IntegerField(default=40)  # Number of available seats
    excluded_subjects = models.ManyToManyField(Subject, blank=True)  # Subjects that exclude this course

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.IntegerField()  # Or ForeignKey to Semester model if applicable
   
    def __str__(self):
        return f'{self.student.user.username} enrolled in {self.course.name} for semester {self.semester}'


   