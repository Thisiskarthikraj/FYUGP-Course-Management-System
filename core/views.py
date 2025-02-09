from django.contrib.auth.views import LoginView ,LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView , ListView ,DeleteView , UpdateView
from .forms import CustomUserCreationForm , CourseRegistrationForm , StudentProfileForm  # Import your custom form
from django.contrib.auth import login 
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Programme ,StudentProfile , Enrollment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Department, Enrollment
from django.db.models import Count

# views here
class HomePageView(TemplateView):
    template_name = 'home.html'
#signup

# views.py
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        # Check for missing fields
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, "signup.html")
        
        # Check for password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")
        
        # Check for existing username or email
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "signup.html")
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "signup.html")
        
        # Create the user if all validations pass
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully!")
        return redirect("login")  # Replace with your actual login route

    return render(request, "signup.html")

# Redirect to a home page or dashboard, update as needed
# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Path to your login template

    def form_valid(self, form):
        # Call the parent method to complete the login process
        response = super().form_valid(form)
        user = self.request.user
        # Redirect based on user type
        if user.is_superuser:  # Check if the user is a superuser
            return redirect('admin_dashboard')
        elif user.user_type == 'student':  # Student
            return redirect('student_dashboard')
        return response

    def form_invalid(self, form):
        # Add error message for invalid login attempts
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)  # Call the parent method
#logout
class CustomLogoutView(DjangoLogoutView):
    next_page = reverse_lazy('home')  


# Admin Dashboard Views
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('profile')
    # Get all profiles pending approval (not yet approved)
    pending_profiles = StudentProfile.objects.filter(approved=False)
    # Render the admin dashboard with pending profiles
    return render(request, 'admin_dashboard.html', {'pending_profiles': pending_profiles})
# Approve students profile
@login_required
def approve(request):
    if request.user.is_superuser:
        # Fetch all profiles, filtering by approval status if necessary
        pending_profiles = StudentProfile.objects.filter(approved=False)  # Only get unapproved profiles
        return render(request, 'admin_approve_profiles.html', {'pending_profiles': pending_profiles})
    else:
        # Optionally, handle access for non-superusers
        return redirect('home')  # Redirect non-superusers to the home page
@login_required
def admin_approve_profile(request, profile_id):
    if request.user.is_superuser:  # Ensure only superusers can access
        profile = get_object_or_404(StudentProfile, id=profile_id)
        profile.approved = True  # Mark the profile as approved
        profile.save()
        messages.success(request, f'Profile of {profile.user.username} has been approved.')  # Add a success message
        return redirect('approve_profiles')  # Redirect to the profile approvals page
    return redirect('home')  # Optional: redirect to home if not superuser
@login_required
def admin_reject_profile(request, profile_id):
    if request.user.is_superuser:  # Check if the user is a superuser
        profile = get_object_or_404(StudentProfile, id=profile_id)
        profile.approved = False  # Set approval status to false
        profile.save()
        messages.warning(request, f'Profile of {profile.user.username} has been rejected.')  # Add a warning message
        return redirect('approve_profiles')  # Redirect back to the approval page
    return redirect('home')  # Optional: redirect to home if not superuser
