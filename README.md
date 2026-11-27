# Shiva Commercial Institute — Typewriting Practice & Management System

A full-stack **HTML, CSS, Bootstrap 5, JavaScript, Python (Flask), and MySQL** web application for a Tamil & English Typewriting Institute.

## Features
- **Bold High-Contrast UI & `14px` Paragraph Typography**: Clear high-visibility interface with `14px` paragraph and passage text (`Noto Sans Tamil` + clean UI fonts).
- **Separate Staff/Admin & Student Portals**:
  - **Admin / Staff Self-Service Credentials**: Admin can update their own Login ID (`username`) and Password at `/admin/account` and add staff accounts.
  - **Sequential Auto-Generated Student IDs**: Every admitted student automatically gets the next ID in order (`SCI001`, `SCI002`, `SCI003`, ...).
  - **Student Self-Service Password Change**: Students can change their password anytime inside `/student/change-password`.
- **Admission Form with Edit & Delete**:
  - Printable commercial typewriting institute admission form (`/admin/admission`) with photo upload, personal/family details, course & batch selection, fee settings, and instant **Edit** & **Delete** options if any detail was entered wrong.
- **Automatic Attendance on Login**:
  - Logging into the Student Portal automatically records today's attendance (`Present` + login timestamp).
- **Monthly Fee Intimation & Automatic Login Block**:
  - Shows Monthly Fee Intimation notices before the due date.
  - Automatically blocks student login access if monthly fee payment is delayed past the due date (attendance is not marked when blocked), and immediately restores access once Staff marks the fee Paid.
- **10-Minute Timed Practice Arena Across All 6 Categories**:
  1. `Junior English Basic`
  2. `Junior English Speed`
  3. `Senior English Speed`
  4. `Junior Tamil Basic`
  5. `Junior Tamil Speed`
  6. `Senior Tamil Speed`
  - Includes numbered sessions (**Practice 1, Practice 2, Practice 3, ...**), live WPM, Accuracy %, Errors, Strokes, Progress %, Weak Keys detection, and automatic submission at **10:00**.

## Setup (MySQL + Flask)
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure MySQL credentials:
   Copy `.env.example` to `.env` and update `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_DATABASE`.
3. Initialize the MySQL schema (`sql/schema.sql`) and seed Practice 1..N lessons + default Admin:
   ```bash
   python setup_mysql.py
   ```
4. Run the Flask server:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.
   - Default Admin Login ID: `admin` | Password: `admin123`
