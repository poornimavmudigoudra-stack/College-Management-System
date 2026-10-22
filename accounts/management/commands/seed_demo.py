"""
Fill the database with demo data: 50 students, every course's full semester-wise syllabus
(courses/syllabus.py) and exactly 20 records in every other module.

    python manage.py seed_demo            # only runs on an empty database
    python manage.py seed_demo --reset    # wipe existing data (except superusers) and reseed

Every demo login uses the password "Demo@123".
"""
import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from attendance.models import Attendance
from courses.models import Course, Department, Subject
from courses.syllabus import add_syllabus
from examinations.models import Exam, Mark
from faculty.models import Faculty
from fees.models import Fee, Payment
from notices.models import Notice
from students.models import Student

DEMO_PASSWORD = "Demo@123"

# Department (name, code) -> its course (code, name, years, tuition) -> one semester-1 subject (code, name)
CATALOGUE = [
    (("Computer Science", "CS"), ("BCA", "Bachelor of Computer Applications", 3, 45000), ("BCA101", "Programming in C")),
    (("Information Science", "IS"), ("BSCIT", "B.Sc Information Technology", 3, 42000), ("BIT101", "Web Technologies")),
    (("Electronics", "EC"), ("BEEC", "B.E. Electronics & Communication", 4, 85000), ("EC101", "Basic Electronics")),
    (("Electrical Engineering", "EE"), ("BEEE", "B.E. Electrical Engineering", 4, 85000), ("EE101", "Circuit Theory")),
    (("Mechanical Engineering", "ME"), ("BEME", "B.E. Mechanical Engineering", 4, 85000), ("ME101", "Engineering Mechanics")),
    (("Civil Engineering", "CV"), ("BECV", "B.E. Civil Engineering", 4, 80000), ("CV101", "Surveying")),
    (("Commerce", "COM"), ("BCOM", "Bachelor of Commerce", 3, 30000), ("BCOM101", "Financial Accounting")),
    (("Management", "MGT"), ("BBA", "Bachelor of Business Administration", 3, 40000), ("BBA101", "Principles of Management")),
    (("Physics", "PHY"), ("BSCPHY", "B.Sc Physics", 3, 35000), ("PHY101", "Mechanics")),
    (("Chemistry", "CHE"), ("BSCCHE", "B.Sc Chemistry", 3, 35000), ("CHE101", "Inorganic Chemistry")),
    (("Mathematics", "MAT"), ("BSCMAT", "B.Sc Mathematics", 3, 32000), ("MAT101", "Calculus")),
    (("Biotechnology", "BT"), ("BSCBT", "B.Sc Biotechnology", 3, 50000), ("BT101", "Cell Biology")),
    (("English", "ENG"), ("BAENG", "B.A. English Literature", 3, 25000), ("ENG101", "British Poetry")),
    (("Economics", "ECO"), ("BAECO", "B.A. Economics", 3, 25000), ("ECO101", "Microeconomics")),
    (("Psychology", "PSY"), ("BAPSY", "B.A. Psychology", 3, 28000), ("PSY101", "Introduction to Psychology")),
    (("Journalism", "JMC"), ("BAJMC", "B.A. Journalism & Mass Communication", 3, 38000), ("JMC101", "News Reporting")),
    (("Hotel Management", "HM"), ("BHM", "Bachelor of Hotel Management", 4, 60000), ("HM101", "Food Production")),
    (("Fashion Design", "FD"), ("BDES", "Bachelor of Design (Fashion)", 4, 70000), ("FD101", "Fashion Illustration")),
    (("Law", "LAW"), ("BALLB", "B.A. LL.B (Integrated)", 5, 75000), ("LAW101", "Law of Contracts")),
    (("Pharmacy", "PHA"), ("BPHARM", "Bachelor of Pharmacy", 4, 90000), ("PHA101", "Pharmaceutics")),
]

