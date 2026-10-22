# Tests

Unit tests live next to the code they cover, in each app's `tests.py`:

| App            | What is tested                                                        |
|----------------|-----------------------------------------------------------------------|
| `accounts`     | Roles, registration, login-required redirects, role-based dashboards  |
| `students`     | Adding students (user + profile), access rules, cascade delete        |
| `faculty`      | Adding faculty, admin-only access                                     |
| `courses`      | Semester validation, admin-only course creation                       |
| `attendance`   | Marking, re-marking (no duplicates), "late counts as present"         |
| `examinations` | Grade calculation, marks range validation, student results            |
| `fees`         | Fee status/balance, receipt numbering, overpayment, bulk assignment   |
| `notices`      | Audience-based visibility, posting                                    |

## Running

```bash
python manage.py test                 # everything
python manage.py test fees            # one app
python manage.py test fees.tests.FeeTests.test_status_and_balance   # one test
```

Add project-wide integration tests to this folder if needed (give it an `__init__.py`
and name files `test_*.py` so Django's test runner discovers them).
