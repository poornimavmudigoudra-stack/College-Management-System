from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="list"),
    path("add/", views.course_add, name="add"),
    path("<int:pk>/", views.course_detail, name="detail"),
    path("<int:pk>/edit/", views.course_edit, name="edit"),
    path("departments/add/", views.department_add, name="department_add"),
    path("subjects/add/", views.subject_add, name="subject_add"),
    path("subjects/<int:pk>/edit/", views.subject_edit, name="subject_edit"),
]
