import base64
import calendar
import os
import re
import uuid
from datetime import date, datetime
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from config import Config
from db import get_db, init_db_schema
from seed_data import seed_initial_data


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Ensure schema & seed exist when running locally with sqlite or initialized MySQL
    try:
        init_db_schema()
        seed_initial_data()
    except Exception as exc:
        app.logger.warning("Startup DB init skipped or failed: %s", exc)

    # ------------------------------------------------------------------
    # Helpers: Auth, IDs, Fees, Attendance
    # ------------------------------------------------------------------
    def allowed_file(filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
        )

    def save_admission_photo(photo_file, captured_data, existing_filename=""):
        """Save uploaded image file or base64 live-camera capture."""
        if captured_data:
            match = re.match(
                r"^data:image/(png|jpeg|jpg|webp);base64,(.+)$",
                captured_data.strip(),
                re.IGNORECASE | re.DOTALL,
            )
            if match:
                ext = "jpg" if match.group(1).lower() == "jpeg" else match.group(1).lower()
                raw_bytes = base64.b64decode(match.group(2))
                filename = f"{uuid.uuid4().hex[:12]}_camera.{ext}"
                with open(os.path.join(app.config["UPLOAD_FOLDER"], filename), "wb") as fh:
                    fh.write(raw_bytes)
                return filename

        if photo_file and photo_file.filename and allowed_file(photo_file.filename):
            ext = photo_file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex[:12]}_{secure_filename(photo_file.filename)}"
            if not filename.lower().endswith(ext):
                filename = f"{filename}.{ext}"
            photo_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return filename

        return existing_filename

    def staff_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if session.get("user_type") != "staff" or not session.get("user_id"):
                flash("Please sign in with your Staff / Admin Login ID.", "warning")
                return redirect(url_for("login", role="staff"))
            return fn(*args, **kwargs)

        return wrapper

    def student_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if session.get("user_type") != "student" or not session.get("user_id"):
                flash("Please sign in with your Student ID.", "warning")
                return redirect(url_for("login", role="student"))
            return fn(*args, **kwargs)

        return wrapper

    def clamp_due_date(billing_month, due_day):
        year, month = map(int, billing_month.split("-"))
        max_day = calendar.monthrange(year, month)[1]
        day = max(1, min(int(due_day or 10), max_day))
        return f"{year:04d}-{month:02d}-{day:02d}"

    def peek_next_student_code(db):
        row = db.fetchone(
            "SELECT last_number FROM institute_counters WHERE counter_key = %s",
            ("student_code",),
        )
        next_num = (row["last_number"] if row else 0) + 1
        return f"SCI{next_num:03d}"

    def allocate_next_student_code(db):
        row = db.fetchone(
            "SELECT last_number FROM institute_counters WHERE counter_key = %s",
            ("student_code",),
        )
        if not row:
            next_num = 1
            db.execute(
                "INSERT INTO institute_counters (counter_key, last_number) VALUES (%s, %s)",
                ("student_code", next_num),
            )
        else:
            next_num = int(row["last_number"]) + 1
            db.execute(
                "UPDATE institute_counters SET last_number = %s WHERE counter_key = %s",
                (next_num, "student_code"),
            )
        return f"SCI{next_num:03d}"

    def ensure_month_fee_record(db, student, billing_month):
        existing = db.fetchone(
            "SELECT * FROM fee_payments WHERE student_id = %s AND billing_month = %s",
            (student["id"], billing_month),
        )
        if existing:
            return existing

        due_date = clamp_due_date(billing_month, student.get("fee_due_day", 10))
        today_str = date.today().isoformat()
        initial_status = "Overdue" if due_date < today_str else "Pending"
        db.execute(
            """
            INSERT INTO fee_payments
                (student_id, billing_month, amount, due_date, status, intimation_note)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                student["id"],
                billing_month,
                student["monthly_fee"],
                due_date,
                initial_status,
                f"Monthly tuition fee for {billing_month}",
            ),
        )
        return db.fetchone(
            "SELECT * FROM fee_payments WHERE student_id = %s AND billing_month = %s",
            (student["id"], billing_month),
        )

    def evaluate_student_fee_access(db, student, today=None):
        """
        Check monthly fee status for a student.
        - Auto-generates the current month's fee invoice if missing.
        - Marks any unpaid fee with due_date < today as 'Overdue' and blocks login.
        - Returns dict with is_blocked, overdue_fees, pending_fees, current_fee.
        """
        today_dt = today or date.today()
        today_str = today_dt.isoformat()
        current_month = today_dt.strftime("%Y-%m")

        if student["status"] == "Active":
            ensure_month_fee_record(db, student, current_month)

        unpaid = db.fetchall(
            """
            SELECT * FROM fee_payments
            WHERE student_id = %s AND status != 'Paid'
            ORDER BY billing_month ASC
            """,
            (student["id"],),
        )

        overdue_fees = []
        pending_fees = []
        for fee in unpaid:
            if fee["due_date"] < today_str:
                if fee["status"] != "Overdue":
                    db.execute(
                        "UPDATE fee_payments SET status = 'Overdue' WHERE id = %s",
                        (fee["id"],),
                    )
                    fee["status"] = "Overdue"
                overdue_fees.append(fee)
            else:
                pending_fees.append(fee)

        db.commit()

        current_fee = db.fetchone(
            "SELECT * FROM fee_payments WHERE student_id = %s AND billing_month = %s",
            (student["id"], current_month),
        )

        return {
            "is_blocked": len(overdue_fees) > 0,
            "overdue_fees": overdue_fees,
            "pending_fees": pending_fees,
            "current_fee": current_fee,
            "total_due": sum(f["amount"] for f in unpaid),
        }

    def mark_auto_attendance(db, student, now=None):
        now_dt = now or datetime.now()
        att_date = now_dt.strftime("%Y-%m-%d")
        att_time = now_dt.strftime("%H:%M:%S")
        existing = db.fetchone(
            "SELECT * FROM attendance WHERE student_id = %s AND attendance_date = %s",
            (student["id"], att_date),
        )
        if existing:
            return False, existing

        db.execute(
            """
            INSERT INTO attendance
                (student_id, attendance_date, login_time, status, marked_by, practice_category)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                student["id"],
                att_date,
                att_time,
                "Present",
                "AUTO_LOGIN",
                student["course_category"],
            ),
        )
        db.commit()
        created = db.fetchone(
            "SELECT * FROM attendance WHERE student_id = %s AND attendance_date = %s",
            (student["id"], att_date),
        )
        return True, created

    @app.context_processor
    def inject_globals():
        return {
            "institute_name": Config.INSTITUTE_NAME,
            "institute_subtitle": Config.INSTITUTE_SUBTITLE,
            "course_categories": Config.COURSE_CATEGORIES,
            "batch_timings": Config.BATCH_TIMINGS,
            "practice_duration_seconds": Config.PRACTICE_DURATION_SECONDS,
            "today_iso": date.today().isoformat(),
            "current_month": date.today().strftime("%Y-%m"),
        }

    # ------------------------------------------------------------------
    # Authentication Routes
    # ------------------------------------------------------------------
    @app.route("/")
    def index():
        if session.get("user_type") == "staff":
            return redirect(url_for("admin_dashboard"))
        if session.get("user_type") == "student":
            return redirect(url_for("student_dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        active_role = request.args.get("role", "student")
        fee_block_info = None

        if request.method == "POST":
            login_type = request.form.get("login_type", "student").strip()
            active_role = login_type
            login_id = request.form.get("login_id", "").strip()
            password = request.form.get("password", "")

            if not login_id or not password:
                flash("Please enter both Login ID and Password.", "danger")
                return render_template("login.html", active_role=active_role)

            with get_db() as db:
                if login_type == "staff":
                    staff = db.fetchone(
                        "SELECT * FROM staff_users WHERE username = %s",
                        (login_id,),
                    )
                    if not staff or not check_password_hash(staff["password_hash"], password):
                        flash("Invalid Staff / Admin Login ID or Password.", "danger")
                        return render_template("login.html", active_role="staff")

                    session.clear()
                    session["user_type"] = "staff"
                    session["user_id"] = staff["id"]
                    session["username"] = staff["username"]
                    session["full_name"] = staff["full_name"]
                    session["role"] = staff["role"]
                    flash(f"Welcome back, {staff['full_name']}!", "success")
                    return redirect(url_for("admin_dashboard"))

                # Student login flow
                student = db.fetchone(
                    "SELECT * FROM students WHERE UPPER(student_code) = UPPER(%s)",
                    (login_id,),
                )
                if not student or not check_password_hash(student["password_hash"], password):
                    flash("Invalid Student ID or Password.", "danger")
                    return render_template("login.html", active_role="student")

                if student["status"] != "Active":
                    flash(
                        "Your student account is currently inactive. Contact the institute office.",
                        "danger",
                    )
                    return render_template("login.html", active_role="student")

                # Monthly Fee Delay Block Check BEFORE allowing practice login or marking attendance
                fee_status = evaluate_student_fee_access(db, student)
                if fee_status["is_blocked"]:
                    fee_block_info = {
                        "student": student,
                        "overdue_fees": fee_status["overdue_fees"],
                        "total_due": fee_status["total_due"],
                    }
                    flash(
                        "Login Blocked: Monthly tuition fee payment is delayed/overdue. "
                        "Please clear your pending fee at the office to restore practice access.",
                        "danger",
                    )
                    return (
                        render_template(
                            "login.html",
                            active_role="student",
                            fee_block_info=fee_block_info,
                        ),
                        403,
                    )

                # Mark attendance automatically on successful practice login
                marked_now, att_row = mark_auto_attendance(db, student)

                session.clear()
                session["user_type"] = "student"
                session["user_id"] = student["id"]
                session["student_code"] = student["student_code"]
                session["full_name"] = student["full_name"]
                session["course_category"] = student["course_category"]
                session["attendance_marked_now"] = marked_now
                session["attendance_time"] = att_row["login_time"] if att_row else ""

                if marked_now:
                    flash(
                        f"Welcome {student['full_name']}! Attendance automatically marked Present at {att_row['login_time']}.",
                        "success",
                    )
                else:
                    flash(
                        f"Welcome back {student['full_name']}! Today's attendance is already recorded ({att_row['login_time']}).",
                        "info",
                    )
                return redirect(url_for("student_dashboard"))

        return render_template("login.html", active_role=active_role, fee_block_info=fee_block_info)

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out safely.", "info")
        return redirect(url_for("login"))

    # ------------------------------------------------------------------
    # Student Portal Routes
    # ------------------------------------------------------------------
    @app.route("/student/dashboard")
    @student_required
    def student_dashboard():
        with get_db() as db:
            student = db.fetchone(
                "SELECT * FROM students WHERE id = %s", (session["user_id"],)
            )
            if not student:
                session.clear()
                return redirect(url_for("login"))

            fee_status = evaluate_student_fee_access(db, student)
            today_att = db.fetchone(
                "SELECT * FROM attendance WHERE student_id = %s AND attendance_date = %s",
                (student["id"], date.today().isoformat()),
            )
            att_count = db.fetchone(
                "SELECT COUNT(*) AS cnt FROM attendance WHERE student_id = %s AND status = 'Present'",
                (student["id"],),
            )["cnt"]
            recent_sessions = db.fetchall(
                """
                SELECT * FROM practice_sessions
                WHERE student_id = %s
                ORDER BY practiced_at DESC, id DESC
                LIMIT 8
                """,
                (student["id"],),
            )
            stats_row = db.fetchone(
                """
                SELECT COUNT(*) AS total_sessions,
                       COALESCE(MAX(wpm), 0) AS best_wpm,
                       COALESCE(ROUND(AVG(accuracy_pct)), 100) AS avg_acc
                FROM practice_sessions
                WHERE student_id = %s
                """,
                (student["id"],),
            )
            passages_by_cat = {}
            for cat in Config.COURSE_CATEGORIES:
                rows = db.fetchall(
                    """
                    SELECT practice_number, title, content_type
                    FROM practice_passages
                    WHERE category = %s
                    ORDER BY practice_number ASC
                    """,
                    (cat,),
                )
                passages_by_cat[cat] = rows

        return render_template(
            "student/dashboard.html",
            student=student,
            fee_status=fee_status,
            today_att=today_att,
            att_count=att_count,
            recent_sessions=recent_sessions,
            stats=stats_row,
            passages_by_cat=passages_by_cat,
        )

    @app.route("/student/practice")
    @student_required
    def student_practice():
        with get_db() as db:
            student = db.fetchone(
                "SELECT * FROM students WHERE id = %s", (session["user_id"],)
            )
            fee_status = evaluate_student_fee_access(db, student)
            if fee_status["is_blocked"]:
                session.clear()
                flash("Practice access blocked due to overdue monthly fee.", "danger")
                return redirect(url_for("login"))

            selected_category = request.args.get("category") or student["course_category"]
            if selected_category not in Config.COURSE_CATEGORIES:
                selected_category = student["course_category"]
            selected_practice = request.args.get("practice", "1")

            today_att = db.fetchone(
                "SELECT * FROM attendance WHERE student_id = %s AND attendance_date = %s",
                (student["id"], date.today().isoformat()),
            )

        return render_template(
            "student/practice.html",
            student=student,
            fee_status=fee_status,
            today_att=today_att,
            selected_category=selected_category,
            selected_practice=selected_practice,
        )

    @app.route("/student/attendance")
    @student_required
    def student_attendance():
        with get_db() as db:
            student = db.fetchone(
                "SELECT * FROM students WHERE id = %s", (session["user_id"],)
            )
            records = db.fetchall(
                """
                SELECT * FROM attendance
                WHERE student_id = %s
                ORDER BY attendance_date DESC
                """,
                (student["id"],),
            )
        return render_template(
            "student/attendance.html", student=student, records=records
        )

    @app.route("/student/fees")
    @student_required
    def student_fees():
        with get_db() as db:
            student = db.fetchone(
                "SELECT * FROM students WHERE id = %s", (session["user_id"],)
            )
            fee_status = evaluate_student_fee_access(db, student)
            fees = db.fetchall(
                """
                SELECT * FROM fee_payments
                WHERE student_id = %s
                ORDER BY billing_month DESC
                """,
                (student["id"],),
            )
        return render_template(
            "student/fees.html", student=student, fee_status=fee_status, fees=fees
        )

    @app.route("/student/change-password", methods=["GET", "POST"])
    @student_required
    def student_change_password():
        with get_db() as db:
            student = db.fetchone(
                "SELECT * FROM students WHERE id = %s", (session["user_id"],)
            )
            if request.method == "POST":
                current_pw = request.form.get("current_password", "")
                new_pw = request.form.get("new_password", "")
                confirm_pw = request.form.get("confirm_password", "")

                if not check_password_hash(student["password_hash"], current_pw):
                    flash("Current password is incorrect.", "danger")
                elif len(new_pw) < 4:
                    flash("New password must be at least 4 characters long.", "danger")
                elif new_pw != confirm_pw:
                    flash("New password and confirmation do not match.", "danger")
                else:
                    db.execute(
                        "UPDATE students SET password_hash = %s WHERE id = %s",
                        (generate_password_hash(new_pw), student["id"]),
                    )
                    db.commit()
                    flash("Your password has been updated successfully!", "success")
                    return redirect(url_for("student_dashboard"))

        return render_template("student/change_password.html", student=student)

    # ------------------------------------------------------------------
    # Typing Practice JSON APIs (used by static/js/practice.js)
    # ------------------------------------------------------------------
    @app.route("/api/practice-passages")
    def api_practice_passages():
        category = request.args.get("category", "Junior Tamil Basic").strip()
        content_type = request.args.get("type", "").strip().lower()
        practice_number = request.args.get("practice_number", "").strip()

        with get_db() as db:
            sql = "SELECT * FROM practice_passages WHERE category = %s"
            params = [category]
            if content_type in ("word", "paragraph"):
                sql += " AND content_type = %s"
                params.append(content_type)
            if practice_number.isdigit():
                sql += " AND practice_number = %s"
                params.append(int(practice_number))
            sql += " ORDER BY practice_number ASC"
            rows = db.fetchall(sql, tuple(params))

        sessions_list = []
        paragraphs = []
        for r in rows:
            parts = [p.strip() for p in r["passage_text"].split("\n\n") if p.strip()]
            paragraphs.extend(parts)
            sessions_list.append(
                {
                    "id": r["id"],
                    "practice_number": r["practice_number"],
                    "title": r["title"],
                    "content_type": r["content_type"],
                    "passage_text": r["passage_text"],
                    "paragraphs": parts,
                    "target_wpm": r["target_wpm"],
                    "target_strokes": r["target_strokes"],
                }
            )

        return jsonify(
            {
                "category": category,
                "sessions": sessions_list,
                "paragraphs": paragraphs,
                "duration_seconds": Config.PRACTICE_DURATION_SECONDS,
            }
        )

    @app.route("/api/practice-sessions", methods=["POST"])
    def api_save_practice_session():
        if session.get("user_type") not in ("student", "staff") or not session.get("user_id"):
            return jsonify({"error": "Authentication required"}), 401

        data = request.get_json(silent=True) or {}
        category = data.get("category", "Junior Tamil Basic")
        practice_number = int(data.get("practice_number") or 1)
        content_type = data.get("content_type", "paragraph")
        duration_sec = int(data.get("duration_sec") or 0)
        strokes = int(data.get("strokes") or 0)
        wpm = int(data.get("wpm") or 0)
        accuracy_pct = int(data.get("accuracy_pct") or 100)
        errors = int(data.get("errors") or 0)
        weak_chars = str(data.get("weak_chars") or "")[:250]

        with get_db() as db:
            passage = db.fetchone(
                "SELECT target_wpm, target_strokes FROM practice_passages WHERE category = %s AND practice_number = %s",
                (category, practice_number),
            )
            if not passage:
                passage = db.fetchone(
                    "SELECT target_wpm, target_strokes FROM practice_passages WHERE category = %s ORDER BY practice_number ASC LIMIT 1",
                    (category,),
                )
            target_wpm = int(passage["target_wpm"]) if passage else (45 if "Senior" in category else 30)
            target_strokes = int(passage["target_strokes"]) if passage else (1750 if "Senior" in category else 1200)
            target_met = 1 if (wpm >= target_wpm and accuracy_pct >= 90) else 0

            if session.get("user_type") == "student":
                db.execute(
                    """
                    INSERT INTO practice_sessions
                        (student_id, category, practice_number, content_type, duration_sec,
                         strokes, wpm, accuracy_pct, errors, weak_chars, target_met)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        session["user_id"],
                        category,
                        practice_number,
                        content_type,
                        duration_sec,
                        strokes,
                        wpm,
                        accuracy_pct,
                        errors,
                        weak_chars,
                        target_met,
                    ),
                )
                db.commit()

        return jsonify(
            {
                "saved": True,
                "target_met": bool(target_met),
                "target_wpm": target_wpm,
                "target_strokes": target_strokes,
            }
        )

    # ------------------------------------------------------------------
    # Staff / Admin Portal Routes
    # ------------------------------------------------------------------
    @app.route("/admin/dashboard")
    @staff_required
    def admin_dashboard():
        today_str = date.today().isoformat()
        with get_db() as db:
            students = db.fetchall("SELECT * FROM students WHERE status = 'Active'")
            overdue_count = 0
            pending_count = 0
            for stu in students:
                fs = evaluate_student_fee_access(db, stu)
                if fs["is_blocked"]:
                    overdue_count += 1
                elif fs["pending_fees"]:
                    pending_count += 1

            total_students = db.fetchone("SELECT COUNT(*) AS cnt FROM students")["cnt"]
            today_present = db.fetchone(
                "SELECT COUNT(*) AS cnt FROM attendance WHERE attendance_date = %s AND status = 'Present'",
                (today_str,),
            )["cnt"]

            recent_admissions = db.fetchall(
                "SELECT * FROM students ORDER BY id DESC LIMIT 6"
            )
            recent_attendance = db.fetchall(
                """
                SELECT a.*, s.student_code, s.full_name, s.course_category
                FROM attendance a
                JOIN students s ON s.id = a.student_id
                WHERE a.attendance_date = %s
                ORDER BY a.login_time DESC
                LIMIT 8
                """,
                (today_str,),
            )
            category_counts = db.fetchall(
                """
                SELECT course_category, COUNT(*) AS cnt
                FROM students
                GROUP BY course_category
                ORDER BY cnt DESC
                """
            )

        return render_template(
            "admin/dashboard.html",
            total_students=total_students,
            today_present=today_present,
            overdue_count=overdue_count,
            pending_count=pending_count,
            recent_admissions=recent_admissions,
            recent_attendance=recent_attendance,
            category_counts=category_counts,
        )

    @app.route("/admin/admission", methods=["GET", "POST"])
    @staff_required
    def admin_admission():
        with get_db() as db:
            next_code_preview = peek_next_student_code(db)

            if request.method == "POST":
                full_name = request.form.get("full_name", "").strip()
                father_guardian_name = request.form.get("father_guardian_name", "").strip()
                guardian_occupation = request.form.get("guardian_occupation", "").strip()
                gender = request.form.get("gender", "Female").strip()
                dob = request.form.get("dob", "").strip()
                qualification = request.form.get("qualification", "").strip()
                school_college = request.form.get("school_college", "").strip()
                phone = request.form.get("phone", "").strip()
                alt_phone = request.form.get("alt_phone", "").strip()
                email = request.form.get("email", "").strip()
                address = request.form.get("address", "").strip()
                city = request.form.get("city", "").strip()
                pincode = request.form.get("pincode", "").strip()
                aadhaar_no = request.form.get("aadhaar_no", "").strip()
                course_category = request.form.get("course_category", "").strip()
                batch_timing = request.form.get("batch_timing", "").strip()
                machine_no = request.form.get("machine_no", "").strip()
                admission_date = request.form.get("admission_date") or date.today().isoformat()
                admission_fee = float(request.form.get("admission_fee") or Config.DEFAULT_ADMISSION_FEE)
                monthly_fee = float(request.form.get("monthly_fee") or Config.DEFAULT_MONTHLY_FEE)
                fee_due_day = int(request.form.get("fee_due_day") or Config.DEFAULT_FEE_DUE_DAY)
                initial_password = request.form.get("initial_password", "").strip() or "stu123"
                mark_first_month_paid = request.form.get("mark_first_month_paid") == "on"
                payment_mode = request.form.get("payment_mode", "Cash").strip()
                notes = request.form.get("notes", "").strip()

                if not full_name or not father_guardian_name or not dob or not phone or not address:
                    flash("Please fill in all required admission form fields (*).", "danger")
                    return render_template(
                        "admin/admission.html",
                        next_code=next_code_preview,
                        form_data=request.form,
                    )

                photo_filename = save_admission_photo(
                    request.files.get("photo"),
                    request.form.get("captured_photo_data", ""),
                    "",
                )

                student_code = allocate_next_student_code(db)
                student_id = db.execute(
                    """
                    INSERT INTO students (
                        student_code, full_name, father_guardian_name, guardian_occupation,
                        gender, dob, qualification, school_college, phone, alt_phone, email,
                        address, city, pincode, aadhaar_no, course_category, batch_timing,
                        machine_no, admission_date, admission_fee, monthly_fee, fee_due_day,
                        photo_filename, password_hash, status, notes
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                    """,
                    (
                        student_code,
                        full_name,
                        father_guardian_name,
                        guardian_occupation,
                        gender,
                        dob,
                        qualification,
                        school_college,
                        phone,
                        alt_phone,
                        email,
                        address,
                        city,
                        pincode,
                        aadhaar_no,
                        course_category,
                        batch_timing,
                        machine_no,
                        admission_date,
                        admission_fee,
                        monthly_fee,
                        fee_due_day,
                        photo_filename,
                        generate_password_hash(initial_password),
                        "Active",
                        notes,
                    ),
                )

                # Create first billing month record based on admission date
                billing_month = admission_date[:7]
                due_date = clamp_due_date(billing_month, fee_due_day)
                if mark_first_month_paid:
                    receipt_no = f"RCPT-{student_code}-{billing_month.replace('-', '')}"
                    db.execute(
                        """
                        INSERT INTO fee_payments
                            (student_id, billing_month, amount, due_date, paid_date, status, payment_mode, receipt_no, intimation_note)
                        VALUES (%s, %s, %s, %s, %s, 'Paid', %s, %s, %s)
                        """,
                        (
                            student_id,
                            billing_month,
                            monthly_fee,
                            due_date,
                            date.today().isoformat(),
                            payment_mode,
                            receipt_no,
                            "Paid at admission",
                        ),
                    )
                else:
                    status = "Overdue" if due_date < date.today().isoformat() else "Pending"
                    db.execute(
                        """
                        INSERT INTO fee_payments
                            (student_id, billing_month, amount, due_date, status, intimation_note)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            student_id,
                            billing_month,
                            monthly_fee,
                            due_date,
                            status,
                            f"Monthly fee due on {due_date}",
                        ),
                    )

                db.commit()
                flash(
                    f"Admission saved! Auto-generated Student ID: {student_code} | Initial Password: {initial_password}",
                    "success",
                )
                return redirect(url_for("admin_student_detail", student_id=student_id))

        return render_template(
            "admin/admission.html", next_code=next_code_preview, form_data={}
        )

    @app.route("/admin/students")
    @staff_required
    def admin_students():
        q = request.args.get("q", "").strip()
        category = request.args.get("category", "").strip()

        with get_db() as db:
            sql = "SELECT * FROM students WHERE 1=1"
            params = []
            if q:
                sql += " AND (UPPER(student_code) LIKE UPPER(%s) OR UPPER(full_name) LIKE UPPER(%s) OR phone LIKE %s)"
                like = f"%{q}%"
                params.extend([like, like, like])
            if category:
                sql += " AND course_category = %s"
                params.append(category)
            sql += " ORDER BY id DESC"
            students = db.fetchall(sql, tuple(params))

            for stu in students:
                fs = evaluate_student_fee_access(db, stu)
                stu["fee_blocked"] = fs["is_blocked"]
                stu["total_due"] = fs["total_due"]

        return render_template(
            "admin/students.html",
            students=students,
            q=q,
            selected_category=category,
        )

    @app.route("/admin/students/<int:student_id>")
    @staff_required
    def admin_student_detail(student_id):
        with get_db() as db:
            student = db.fetchone("SELECT * FROM students WHERE id = %s", (student_id,))
            if not student:
                flash("Student admission record not found.", "warning")
                return redirect(url_for("admin_students"))

            fee_status = evaluate_student_fee_access(db, student)
            fees = db.fetchall(
                "SELECT * FROM fee_payments WHERE student_id = %s ORDER BY billing_month DESC",
                (student_id,),
            )
            attendance = db.fetchall(
                "SELECT * FROM attendance WHERE student_id = %s ORDER BY attendance_date DESC LIMIT 15",
                (student_id,),
            )
            sessions = db.fetchall(
                "SELECT * FROM practice_sessions WHERE student_id = %s ORDER BY practiced_at DESC LIMIT 10",
                (student_id,),
            )

        return render_template(
            "admin/student_detail.html",
            student=student,
            fee_status=fee_status,
            fees=fees,
            attendance=attendance,
            sessions=sessions,
        )

    @app.route("/admin/students/<int:student_id>/edit", methods=["GET", "POST"])
    @staff_required
    def admin_student_edit(student_id):
        with get_db() as db:
            student = db.fetchone("SELECT * FROM students WHERE id = %s", (student_id,))
            if not student:
                flash("Student not found.", "warning")
                return redirect(url_for("admin_students"))

            if request.method == "POST":
                full_name = request.form.get("full_name", "").strip()
                father_guardian_name = request.form.get("father_guardian_name", "").strip()
                guardian_occupation = request.form.get("guardian_occupation", "").strip()
                gender = request.form.get("gender", student["gender"]).strip()
                dob = request.form.get("dob", student["dob"]).strip()
                qualification = request.form.get("qualification", "").strip()
                school_college = request.form.get("school_college", "").strip()
                phone = request.form.get("phone", "").strip()
                alt_phone = request.form.get("alt_phone", "").strip()
                email = request.form.get("email", "").strip()
                address = request.form.get("address", "").strip()
                city = request.form.get("city", "").strip()
                pincode = request.form.get("pincode", "").strip()
                aadhaar_no = request.form.get("aadhaar_no", "").strip()
                course_category = request.form.get("course_category", "").strip()
                batch_timing = request.form.get("batch_timing", "").strip()
                machine_no = request.form.get("machine_no", "").strip()
                admission_date = request.form.get("admission_date") or student["admission_date"]
                admission_fee = float(request.form.get("admission_fee") or student["admission_fee"])
                monthly_fee = float(request.form.get("monthly_fee") or student["monthly_fee"])
                fee_due_day = int(request.form.get("fee_due_day") or student["fee_due_day"])
                status = request.form.get("status", "Active").strip()
                notes = request.form.get("notes", "").strip()
                new_password = request.form.get("new_password", "").strip()

                photo_filename = save_admission_photo(
                    request.files.get("photo"),
                    request.form.get("captured_photo_data", ""),
                    student["photo_filename"],
                )

                pw_hash = (
                    generate_password_hash(new_password)
                    if new_password
                    else student["password_hash"]
                )

                db.execute(
                    """
                    UPDATE students SET
                        full_name=%s, father_guardian_name=%s, guardian_occupation=%s,
                        gender=%s, dob=%s, qualification=%s, school_college=%s,
                        phone=%s, alt_phone=%s, email=%s, address=%s, city=%s,
                        pincode=%s, aadhaar_no=%s, course_category=%s, batch_timing=%s,
                        machine_no=%s, admission_date=%s, admission_fee=%s, monthly_fee=%s,
                        fee_due_day=%s, photo_filename=%s, password_hash=%s, status=%s, notes=%s
                    WHERE id=%s
                    """,
                    (
                        full_name,
                        father_guardian_name,
                        guardian_occupation,
                        gender,
                        dob,
                        qualification,
                        school_college,
                        phone,
                        alt_phone,
                        email,
                        address,
                        city,
                        pincode,
                        aadhaar_no,
                        course_category,
                        batch_timing,
                        machine_no,
                        admission_date,
                        admission_fee,
                        monthly_fee,
                        fee_due_day,
                        photo_filename,
                        pw_hash,
                        status,
                        notes,
                        student_id,
                    ),
                )
                db.commit()
                flash(f"Admission details for {student['student_code']} updated.", "success")
                return redirect(url_for("admin_student_detail", student_id=student_id))

        return render_template("admin/student_edit.html", student=student)

    @app.route("/admin/students/<int:student_id>/delete", methods=["POST"])
    @staff_required
    def admin_student_delete(student_id):
        with get_db() as db:
            student = db.fetchone("SELECT * FROM students WHERE id = %s", (student_id,))
            if not student:
                flash("Admission record not found.", "warning")
                return redirect(url_for("admin_students"))

            code = student["student_code"]
            name = student["full_name"]
            photo = student.get("photo_filename") or ""

            db.execute("DELETE FROM students WHERE id = %s", (student_id,))
            db.commit()

            if photo:
                photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo)
                if os.path.isfile(photo_path):
                    try:
                        os.remove(photo_path)
                    except OSError:
                        pass

        flash(f"Deleted admission record {code} ({name}).", "success")
        return redirect(url_for("admin_students"))

    @app.route("/admin/attendance", methods=["GET", "POST"])
    @staff_required
    def admin_attendance():
        filter_date = request.args.get("date") or date.today().isoformat()
        filter_category = request.args.get("category", "").strip()

        with get_db() as db:
            if request.method == "POST":
                student_id = int(request.form.get("student_id"))
                att_date = request.form.get("attendance_date") or date.today().isoformat()
                status = request.form.get("status", "Present")
                stu = db.fetchone("SELECT * FROM students WHERE id = %s", (student_id,))
                if stu:
                    existing = db.fetchone(
                        "SELECT id FROM attendance WHERE student_id = %s AND attendance_date = %s",
                        (student_id, att_date),
                    )
                    if existing:
                        db.execute(
                            "UPDATE attendance SET status = %s, marked_by = 'STAFF_MANUAL' WHERE id = %s",
                            (status, existing["id"]),
                        )
                    else:
                        db.execute(
                            """
                            INSERT INTO attendance
                                (student_id, attendance_date, login_time, status, marked_by, practice_category)
                            VALUES (%s, %s, %s, %s, 'STAFF_MANUAL', %s)
                            """,
                            (
                                student_id,
                                att_date,
                                datetime.now().strftime("%H:%M:%S"),
                                status,
                                stu["course_category"],
                            ),
                        )
                    db.commit()
                    flash(f"Attendance updated for {stu['student_code']}.", "success")
                return redirect(url_for("admin_attendance", date=att_date, category=filter_category))

            sql = """
                SELECT a.*, s.student_code, s.full_name, s.course_category, s.batch_timing
                FROM attendance a
                JOIN students s ON s.id = a.student_id
                WHERE a.attendance_date = %s
            """
            params = [filter_date]
            if filter_category:
                sql += " AND s.course_category = %s"
                params.append(filter_category)
            sql += " ORDER BY a.login_time DESC"
            records = db.fetchall(sql, tuple(params))

            all_students = db.fetchall(
                "SELECT id, student_code, full_name, course_category FROM students WHERE status = 'Active' ORDER BY student_code ASC"
            )

        return render_template(
            "admin/attendance.html",
            records=records,
            filter_date=filter_date,
            filter_category=filter_category,
            all_students=all_students,
        )

    @app.route("/admin/fees")
    @staff_required
    def admin_fees():
        filter_month = request.args.get("month") or date.today().strftime("%Y-%m")
        filter_status = request.args.get("status", "").strip()

        with get_db() as db:
            # Ensure active students have current-month fee rows updated
            active_students = db.fetchall("SELECT * FROM students WHERE status = 'Active'")
            for stu in active_students:
                ensure_month_fee_record(db, stu, filter_month)
                evaluate_student_fee_access(db, stu)

            sql = """
                SELECT f.*, s.student_code, s.full_name, s.phone, s.course_category, s.fee_due_day
                FROM fee_payments f
                JOIN students s ON s.id = f.student_id
                WHERE f.billing_month = %s
            """
            params = [filter_month]
            if filter_status:
                sql += " AND f.status = %s"
                params.append(filter_status)
            sql += " ORDER BY CASE f.status WHEN 'Overdue' THEN 1 WHEN 'Pending' THEN 2 ELSE 3 END, s.student_code ASC"
            fee_rows = db.fetchall(sql, tuple(params))

            summary = {"Paid": 0, "Pending": 0, "Overdue": 0, "collected_amt": 0.0, "due_amt": 0.0}
            all_month_rows = db.fetchall(
                "SELECT status, amount FROM fee_payments WHERE billing_month = %s",
                (filter_month,),
            )
            for row in all_month_rows:
                st = row["status"]
                if st in summary:
                    summary[st] += 1
                if st == "Paid":
                    summary["collected_amt"] += float(row["amount"])
                else:
                    summary["due_amt"] += float(row["amount"])

        return render_template(
            "admin/fees.html",
            fee_rows=fee_rows,
            filter_month=filter_month,
            filter_status=filter_status,
            summary=summary,
        )

    @app.route("/admin/fees/<int:fee_id>/pay", methods=["POST"])
    @staff_required
    def admin_fee_pay(fee_id):
        payment_mode = request.form.get("payment_mode", "Cash").strip()
        redirect_month = request.form.get("billing_month") or date.today().strftime("%Y-%m")
        with get_db() as db:
            fee = db.fetchone(
                """
                SELECT f.*, s.student_code, s.full_name
                FROM fee_payments f
                JOIN students s ON s.id = f.student_id
                WHERE f.id = %s
                """,
                (fee_id,),
            )
            if fee:
                receipt_no = f"RCPT-{fee['student_code']}-{fee['billing_month'].replace('-', '')}"
                db.execute(
                    """
                    UPDATE fee_payments
                    SET status = 'Paid', paid_date = %s, payment_mode = %s, receipt_no = %s
                    WHERE id = %s
                    """,
                    (date.today().isoformat(), payment_mode, receipt_no, fee_id),
                )
                db.commit()
                flash(
                    f"Fee marked PAID for {fee['student_code']} ({fee['full_name']}) — Receipt {receipt_no}. Login access is active!",
                    "success",
                )
        return redirect(url_for("admin_fees", month=redirect_month))

    @app.route("/admin/fees/<int:fee_id>/due-date", methods=["POST"])
    @staff_required
    def admin_fee_due_date(fee_id):
        new_due_date = request.form.get("due_date", "").strip()
        redirect_month = request.form.get("billing_month") or date.today().strftime("%Y-%m")
        if new_due_date:
            with get_db() as db:
                fee = db.fetchone("SELECT * FROM fee_payments WHERE id = %s", (fee_id,))
                if fee and fee["status"] != "Paid":
                    new_status = "Overdue" if new_due_date < date.today().isoformat() else "Pending"
                    db.execute(
                        "UPDATE fee_payments SET due_date = %s, status = %s WHERE id = %s",
                        (new_due_date, new_status, fee_id),
                    )
                    db.commit()
                    flash(
                        f"Updated due date to {new_due_date} (Status: {new_status}).",
                        "info",
                    )
        return redirect(url_for("admin_fees", month=redirect_month))

    @app.route("/admin/passages", methods=["GET", "POST"])
    @staff_required
    def admin_passages():
        selected_category = request.args.get("category") or Config.COURSE_CATEGORIES[0]
        with get_db() as db:
            if request.method == "POST":
                category = request.form.get("category", "").strip()
                practice_number = int(request.form.get("practice_number") or 1)
                title = request.form.get("title", "").strip()
                content_type = request.form.get("content_type", "paragraph").strip()
                target_wpm = int(request.form.get("target_wpm") or 30)
                target_strokes = int(request.form.get("target_strokes") or 600)
                passage_text = request.form.get("passage_text", "").strip()

                if not category or not title or not passage_text:
                    flash("Category, title, and passage text are required.", "danger")
                else:
                    existing = db.fetchone(
                        "SELECT id FROM practice_passages WHERE category = %s AND practice_number = %s",
                        (category, practice_number),
                    )
                    if existing:
                        db.execute(
                            """
                            UPDATE practice_passages
                            SET title=%s, content_type=%s, passage_text=%s, target_wpm=%s, target_strokes=%s
                            WHERE id=%s
                            """,
                            (
                                title,
                                content_type,
                                passage_text,
                                target_wpm,
                                target_strokes,
                                existing["id"],
                            ),
                        )
                        flash(f"Updated Practice {practice_number} for {category}.", "success")
                    else:
                        db.execute(
                            """
                            INSERT INTO practice_passages
                                (category, practice_number, title, content_type, passage_text, target_wpm, target_strokes)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                category,
                                practice_number,
                                title,
                                content_type,
                                passage_text,
                                target_wpm,
                                target_strokes,
                            ),
                        )
                        flash(f"Added Practice {practice_number} to {category}.", "success")
                    db.commit()
                return redirect(url_for("admin_passages", category=category))

            passages = db.fetchall(
                """
                SELECT * FROM practice_passages
                WHERE category = %s
                ORDER BY practice_number ASC
                """,
                (selected_category,),
            )
            next_practice_num = (
                max((p["practice_number"] for p in passages), default=0) + 1
            )

        return render_template(
            "admin/passages.html",
            passages=passages,
            selected_category=selected_category,
            next_practice_num=next_practice_num,
        )

    @app.route("/admin/passages/<int:passage_id>/delete", methods=["POST"])
    @staff_required
    def admin_passage_delete(passage_id):
        category = request.form.get("category") or Config.COURSE_CATEGORIES[0]
        with get_db() as db:
            db.execute("DELETE FROM practice_passages WHERE id = %s", (passage_id,))
            db.commit()
        flash("Practice passage removed.", "info")
        return redirect(url_for("admin_passages", category=category))

    @app.route("/admin/account", methods=["GET", "POST"])
    @staff_required
    def admin_account():
        with get_db() as db:
            current_staff = db.fetchone(
                "SELECT * FROM staff_users WHERE id = %s", (session["user_id"],)
            )
            if request.method == "POST":
                action = request.form.get("action", "update_self")

                if action == "update_self":
                    new_username = request.form.get("new_username", "").strip()
                    new_full_name = request.form.get("full_name", "").strip()
                    new_phone = request.form.get("phone", "").strip()
                    current_password = request.form.get("current_password", "")
                    new_password = request.form.get("new_password", "")
                    confirm_password = request.form.get("confirm_password", "")

                    if not check_password_hash(current_staff["password_hash"], current_password):
                        flash("Current password verification failed.", "danger")
                        return redirect(url_for("admin_account"))

                    if not new_username or not new_full_name:
                        flash("Login ID and Full Name cannot be empty.", "danger")
                        return redirect(url_for("admin_account"))

                    conflict = db.fetchone(
                        "SELECT id FROM staff_users WHERE username = %s AND id != %s",
                        (new_username, current_staff["id"]),
                    )
                    if conflict:
                        flash("That Login ID is already used by another staff member.", "danger")
                        return redirect(url_for("admin_account"))

                    pw_hash = current_staff["password_hash"]
                    if new_password:
                        if len(new_password) < 4:
                            flash("New password must be at least 4 characters.", "danger")
                            return redirect(url_for("admin_account"))
                        if new_password != confirm_password:
                            flash("New password and confirmation do not match.", "danger")
                            return redirect(url_for("admin_account"))
                        pw_hash = generate_password_hash(new_password)

                    db.execute(
                        """
                        UPDATE staff_users
                        SET username = %s, full_name = %s, phone = %s, password_hash = %s
                        WHERE id = %s
                        """,
                        (new_username, new_full_name, new_phone, pw_hash, current_staff["id"]),
                    )
                    db.commit()
                    session["username"] = new_username
                    session["full_name"] = new_full_name
                    flash("Admin Login ID and account credentials updated!", "success")
                    return redirect(url_for("admin_account"))

                if action == "add_staff":
                    username = request.form.get("staff_username", "").strip()
                    full_name = request.form.get("staff_full_name", "").strip()
                    phone = request.form.get("staff_phone", "").strip()
                    role = request.form.get("staff_role", "instructor").strip()
                    password = request.form.get("staff_password", "").strip()

                    if not username or not full_name or len(password) < 4:
                        flash("Enter staff Login ID, Name, and Password (min 4 chars).", "danger")
                    else:
                        dup = db.fetchone(
                            "SELECT id FROM staff_users WHERE username = %s", (username,)
                        )
                        if dup:
                            flash("Staff Login ID already exists.", "danger")
                        else:
                            db.execute(
                                """
                                INSERT INTO staff_users (username, full_name, role, password_hash, phone)
                                VALUES (%s, %s, %s, %s, %s)
                                """,
                                (
                                    username,
                                    full_name,
                                    role,
                                    generate_password_hash(password),
                                    phone,
                                ),
                            )
                            db.commit()
                            flash(f"Staff account '{username}' created.", "success")
                    return redirect(url_for("admin_account"))

            staff_list = db.fetchall(
                "SELECT id, username, full_name, role, phone, created_at FROM staff_users ORDER BY id ASC"
            )

        return render_template(
            "admin/account_settings.html",
            current_staff=current_staff,
            staff_list=staff_list,
        )

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=os.environ.get("FLASK_DEBUG", "1") == "1")
