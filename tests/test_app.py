import os
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_DIR))


class TypewritingAppTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        os.environ["DB_BACKEND"] = "sqlite"
        os.environ["SQLITE_PATH"] = os.path.join(self.tmp_dir.name, "test.db")

        from config import Config
        Config.DB_BACKEND = "sqlite"
        Config.SQLITE_PATH = os.environ["SQLITE_PATH"]

        from app import create_app
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def login_staff(self, username="admin", password="admin123"):
        return self.client.post(
            "/login",
            data={"login_type": "staff", "login_id": username, "password": password},
            follow_redirects=True,
        )

    def login_student(self, student_code, password):
        return self.client.post(
            "/login",
            data={"login_type": "student", "login_id": student_code, "password": password},
            follow_redirects=True,
        )

    def admit_student(self, name, category="Junior Tamil Basic", paid=True, due_day=10):
        data = {
            "full_name": name,
            "father_guardian_name": "Sundaram",
            "guardian_occupation": "Farmer",
            "gender": "Female",
            "dob": "2006-05-14",
            "qualification": "12th",
            "school_college": "Govt HSS",
            "phone": "9876543210",
            "address": "12 Main Road",
            "city": "Salem",
            "pincode": "636001",
            "course_category": category,
            "batch_timing": "08:00 AM - 09:00 AM",
            "admission_date": date.today().isoformat(),
            "admission_fee": "200",
            "monthly_fee": "500",
            "fee_due_day": str(due_day),
            "initial_password": "pass123",
        }
        if paid:
            data["mark_first_month_paid"] = "on"
        return self.client.post("/admin/admission", data=data, follow_redirects=True)

    def test_01_admin_self_credential_change(self):
        resp = self.login_staff("admin", "admin123")
        self.assertIn(b"Staff &amp; Admin Control Panel", resp.data)

        resp = self.client.post(
            "/admin/account",
            data={
                "action": "update_self",
                "new_username": "chief_admin",
                "full_name": "Shiva Principal",
                "phone": "9000011111",
                "current_password": "admin123",
                "new_password": "newpass99",
                "confirm_password": "newpass99",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Admin Login ID and account credentials updated", resp.data)

        self.client.get("/logout")
        bad = self.login_staff("admin", "admin123")
        self.assertIn(b"Invalid Staff / Admin Login ID or Password", bad.data)

        ok = self.login_staff("chief_admin", "newpass99")
        self.assertIn(b"Staff &amp; Admin Control Panel", ok.data)

    def test_02_sequential_ids_and_delete_wrong_admission(self):
        self.login_staff()
        r1 = self.admit_student("Priya K", "Junior English Basic", paid=True)
        self.assertIn(b"SCI001", r1.data)

        r2 = self.admit_student("Wrong Entry", "Junior Tamil Basic", paid=True)
        self.assertIn(b"SCI002", r2.data)

        # Delete wrong admission SCI002
        from db import get_db
        with get_db() as db:
            wrong = db.fetchone("SELECT id FROM students WHERE student_code = 'SCI002'")
            self.assertIsNotNone(wrong)
            wrong_id = wrong["id"]

        del_resp = self.client.post(f"/admin/students/{wrong_id}/delete", follow_redirects=True)
        self.assertIn(b"Deleted admission record SCI002", del_resp.data)

        # Next admission continues sequentially to SCI003
        r3 = self.admit_student("Karthik R", "Senior English Speed", paid=True)
        self.assertIn(b"SCI003", r3.data)

    def test_03_auto_attendance_student_pw_change_and_practice(self):
        self.login_staff()
        self.admit_student("Anitha M", "Junior Tamil Speed", paid=True)
        self.client.get("/logout")

        # Student login marks attendance automatically
        stu_resp = self.login_student("SCI001", "pass123")
        self.assertIn(b"Attendance automatically marked Present", stu_resp.data)

        # Change student password
        pw_resp = self.client.post(
            "/student/change-password",
            data={
                "current_password": "pass123",
                "new_password": "anitha77",
                "confirm_password": "anitha77",
            },
            follow_redirects=True,
        )
        self.assertIn(b"password has been updated", pw_resp.data)

        # Check Practice Arena (10-minute timer, 6 categories & dynamic English/Tamil keyboard)
        arena = self.client.get("/student/practice")
        self.assertIn(b"10:00", arena.data)
        self.assertIn(b"Junior English Basic", arena.data)
        self.assertIn(b"Senior Tamil Speed", arena.data)
        self.assertIn(b"virtualKeyboard", arena.data)
        self.assertIn(b"tamilLayoutSelect", arena.data)

        # Verify API returns Practice 1..N and 600s duration for all 6 categories
        for cat in [
            "Junior English Basic",
            "Junior English Speed",
            "Senior English Speed",
            "Junior Tamil Basic",
            "Junior Tamil Speed",
            "Senior Tamil Speed",
        ]:
            api_resp = self.client.get(f"/api/practice-passages?category={cat}")
            self.assertEqual(api_resp.status_code, 200)
            payload = api_resp.get_json()
            self.assertEqual(payload["duration_seconds"], 600)
            self.assertGreaterEqual(len(payload["sessions"]), 1)

        # Save a practice session
        save_resp = self.client.post(
            "/api/practice-sessions",
            json={
                "category": "Junior Tamil Speed",
                "practice_number": 1,
                "content_type": "paragraph",
                "duration_sec": 600,
                "strokes": 1300,
                "wpm": 28,
                "accuracy_pct": 95,
                "errors": 5,
                "weak_chars": "'க' (2)",
            },
        )
        self.assertEqual(save_resp.status_code, 200)
        self.assertTrue(save_resp.get_json()["saved"])

        # Re-login with new password works
        self.client.get("/logout")
        relogin = self.login_student("SCI001", "anitha77")
        self.assertIn(b"Welcome back Anitha M", relogin.data)

    def test_04_fee_intimation_and_overdue_login_block(self):
        self.login_staff()
        self.admit_student("Bala V", "Senior Tamil Speed", paid=False)

        # Make due_date in the future -> intimation shown, login allowed
        from db import get_db
        future_due = (date.today() + timedelta(days=3)).isoformat()
        with get_db() as db:
            stu = db.fetchone("SELECT id FROM students WHERE student_code = 'SCI001'")
            fee = db.fetchone("SELECT id FROM fee_payments WHERE student_id = %s", (stu["id"],))
            db.execute("UPDATE fee_payments SET due_date = %s, status = 'Pending' WHERE id = %s", (future_due, fee["id"]))
            db.commit()

        self.client.get("/logout")
        allowed = self.login_student("SCI001", "pass123")
        self.assertIn(b"Monthly Fee Intimation Notice", allowed.data)

        # Remove today's attendance and make fee overdue (due_date in the past) -> login MUST block & NOT mark attendance
        self.client.get("/logout")
        past_due = (date.today() - timedelta(days=2)).isoformat()
        with get_db() as db:
            db.execute("DELETE FROM attendance WHERE student_id = %s", (stu["id"],))
            db.execute("UPDATE fee_payments SET due_date = %s, status = 'Pending' WHERE id = %s", (past_due, fee["id"]))
            db.commit()

        blocked = self.client.post(
            "/login",
            data={"login_type": "student", "login_id": "SCI001", "password": "pass123"},
            follow_redirects=False,
        )
        self.assertEqual(blocked.status_code, 403)
        self.assertIn(b"Practice Login Blocked", blocked.data)

        with get_db() as db:
            att = db.fetchone("SELECT * FROM attendance WHERE student_id = %s", (stu["id"],))
            self.assertIsNone(att)

        # Staff marks fee Paid -> student login works again
        self.login_staff()
        self.client.post(
            f"/admin/fees/{fee['id']}/pay",
            data={"payment_mode": "Cash", "billing_month": date.today().strftime("%Y-%m")},
            follow_redirects=True,
        )
        self.client.get("/logout")
        restored = self.login_student("SCI001", "pass123")
        self.assertIn(b"Attendance automatically marked Present", restored.data)

    def test_05_css_and_js_requirements(self):
        css_text = (APP_DIR / "static" / "css" / "style.css").read_text(encoding="utf-8")
        self.assertIn("font-size: 14px !important;", css_text)
        self.assertIn("font-size: 20px !important;", css_text)
        js_text = (APP_DIR / "static" / "js" / "practice.js").read_text(encoding="utf-8")
        self.assertIn("const PRACTICE_DURATION_SECONDS = 600;", js_text)
        self.assertIn("BASIC_DRILL_POOLS", js_text)
        self.assertIn("FALLBACK_PASSAGE_POOLS", js_text)
        self.assertIn("ENGLISH_KEYBOARD_ROWS", js_text)
        self.assertIn("TAMIL_TYPEWRITER_ROWS", js_text)
        self.assertIn("TAMIL99_ROWS", js_text)

    def test_06_class_timings_7am_to_7pm_and_live_camera_photo(self):
        from config import Config
        self.assertEqual(Config.BATCH_TIMINGS[0], "07:00 AM - 08:00 AM")
        self.assertEqual(Config.BATCH_TIMINGS[-1], "06:00 PM - 07:00 PM")
        self.assertEqual(len(Config.BATCH_TIMINGS), 12)

        self.login_staff()
        adm_page = self.client.get("/admin/admission")
        self.assertIn(b"Live Camera", adm_page.data)
        self.assertIn(b"07:00 AM - 08:00 AM", adm_page.data)
        self.assertIn(b"06:00 PM - 07:00 PM", adm_page.data)

        # Tiny 1x1 PNG base64 capture
        tiny_png = (
            "data:image/png;base64,"
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )
        resp = self.client.post(
            "/admin/admission",
            data={
                "full_name": "Cam Test Student",
                "father_guardian_name": "Ravi",
                "gender": "Female",
                "dob": "2005-03-12",
                "qualification": "B.Sc",
                "phone": "9876500001",
                "address": "10 Temple St",
                "course_category": "Junior English Basic",
                "batch_timing": "07:00 AM - 08:00 AM",
                "admission_date": date.today().isoformat(),
                "admission_fee": "200",
                "monthly_fee": "500",
                "fee_due_day": "10",
                "initial_password": "stu123",
                "mark_first_month_paid": "on",
                "captured_photo_data": tiny_png,
            },
            follow_redirects=True,
        )
        self.assertIn(b"Cam Test Student", resp.data)
        from db import get_db
        with get_db() as db:
            stu = db.fetchone("SELECT id, photo_filename FROM students WHERE full_name = 'Cam Test Student'")
            self.assertTrue(stu["photo_filename"].endswith("_camera.png"))
            photo_path = APP_DIR / "static" / "uploads" / "photos" / stu["photo_filename"]
            self.assertTrue(photo_path.is_file())
            # Clean up test uploaded file
            self.client.post(f"/admin/students/{stu['id']}/delete", follow_redirects=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
