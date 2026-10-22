from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("date", "student", "subject", "status", "marked_by")
    list_filter = ("status", "date", "subject__course", "subject")
    search_fields = ("student__roll_number", "student__user__first_name", "subject__code")
    date_hierarchy = "date"
    list_select_related = ("student__user", "subject", "marked_by")
