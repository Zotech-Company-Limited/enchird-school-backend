from django.contrib import admin
from .models import Course



# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_title', 'course_code', 'credits', 'course_status', 'class_schedule', 'location', 'office_hours', 'term', 'created_at', 'created_by')
    search_fields = ['course_id', 'course_title', 'course_code']
    list_filter = ['course_status']

