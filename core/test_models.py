# myapp/tests.py

from django.test import TestCase
from .models import CustomUser, StudentProfile, Programme, Department, Subject, Course, Enrollment

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('password123'))

class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Computer Science')

    def test_department_str(self):
        self.assertEqual(str(self.department), 'Computer Science')

class ProgrammeModelTest(TestCase):
    def setUp(self):
        self.programme = Programme.objects.create(name='MCA')

    def test_programme_str(self):
        self.assertEqual(str(self.programme), 'MCA')

class SubjectModelTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name='Mathematics')

    def test_subject_str(self):
        self.assertEqual(str(self.subject), 'Mathematics')

class StudentProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='teststudent',
            email='teststudent@example.com',
            password='password123'
        )
        self.programme = Programme.objects.create(name='MCA')
        self.department = Department.objects.create(name='Computer Science')
        self.student_profile = StudentProfile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            address='123 Main St',
            dob='2000-01-01',
            programme=self.programme,
            department=self.department,
            board='CBSE',
            semester=1,
            approved=True
        )

    def test_student_profile_str(self):
        self.assertEqual(str(self.student_profile), 'teststudent - MCA')

class CourseModelTest(TestCase):
    def setUp(self):
        self.programme = Programme.objects.create(name='MCA')
        self.subject1 = Subject.objects.create(name='Mathematics')
        self.course = Course.objects.create(
            name='Mathematics 101',
            course_type='DSC',
            programme=self.programme,
            credit=3,
            semester=1,
            availability=40
        )
        self.course.excluded_subjects.add(self.subject1)

    def test_course_str(self):
        self.assertEqual(str(self.course), 'Mathematics 101')
class EnrollmentTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='teststudent', email='teststudent@example.com', password='password')
        self.programme = Programme.objects.create(name='MCA')
        self.department = Department.objects.create(name='Computer Science')
        self.student_profile = StudentProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Student',
            phone_number='1234567890',
            address='123 Main St',
            dob='2000-01-01',
            profile_picture=None,
            programme=self.programme,
            department=self.department,
            board='CBSE',
            semester=1,
            approved=True
        )
        self.course = Course.objects.create(
            name='Mathematics 101',
            course_type='DSC',
            programme=self.programme,
            credit=3,
            semester=1,
            availability=30
        )
        self.enrollment = Enrollment.objects.create(
            student=self.student_profile,
            course=self.course,
            semester=1
        )

    def test_enrollment_str(self):
        self.assertEqual(str(self.enrollment), 'teststudent enrolled in Mathematics 101 for semester 1')