# One faculty member per department (first, last, designation, qualification)
FACULTY = [
    ("Ramesh", "Kulkarni", "PROF", "Ph.D. Computer Science"),
    ("Priya", "Sharma", "ASSOC", "M.Tech Information Technology"),
    ("Arjun", "Nair", "ASST", "M.Tech VLSI Design"),
    ("Kavya", "Reddy", "ASST", "M.Tech Power Systems"),
    ("Suresh", "Patil", "PROF", "Ph.D. Mechanical Engineering"),
    ("Meena", "Iyer", "ASSOC", "M.Tech Structural Engineering"),
    ("Vikram", "Desai", "PROF", "Ph.D. Commerce"),
    ("Anjali", "Gowda", "ASST", "MBA (Finance)"),
    ("Harish", "Hegde", "ASSOC", "Ph.D. Physics"),
    ("Lakshmi", "Rao", "ASST", "M.Sc Chemistry"),
    ("Mahesh", "Bhat", "LECT", "M.Sc Mathematics"),
    ("Deepa", "Shetty", "ASST", "M.Sc Biotechnology"),
    ("Sunil", "Menon", "ASSOC", "M.A. English, Ph.D."),
    ("Rekha", "Pai", "ASST", "M.A. Economics"),
    ("Naveen", "Kamath", "LECT", "M.Sc Clinical Psychology"),
    ("Shalini", "Verma", "ASST", "M.A. Mass Communication"),
    ("Rajesh", "Pillai", "LECT", "M.Sc Hospitality Administration"),
    ("Nandini", "Joshi", "ASST", "M.Des Fashion"),
    ("Prakash", "Naik", "PROF", "LL.M, Ph.D."),
    ("Usha", "Agarwal", "ASSOC", "M.Pharm, Ph.D."),
]

STUDENT_COUNT = 50  # spread round-robin over the 20 courses
FIRST_NAMES = [
    ("Aarav", "M"), ("Ananya", "F"), ("Rohan", "M"), ("Diya", "F"), ("Karthik", "M"), ("Sneha", "F"),
    ("Siddharth", "M"), ("Pooja", "F"), ("Manoj", "M"), ("Divya", "F"), ("Nikhil", "M"), ("Aishwarya", "F"),
    ("Rahul", "M"), ("Bhavana", "F"), ("Varun", "M"), ("Kavitha", "F"), ("Pranav", "M"), ("Riya", "F"),
    ("Akash", "M"), ("Shruti", "F"), ("Darshan", "M"), ("Megha", "F"), ("Kiran", "M"), ("Swathi", "F"),
    ("Yash", "M"),
]
LAST_NAMES = ["Patil", "Shetty", "Naik", "Joshi", "Kumar", "Gowda", "Hegde", "Rao", "Kamath", "Bhat",
              "Pai", "Menon", "Pillai", "Verma", "Gupta", "Singh", "Mehta", "Jain", "Chavan", "Desai"]

CITIES = ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Belagavi", "Davanagere", "Ballari", "Tumakuru"]

