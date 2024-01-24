from django.contrib import admin
from .models import DirectMessage, ChatGroup, GroupMessage




# Register your models here.

@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('is_read',)

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'code')
    search_fields = ('name', 'course__name', 'code')

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'timestamp', 'group')
    search_fields = ('sender__username', 'content', 'group__name')
    list_filter = ('group',)