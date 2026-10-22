from django import forms

from accounts.forms import BootstrapFormMixin, DateInput

from .models import Faculty


class FacultyForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Faculty
        fields = [
            "employee_id", "department", "designation", "qualification", "specialization",
            "phone", "date_of_joining", "photo", "address",
        ]
        widgets = {
            "date_of_joining": DateInput(),
            "address": forms.Textarea(attrs={"rows": 2}),
        }
