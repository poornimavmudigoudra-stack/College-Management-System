from django import forms

from accounts.forms import BootstrapFormMixin, DateInput

from .models import Student


class StudentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "roll_number", "course", "semester", "gender", "date_of_birth", "phone",
            "guardian_name", "guardian_phone", "admission_date", "photo", "address",
        ]
        widgets = {
            "date_of_birth": DateInput(),
            "admission_date": DateInput(),
            "address": forms.Textarea(attrs={"rows": 2}),
        }

    def clean(self):
        cleaned = super().clean()
        course, semester = cleaned.get("course"), cleaned.get("semester")
        if course and semester and semester > course.total_semesters:
            self.add_error("semester", f"{course.code} only has {course.total_semesters} semesters.")
        return cleaned
