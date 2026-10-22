from django.contrib import admin

from .models import Course, Department, Subject


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("name", "code")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department", "duration_years")
    list_filter = ("department",)
    search_fields = ("name", "code")
    inlines = [SubjectInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "course", "semester", "credits", "faculty")
    list_filter = ("course", "semester")
    search_fields = ("name", "code")
