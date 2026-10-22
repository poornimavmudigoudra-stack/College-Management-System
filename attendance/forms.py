from django import forms

from accounts.forms import BootstrapFormMixin, DateInput

from .models import Attendance


class AttendanceFilterForm(BootstrapFormMixin, forms.Form):
    """GET filter used on the attendance list and to pick a class for marking."""

    subject = forms.ModelChoiceField(queryset=None, required=False, empty_label="All subjects")
    date = forms.DateField(required=False, widget=DateInput())
    status = forms.ChoiceField(choices=[("", "Any status")] + Attendance.Status.choices, required=False)

    def __init__(self, *args, subjects=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = subjects
