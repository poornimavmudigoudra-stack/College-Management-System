from django.urls import path

from . import views

app_name = "examinations"

urlpatterns = [
    path("", views.exam_list, name="list"),
    path("add/", views.exam_add, name="add"),
    path("<int:pk>/marks/", views.marks_entry, name="marks_entry"),
    path("results/", views.results, name="results"),
]