#course registration
@login_required
def register_course(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admins to home page

    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            # Save the new course; this will also save ManyToMany fields
            course = form.save()
            messages.success(request, 'Course has been registered successfully.')
            return redirect('register_course')  # Redirect to the same page or another page
    else:
        form = CourseRegistrationForm()

    return render(request, 'creg.html', {'form': form})
#view all courses registred
@login_required
def admin_view_courses(request):
    # Fetch the filter values from the GET request (if any)
    course_type = request.GET.get('course_type', None)
    programme = request.GET.get('programme', None)
    credit = request.GET.get('credit', None)
    availability = request.GET.get('availability', None)
    semester = request.GET.get('semester',None)
    # Fetch all courses initially
    courses = Course.objects.all()
    # Apply filters based on the GET parameters
    if course_type:
        courses = courses.filter(course_type=course_type)
    if programme:
        courses = courses.filter(programme__name=programme)
    if credit:
        courses = courses.filter(credit=credit)
    if availability:
        courses = courses.filter(availability__gt=0)  # Only show available courses
    if semester:
        courses =  courses.filter(semester=semester) 
    # Fetch all programmes for the dropdown in the template
    programmes = Programme.objects.all()

    return render(request, 'avc.html', {
        'courses': courses,
        'programmes': programmes,  # For populating the programme dropdown
        'selected_course_type': course_type,
        'selected_programme': programme,
        'selected_credit': credit,
        'selected_availability': availability,
        'selected_semester':semester,
    })
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import StudentProfile, Programme  # Ensure you have a Programme model


@user_passes_test(lambda u: u.is_staff)  # Ensure only admins can access this view
def promote_students_view(request):
    selected_programme_id = request.GET.get('programme')

    if request.method == 'POST':
        student_ids = request.POST.getlist('students')
        for student_id in student_ids:
            try:
                student_profile = StudentProfile.objects.get(id=student_id)
                student_profile.semester += 1  # Promote to next semester
                student_profile.save()
                messages.success(request, f'Student {student_profile.user.username} promoted to semester {student_profile.semester}.')
            except StudentProfile.DoesNotExist:
                messages.error(request, f'Student with ID {student_id} does not exist.')

        return redirect('promote_students')  # Redirect after promotion

    # Fetch all students and filter by programme if a programme is selected
    students = StudentProfile.objects.all()
    if selected_programme_id:
        students = students.filter(programme__id=selected_programme_id)

    # Calculate total credits for each student
    student_data = []
    for student in students:
        enrolled_courses = Enrollment.objects.filter(student=student)  # Adjust this according to your enrollment model
        total_credits = sum(course.course.credit for course in enrolled_courses)
        student_data.append({
            'student': student,
            'total_credits': total_credits,
        })

    programmes = Programme.objects.all()  # Fetch all programmes for the dropdown
    return render(request, 'promote_students.html', {
        'student_data': student_data,  # Pass calculated student data including total credits
        'programmes': programmes,
        'selected_programme_id': selected_programme_id,  # Pass the selected programme id
    })


@user_passes_test(lambda u: u.is_staff)  # Ensure only admins can access this view
def student_list_view(request):
    # Get all students and their profiles
    students = StudentProfile.objects.select_related('user')
    
    # Get programs for filtering
    programmes = Programme.objects.all()

    # Get filter from the GET request
    selected_programme_id = request.GET.get('programme', '')

    # Apply filtering if provided
    if selected_programme_id:
        students = students.filter(programme_id=selected_programme_id)

    return render(request, 'student_list.html', {
        'students': students,
        'programmes': programmes,
        'selected_programme_id': selected_programme_id,
    })

@login_required
def student_detail_view(request, student_id):
    # Retrieve the student profile based on the provided student ID
    student_profile = get_object_or_404(StudentProfile, id=student_id)

    return render(request, 'student_detail.html', {
        'student_profile': student_profile,
    })   
@login_required
def enrolled_courses_view(request):
    # Retrieve all enrollments
    enrollments = Enrollment.objects.select_related('student', 'course')

    # Get filters from the GET request
    programme = request.GET.get('programme', '')

    # Apply programme filter if provided
    if programme:
        enrollments = enrollments.filter(student__programme__name__icontains=programme)

    # Get all unique programmes for the dropdown
    programmes = StudentProfile.objects.values_list('programme__name', flat=True).distinct()

    # Check if no enrollments were found and set a message
    if not enrollments:
        messages.info(request, "No enrollments found matching the provided filters.")

    return render(request, 'enrolled_courses.html', {
        'enrollments': enrollments,
        'selected_programme': programme,
        'programmes': programmes,  # Pass all programme names to the template
    })



#student dashboard
class StudentDashboardView(TemplateView):
    template_name = 'student_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Attempt to get the student's profile
        try:
            student_profile = StudentProfile.objects.get(user=self.request.user)
        except StudentProfile.DoesNotExist:
            messages.error(self.request, "Student profile not found.")
            return context  # Return empty context if profile is not found

        # Get the current semester from the student's profile
        current_semester = student_profile.semester
        
        # Fetch enrolled courses based on the student's profile and current semester
        # Ensure to access the `Enrollment` table correctly
        courses = Enrollment.objects.filter(student=student_profile, semester=current_semester)

        # Add courses and current semester to context
        context['courses'] = courses
        context['current_semester'] = current_semester

        return context
#student profile view and edit
@login_required
def profile_view(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES)
            if form.is_valid():
                student_profile = form.save(commit=False)
                student_profile.user = request.user
                student_profile.save()  # Save the profile first
                form.save_m2m()  # Save the ManyToMany relationship
                return redirect('profile')
        else:
            form = StudentProfileForm()
        return render(request, 'profile_register.html', {'form': form})

    return render(request, 'profile_detail.html', {'student_profile': student_profile})

@login_required
def profile_edit(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('profile')  # Redirect if no profile exists

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            # Save the profile but do not approve yet
            edit_request = form.save(commit=False)
            edit_request.approved = False  # Set approved to False, awaiting admin approval
            edit_request.save()  # Save the profile

            # Save the ManyToMany relationships for subjects
            form.save_m2m()  # Save the selected subjects

            messages.success(request, 'Your edit request has been submitted for approval.')  # Optional success message
            return redirect('profile')  # Redirect after the request is made
    else:
        form = StudentProfileForm(instance=student_profile)

    return render(request, 'profile_edit.html', {'form': form})
#student registred views with filtering
@login_required
def student_view_courses(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        if not student_profile.approved:
            messages.warning(request, "Your profile needs admin approval to explore these features.")
            return redirect('profile')
    except StudentProfile.DoesNotExist:
        return redirect('profile')  # Ensure the student has a profile
    enrolled_courses = Enrollment.objects.filter(student=student_profile).select_related('course')
    course_type = request.GET.get('course_type', None)
    credit = request.GET.get('credit', None)
    semester = request.GET.get('semester', None)
    # If a course is found, we create a base queryset of all enrolled courses
    courses = Course.objects.filter(id__in=enrolled_courses.values_list('course_id', flat=True))
    # Apply filters based on the GET parameters
    if course_type:
        courses = courses.filter(course_type=course_type)

    if credit:
        courses = courses.filter(credit=credit)

    if semester:
        courses = courses.filter(semester=semester)

    return render(request, 'svc.html', {
        'courses': courses,
        'selected_course_type': course_type,
        'selected_credit': credit,
        'selected_semester': semester,
    })

@login_required
def available_mdc_courses(request):
    try:
        # Get the student's profile and ensure it's approved
        student_profile = StudentProfile.objects.get(user=request.user)
        if not student_profile.approved:
            messages.warning(request, "Your profile needs admin approval to explore these features.")
            return redirect('profile')
    except StudentProfile.DoesNotExist:
        # Redirect to profile page if no profile exists
        return redirect('profile')

    # Get the student's subjects from their profile
    student_subjects = student_profile.subjects.all()

    # Get the current semester from the student's profile
    current_semester = student_profile.semester

    # Check if the student is already enrolled in any MDC courses for the current semester
    if Enrollment.objects.filter(student=student_profile, course__course_type='MDC', semester=current_semester).exists():
        messages.info(request, "You are already enrolled in MDC courses for this semester.")
        return redirect('svc')  # Redirect to the SVC page if already enrolled

    # Retrieve MDC courses for the student's current semester that do not exclude any of the student's subjects
    mdc_courses = Course.objects.filter(
        course_type='MDC',
        semester=current_semester  # Only select courses for the student's current semester
    ).exclude(
        excluded_subjects__in=student_subjects
    ).distinct()  # To avoid duplicates if multiple subjects are checked

    # Check if the student's programme is BCA (Hons) and filter accordingly
    if student_profile.programme.name == "BCA(Hons)":
        mdc_courses = mdc_courses.filter(programme=student_profile.programme)

    # Handle the POST request for enrolling in selected MDC courses
    if request.method == "POST":
        selected_courses = request.POST.getlist('selected_courses')  # Get selected course IDs
        for course_id in selected_courses:
            course = Course.objects.get(id=course_id)
            # Check if the course is already enrolled to avoid duplicates
            if not Enrollment.objects.filter(student=student_profile, course=course).exists():
                # Create a new enrollment record
                Enrollment.objects.create(student=student_profile, course=course, semester=current_semester)
                course.availability -= 1
                course.save()

        messages.success(request, "MDC courses enrolled successfully!")
        return redirect('student_dashboard')  # Redirect to the student dashboard or wherever appropriate
    
    # Render the list of available MDC courses to the template
    return render(request, 'mdc_selection.html', {'courses': mdc_courses})

@login_required
def course_selection(request):
    # Get the student's profile
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        if not student_profile.approved:
            messages.warning(request, "Your profile needs admin approval to explore these features.")
            return redirect('profile')
    except StudentProfile.DoesNotExist:
        return redirect('profile')

    # Get the student's current semester from their profile
    current_semester = student_profile.semester

    # Check how many courses the student is already enrolled in for the current semester
    enrolled_courses = Enrollment.objects.filter(student=student_profile, semester=current_semester)
    if enrolled_courses.count() >= 6:
        # Redirect to the enrolled courses page if already enrolled in 6 courses
        messages.info(request, "You have completed enrollment for 6 courses.")
        return redirect('svc')  # Redirect to the enrolled courses page

    # Get filters from the GET request
    course_type = request.GET.get('course_type', '')
    credit = request.GET.get('credit', '')

    # Retrieve available courses for the current semester (excluding enrolled courses)
    courses = Course.objects.filter(
        programme=student_profile.programme,
        semester=current_semester
    ).exclude(course_type='MDC').filter(availability__gt=0)

    # Exclude already enrolled courses
    enrolled_course_ids = enrolled_courses.values_list('course__id', flat=True)
    courses = courses.exclude(id__in=enrolled_course_ids)

    # Apply filters if selected
    if course_type:
        courses = courses.filter(course_type=course_type)
    if credit:
        courses = courses.filter(credit=credit)

    if request.method == "POST":
        selected_courses = request.POST.getlist('selected_courses')

        # Enroll the student in the selected courses, but ensure they don't exceed 6 total courses
        for course_id in selected_courses:
            if enrolled_courses.count() >= 6:
                messages.warning(request, "You cannot register for more than 6 courses.")
                break

            course = Course.objects.get(id=course_id)
            # Check if the course is already enrolled to avoid duplicates
            if not Enrollment.objects.filter(student=student_profile, course=course).exists():
                # Create a new enrollment record
                Enrollment.objects.create(student=student_profile, course=course, semester=current_semester)
                
                # Decrease course availability by one
                course.availability -= 1
                course.save()

        # After enrollment, check if the student has completed registration for 6 courses
        if Enrollment.objects.filter(student=student_profile, semester=current_semester).count() >= 6:
            messages.success(request, "You have enrolled in 6 courses.")
            return redirect('svc')  # Redirect to the enrolled courses page

        messages.success(request, "Courses enrolled successfully!")
        return redirect('course_enrollment')

    return render(request, 'course_selection.html', {
        'courses': courses,
        'current_semester': current_semester,
        'selected_course_type': course_type,
        'selected_credit': credit,
    })




def department_wise_report(request):
    selected_department = request.GET.get('department', '')

    # Fetch all departments for the dropdown
    departments = Department.objects.all()

    # Filter enrollments by selected department (if any)
    report_data = Department.objects.values(
        'name'
    ).annotate(
        total_students=Count('studentprofile__user'),
        enrolled_courses=Count('studentprofile__enrollment__course', distinct=True)
    )

    if selected_department:
        report_data = report_data.filter(name=selected_department)

    student_courses = Enrollment.objects.select_related(
        'student__department', 'course'
    ).values(
        'student__first_name', 'student__last_name',
        'student__department__name', 'course__name', 'course__semester'
    )

    if selected_department:
        student_courses = student_courses.filter(
            student__department__name=selected_department
        )

    context = {
        'departments': departments,
        'selected_department': selected_department,
        'report_data': report_data,
        'student_courses': student_courses,
    }

    return render(request, 'department_wise_report.html', context)


def export_department_report_pdf(request):
    selected_department = request.GET.get('department', '')

    # Fetch filtered report data and student enrollments
    report_data = Department.objects.values(
        'name'
    ).annotate(
        total_students=Count('studentprofile__user'),
        enrolled_courses=Count('studentprofile__enrollment__course', distinct=True)
    )

    if selected_department:
        report_data = report_data.filter(name=selected_department)

    student_courses = Enrollment.objects.select_related(
        'student__department', 'course'
    ).values(
        'student__first_name', 'student__last_name',
        'student__department__name', 'course__name', 'course__semester'
    )

    if selected_department:
        student_courses = student_courses.filter(
            student__department__name=selected_department
        )

    # Render the HTML template with context data
    template = get_template('department_wise_report_pdf.html')
    html = template.render({
        'report_data': report_data,
        'student_courses': student_courses,
        'selected_department': selected_department,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="department_wise_report.pdf"'

    # Generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f'Error generating PDF: <pre>{html}</pre>')
    return response
