from django import forms

from accounts.forms import BootstrapFormMixin

from .models import Course, Department, Subject


class DepartmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "code", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class CourseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "code", "department", "duration_years", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class SubjectForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "code", "course", "semester", "credits", "faculty"]

    def clean(self):
        cleaned = super().clean()
        course, semester = cleaned.get("course"), cleaned.get("semester")
        if course and semester and semester > course.total_semesters:
            self.add_error("semester", f"{course.code} only has {course.total_semesters} semesters.")
        return cleaned
