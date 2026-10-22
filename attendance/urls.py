from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_list, name="list"),
    path("mark/", views.attendance_mark, name="mark"),
    path("report/", views.attendance_report, name="report"),
]
