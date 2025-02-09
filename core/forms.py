# core/forms.py
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser ,StudentProfile
from django.core.exceptions import ValidationError


from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        if password1 and len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if password1 and not any(char.isdigit() for char in password1):
            raise ValidationError("Password must contain at least one digit.")
        if password1 and not any(char.isalpha() for char in password1):
            raise ValidationError("Password must contain at least one letter.")
        if password1 and not any(char in "!@#$%^&*()" for char in password1):
            raise ValidationError("Password must contain at least one special character.")

        return cleaned_data



# core/forms.py
from django import forms
from .models import StudentProfile, Subject

from django import forms
from .models import StudentProfile, Subject

class StudentProfileForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple', 'style': 'width: 100%;'}),  # Set up Select2
        required=True
    )

    class Meta:
        model = StudentProfile
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'dob', 'profile_picture', 'programme', 'department', 'board', 'subjects']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'dob': 'Date of Birth',
            'profile_picture': 'Upload Profile Picture',
            'programme': 'Programme of Study',
            'department': 'Department',
            'board': 'Educational Board at Plus Two',
            'subjects': 'Select Subjects',
        }


    # Customizing form fields
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    profile_picture = forms.ImageField(required=False)


# core/forms.py
from django import forms
from .models import Course, Subject

class CourseRegistrationForm(forms.ModelForm):
    excluded_subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple', 'style': 'width: 100%;'}),
        required=False  # Making it optional
    )

    class Meta:
        model = Course
        fields = ['name', 'course_type', 'programme', 'credit', 'semester', 'availability', 'excluded_subjects']
        labels = {
            'name': 'Course Name',
            'course_type': 'Course Type',
            'programme': 'Programme',
            'credit': 'Credit Value',
            'semester': 'Semester',
            'availability': 'Available Seats',
            'excluded_subjects': 'Excluded Subjects',
        }
