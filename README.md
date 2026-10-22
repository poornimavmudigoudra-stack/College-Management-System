# College Management System

A role-based college management web app built with **Django 5** and **Bootstrap 5**.

## Features

| Module        | Admin                               | Faculty                                | Student                     |
|---------------|-------------------------------------|----------------------------------------|-----------------------------|
| Dashboard     | Stats, fee summary, chart           | Subjects, today's attendance, exams    | Attendance %, results, dues |
| Students      | Add / edit / delete / search        | View list & profiles                   | Own profile                 |
| Faculty       | Add / edit / delete / search        | -                                      | -                           |
| Courses       | Departments, courses, subjects      | View                                   | -                           |
| Attendance    | Mark any subject, reports           | Mark own subjects, reports             | Own records & report        |
| Examinations  | Schedule, marks entry, results      | Same, for own subjects                 | Own results & grades        |
| Fees          | Assign (single/bulk), payments      | -                                      | Own fees & receipts         |
| Notices       | Post / delete any                   | Post / delete own                      | Read                        |

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env          # (cp on macOS/Linux) then set SECRET_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and log in with the superuser (it automatically gets the **Admin** role).

### Demo data

```bash
python manage.py seed_demo            # fills an empty database
python manage.py seed_demo --reset    # wipes everything except superusers, then reseeds
python manage.py seed_subjects        # adds the full syllabus to an already-seeded database
```

Creates 50 students, the full semester-wise syllabus of every course (5 subjects per semester,
690 subjects, listed in `courses/syllabus.py`) and exactly 20 records in every other module: departments,
courses, faculty, attendance, exams, marks, fees, payments and notices. All demo logins use the password `Demo@123`
(e.g. faculty `priya.sharma`, student `bca2026101`).

### Suggested first steps
1. **Courses → Add Department**, then **Add Course**, then **Add Subject**.
2. **Faculty → Add Faculty**, then assign faculty to subjects (edit a subject).
3. **Students → Add Student** (creates the login and the student record).
4. Faculty log in and **Mark Attendance** / **Schedule Exam** / **Enter Marks**.
5. **Fees → Assign Fee** to a student or a whole course, then **Record Payment**.

Students can also self-register at `/accounts/register/`; an admin then creates their
student record (or links it in the Django admin at `/admin/`).

## Project structure

```
config/         settings, root urls, wsgi/asgi
accounts/       custom User (roles), login/register/profile, dashboards, role decorators
students/       Student model + CRUD
faculty/        Faculty model + CRUD
courses/        Department, Course, Subject
attendance/     Attendance marking, records, reports
examinations/   Exam, Mark (grades), marks entry, results
fees/           Fee, Payment (auto receipt numbers), receipts
notices/        Notice board with audience targeting
templates/      base layout, includes/, one folder per app
static/         css/, js/, images/
media/          uploaded student & faculty photos
```

## Tests

```bash
python manage.py test
```

See [tests/README.md](tests/README.md) for what each app's tests cover.

## Configuration

`.env` keys: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`.
`ATTENDANCE_THRESHOLD` (default 75%) in `config/settings.py` controls shortage highlighting.
