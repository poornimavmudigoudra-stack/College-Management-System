from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import home

admin.site.site_header = "College Management System"
admin.site.site_title = "CMS Admin"
admin.site.index_title = "Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("students/", include("students.urls")),
    path("faculty/", include("faculty.urls")),
    path("courses/", include("courses.urls")),
    path("attendance/", include("attendance.urls")),
    path("examinations/", include("examinations.urls")),
    path("fees/", include("fees.urls")),
    path("notices/", include("notices.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "accounts.views.error_404"
handler500 = "accounts.views.error_500"
