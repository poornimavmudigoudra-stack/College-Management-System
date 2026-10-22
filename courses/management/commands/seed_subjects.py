"""
Add the full semester-wise syllabus (courses/syllabus.py) to the existing demo courses.

    python manage.py seed_subjects

Safe to run repeatedly: subjects that already exist are skipped, nothing is deleted.
New subjects are assigned to a faculty member of the course's department, if it has one.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from courses.models import Course, Subject
from courses.syllabus import SYLLABUS, add_syllabus


class Command(BaseCommand):
    help = "Add every semester's subjects to the demo courses."

    def handle(self, *args, **options):
        added = 0
        with transaction.atomic():
            for course in Course.objects.filter(code__in=SYLLABUS).select_related("department"):
                faculty = course.department.faculty.order_by("pk").first()
                count = add_syllabus(course, faculty)
                added += count
                self.stdout.write(f"{course.code}: {count} subject(s) added")
        self.stdout.write(self.style.SUCCESS(f"Added {added} subjects; {Subject.objects.count()} subjects in total."))