NOTICES = [
    ("Semester examinations timetable released", "The timetable for the semester-end examinations is available on the exam schedule page.", "ALL", True),
    ("College closed for Kannada Rajyotsava", "The college will remain closed on 1st November. Classes resume the next day.", "ALL", False),
    ("Fee payment deadline", "Clear outstanding tuition fees at the accounts office before the due date to avoid a late fee.", "STUDENTS", True),
    ("Annual sports meet registrations open", "Register with your class representative for track, field and indoor events.", "STUDENTS", False),
    ("Faculty meeting on internal assessment", "All faculty are requested to attend a meeting in the seminar hall on Wednesday at 3:30 PM.", "FACULTY", False),
    ("Workshop: Building web apps with Django", "A two-day hands-on Django workshop is being conducted by the Department of Computer Science.", "ALL", False),
    ("Attendance shortage warning", "Students below 75% attendance will not be permitted to write the semester-end examinations.", "STUDENTS", True),
    ("Library timings extended", "The central library will remain open until 9 PM during the examination period.", "ALL", False),
    ("Blood donation camp", "The NSS unit is organising a blood donation camp in the main auditorium on Saturday.", "ALL", False),
    ("Scholarship applications", "Eligible students may apply for the state merit scholarship through the scholarship cell.", "STUDENTS", True),
    ("Submission of question papers", "Faculty must submit semester-end question papers to the examination cell by Friday.", "FACULTY", True),
    ("Campus placement drive", "Leading IT and finance companies will visit the campus next month. Register with the placement cell.", "STUDENTS", False),
    ("Guest lecture on Artificial Intelligence", "An industry expert will deliver a guest lecture on AI trends in the seminar hall.", "ALL", False),
    ("Revised bus timings", "College buses will depart 15 minutes earlier from next Monday due to road work.", "ALL", False),
    ("Faculty development programme", "A one-week FDP on outcome-based education begins on the 10th. Registration is mandatory.", "FACULTY", False),
    ("Cultural fest volunteers needed", "Students interested in volunteering for the annual cultural fest may contact the student council.", "STUDENTS", False),
    ("Anti-ragging awareness session", "An awareness session on anti-ragging regulations will be held for all first-year students.", "STUDENTS", True),
    ("Hostel mess menu updated", "The new weekly mess menu is displayed on the hostel notice board.", "ALL", False),
    ("Research paper submissions", "Faculty may submit papers for the college research journal before the end of the month.", "FACULTY", False),
    ("Independence Day celebrations", "All students and staff are requested to assemble on the main ground at 8 AM for the flag hoisting.", "ALL", False),
]


