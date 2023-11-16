from django.contrib import admin 
from .models import Faculty 


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'name', 'abbrev', 'is_deleted', 'created_at', 'created_by')
    search_fields = ['faculty_id', 'name', 'abbrev']
    list_filter = ['is_deleted']

