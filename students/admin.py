from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "full_name", "course", "semester", "phone", "admission_date")
    list_filter = ("course", "semester", "gender")
    search_fields = ("roll_number", "user__first_name", "user__last_name", "user__email")
    autocomplete_fields = ("user",)
    list_select_related = ("user", "course")
