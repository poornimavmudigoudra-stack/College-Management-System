from django.contrib import admin

from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "audience", "is_important", "is_active", "posted_by", "created_at")
    list_filter = ("audience", "is_important", "is_active")
    list_editable = ("is_important", "is_active")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
