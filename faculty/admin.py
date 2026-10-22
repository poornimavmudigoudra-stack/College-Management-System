from django.contrib import admin

from .models import Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "full_name", "department", "designation", "phone", "date_of_joining")
    list_filter = ("department", "designation")
    search_fields = ("employee_id", "user__first_name", "user__last_name", "specialization")
    autocomplete_fields = ("user",)
    list_select_related = ("user", "department")
