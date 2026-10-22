from django.contrib import admin

from .models import Exam, Mark


class MarkInline(admin.TabularInline):
    model = Mark
    extra = 0
    autocomplete_fields = ("student",)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name", "exam_type", "subject", "date", "max_marks", "pass_marks")
    list_filter = ("exam_type", "subject__course", "date")
    search_fields = ("name", "subject__code", "subject__name")
    date_hierarchy = "date"
    inlines = [MarkInline]


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ("exam", "student", "marks_obtained", "grade")
    list_filter = ("exam__subject",)
    search_fields = ("student__roll_number", "exam__name")
    list_select_related = ("exam", "student__user")