class Command(BaseCommand):
    help = "Populate the database with demo records in every module."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing data (superusers are kept) before seeding.")

    def handle(self, *args, **options):
        if options["reset"]:
            self._reset()
        elif Department.objects.exists() or Student.objects.exists():
            raise CommandError("Database already has data. Run with --reset to wipe it and reseed.")

        random.seed(2026)  # same data on every run
        self.today = timezone.localdate()
        self.admin = User.objects.filter(is_superuser=True).first()
        self.password = make_password(DEMO_PASSWORD)  # hash once; hashing per user is slow

        with transaction.atomic():
            subjects = self._catalogue()
            students = self._students(subjects)
            # Other modules stay at 20 records: one per course, for the first student of each course
            first_per_course = students[:len(subjects)]
            self._attendance(first_per_course, subjects)
            self._exams(first_per_course, subjects)
            self._fees(first_per_course)
            self._notices()

        counts = ", ".join(f"{m._meta.verbose_name_plural}: {m.objects.count()}" for m in (
            Department, Course, Subject, Faculty, Student, Attendance, Exam, Mark, Fee, Payment, Notice))
        self.stdout.write(self.style.SUCCESS(f"Seeded -> {counts}"))
        self.stdout.write(f"Demo logins use password {DEMO_PASSWORD!r}, e.g. faculty 'priya.sharma', student 'bca2026101'.")

    def _reset(self):
        for model in (Payment, Fee, Mark, Exam, Attendance, Notice, Student, Subject, Faculty, Course, Department):
            model.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write("Existing data removed.")

    def _catalogue(self):
        """20 departments, each with one faculty member and one course whose whole syllabus that faculty teaches.

        Returns each course's first semester-1 subject, which the attendance and exam records use.
        """
        subjects = []
        for i, ((dept_name, dept_code), (c_code, c_name, years, tuition), (s_code, s_name)) in enumerate(CATALOGUE):
            department = Department.objects.create(name=dept_name, code=dept_code, description=f"Department of {dept_name}.")
            first, last, designation, qualification = FACULTY[i]
            user = User.objects.create(
                username=f"{first}.{last}".lower(), first_name=first, last_name=last,
                email=f"{first}.{last}@college.edu".lower(), role=User.Role.FACULTY, password=self.password,
            )
            faculty = Faculty.objects.create(
                user=user, employee_id=f"EMP{i + 1:03d}", department=department, designation=designation,
                qualification=qualification, specialization=s_name, phone=f"98{random.randint(10000000, 99999999)}",
                date_of_joining=self.today - timedelta(days=random.randint(400, 5000)),
                address=f"{random.randint(1, 300)}, {random.choice(CITIES)}, Karnataka",
            )
            course = Course.objects.create(
                code=c_code, name=c_name, department=department, duration_years=years,
                description=f"{c_name} is a {years}-year programme offered by the Department of {dept_name}.",
            )
            course.tuition = tuition  # used when creating fees
            subjects.append(Subject.objects.create(code=s_code, name=s_name, course=course, semester=1,
                                                   credits=4, faculty=faculty))
            add_syllabus(course, faculty)
        return subjects

    def _students(self, subjects):
        year = self.today.year
        students = []
        for i in range(STUDENT_COUNT):
            first, gender = FIRST_NAMES[i % len(FIRST_NAMES)]
            last = LAST_NAMES[(i * 7) % len(LAST_NAMES)]
            course = subjects[i % len(subjects)].course
            roll = f"{course.code}{year}1{i // len(subjects) + 1:02d}"
            user = User.objects.create(
                username=roll.lower(), first_name=first, last_name=last,
                email=f"{roll}@student.college.edu".lower(), role=User.Role.STUDENT, password=self.password,
            )
            student = Student.objects.create(
                user=user, roll_number=roll, course=course, semester=1, gender=gender,
                date_of_birth=self.today - timedelta(days=365 * 18 + random.randint(0, 700)),
                phone=f"9{random.randint(100000000, 999999999)}",
                guardian_name=f"{random.choice(['Ravi', 'Mohan', 'Shankar', 'Ganesh', 'Prakash'])} {last}",
                guardian_phone=f"9{random.randint(100000000, 999999999)}",
                address=f"#{random.randint(1, 999)}, {random.randint(1, 20)}th Cross, {random.choice(CITIES)}, Karnataka",
                admission_date=self.today.replace(month=7, day=15),
            )
            student.tuition = course.tuition
            students.append(student)
        return students

    def _attendance(self, students, subjects):
        """One attendance record per student (yesterday's class), 16 present, 2 late, 2 absent."""
        day = self.today - timedelta(days=1)
        statuses = ["P"] * 16 + ["L"] * 2 + ["A"] * 2
        random.shuffle(statuses)
        Attendance.objects.bulk_create([
            Attendance(student=s, subject=subjects[i], date=day, status=statuses[i], marked_by=subjects[i].faculty.user)
            for i, s in enumerate(students)
        ])

    def _exams(self, students, subjects):
        """One mid-term per subject (held in the last month) and one mark per student."""
        for i, (student, subject) in enumerate(zip(students, subjects)):
            exam = Exam.objects.create(
                name="Mid Term Examination", exam_type=Exam.ExamType.MIDTERM, subject=subject,
                date=self.today - timedelta(days=3 + i), max_marks=100, pass_marks=35, created_by=subject.faculty.user,
            )
            score = 28 if i in (4, 13) else random.randint(45, 96)  # two students fail
            Mark.objects.create(exam=exam, student=student, marks_obtained=Decimal(score),
                                remarks="Needs improvement" if score < 35 else "")

    def _fees(self, students):
        """One tuition fee per student and one payment against each: 12 paid in full, 8 paid in part."""
        methods = [m for m, _ in Payment.Method.choices]
        for i, student in enumerate(students):
            fee = Fee.objects.create(
                student=student, fee_type=Fee.FeeType.TUITION, amount=student.tuition,
                due_date=self.today + timedelta(days=-20 if i % 2 else 15), description="Semester 1 tuition fee",
            )
            amount = fee.amount if i < 12 else (fee.amount * Decimal("0.5"))
            method = random.choice(methods)
            Payment.objects.create(
                fee=fee, amount=amount, method=method, received_by=self.admin,
                payment_date=self.today - timedelta(days=random.randint(1, 25)),
                transaction_id="" if method == "CASH" else f"TXN{random.randint(10**9, 10**10 - 1)}",
            )

    def _notices(self):
        for i, (title, content, audience, important) in enumerate(NOTICES):
            notice = Notice.objects.create(title=title, content=content, audience=audience,
                                           is_important=important, posted_by=self.admin)
            # spread notices over the last few weeks
            Notice.objects.filter(pk=notice.pk).update(created_at=timezone.now() - timedelta(days=i, hours=i))
