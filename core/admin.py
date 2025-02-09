from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Department , CustomUser ,Programme ,Course ,Subject ,StudentProfile


admin.site.register(Department)
admin.site.register(CustomUser)
admin.site.register(Programme)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(StudentProfile)