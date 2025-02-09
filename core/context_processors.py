# context_processors.py
from .models import StudentProfile

def student_profile_processor(request):
    student_profile = None
    if request.user.is_authenticated:
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            pass  # Handle if the student profile does not exist
    return {'student_profile': student_profile}
