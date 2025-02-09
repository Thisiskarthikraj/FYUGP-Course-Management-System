from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    CustomLoginView, 
    StudentDashboardView, 
  
    HomePageView, 
    CustomLogoutView 
)
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  # Home page
    path('login/', CustomLoginView.as_view(), name='login'),  # Login page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('student-dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),  # Student dashboard
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Logout
    path('profile/', views.profile_view, name='profile'),  # View or register profile
    path('profile/edit/', views.profile_edit, name='profile_edit'), 
    path('courses/',views.student_view_courses, name='svc'),
    path('course-enrollment/', views.course_selection, name='course_enrollment'),
  

   
    # Edit profile (requires admin approval)

    # Admin dashboard and approval views
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('approve/', views.approve, name='approve_profiles'), 
    path('register-course/', views.register_course, name='register_course'),# Approval list
    path('approve/profiles/<int:profile_id>/approve/', views.admin_approve_profile, name='admin_approve_profile'),  # Approve individual profiles
    path('approve/profiles/<int:profile_id>/reject/', views.admin_reject_profile, name='admin_reject_profile'), 
    path('view-courses/', views.admin_view_courses, name='viewcourses'),
    path('mdc-selection/', views.available_mdc_courses, name='mdc_selection'), 
    path('enrolled-courses/',views.enrolled_courses_view, name='enrolled_courses'),
    path('promote-students/',views.promote_students_view, name='promote_students'),
    path('students/',views. student_list_view, name='student_list'),
    path('students/<int:student_id>/',views. student_detail_view, name='student_detail'),
    path('reports/department/', views.department_wise_report, name='department_wise_report'),
     path('reports/department/pdf/', views.export_department_report_pdf, name='export_department_report_pdf'),
# URL for MDC selection

# Reject individual profiles # Reject individual profiles
# Approve individual profiles
    # path('admin-dashboard/profiles/edit-approvals/', views.admin_approve_edit_requests, name='admin_approve_edit_requests'),  # Approve edit requests
]

if settings.DEBUG:  # Ensure this only runs in DEBUG mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


