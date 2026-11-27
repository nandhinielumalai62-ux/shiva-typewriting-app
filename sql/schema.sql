-- Shiva Commercial Institute - MySQL 8.0 Schema
CREATE DATABASE IF NOT EXISTS shiva_typewriting_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE shiva_typewriting_db;

CREATE TABLE IF NOT EXISTS staff_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'admin',
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS institute_counters (
    counter_key VARCHAR(64) PRIMARY KEY,
    last_number INT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_code VARCHAR(24) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    father_guardian_name VARCHAR(120) NOT NULL,
    guardian_occupation VARCHAR(100) DEFAULT '',
    gender VARCHAR(20) NOT NULL,
    dob DATE NOT NULL,
    qualification VARCHAR(100) NOT NULL,
    school_college VARCHAR(150) DEFAULT '',
    phone VARCHAR(20) NOT NULL,
    alt_phone VARCHAR(20) DEFAULT '',
    email VARCHAR(120) DEFAULT '',
    address TEXT NOT NULL,
    city VARCHAR(80) DEFAULT '',
    pincode VARCHAR(12) DEFAULT '',
    aadhaar_no VARCHAR(24) DEFAULT '',
    course_category VARCHAR(64) NOT NULL,
    batch_timing VARCHAR(40) NOT NULL,
    machine_no VARCHAR(24) DEFAULT '',
    admission_date DATE NOT NULL,
    admission_fee DECIMAL(10,2) NOT NULL DEFAULT 200.00,
    monthly_fee DECIMAL(10,2) NOT NULL DEFAULT 500.00,
    fee_due_day INT NOT NULL DEFAULT 10,
    photo_filename VARCHAR(255) DEFAULT '',
    password_hash VARCHAR(255) NOT NULL,
    status VARCHAR(24) NOT NULL DEFAULT 'Active',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    login_time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Present',
    marked_by VARCHAR(32) NOT NULL DEFAULT 'AUTO_LOGIN',
    practice_category VARCHAR(64) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_student_date (student_id, attendance_date),
    CONSTRAINT fk_attendance_student FOREIGN KEY (student_id)
        REFERENCES students(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fee_payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    billing_month CHAR(7) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL,
    paid_date DATE NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    payment_mode VARCHAR(32) DEFAULT '',
    receipt_no VARCHAR(40) DEFAULT '',
    intimation_note VARCHAR(255) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_student_month (student_id, billing_month),
    CONSTRAINT fk_fee_student FOREIGN KEY (student_id)
        REFERENCES students(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS practice_passages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(64) NOT NULL,
    practice_number INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    content_type VARCHAR(20) NOT NULL DEFAULT 'paragraph',
    passage_text LONGTEXT NOT NULL,
    target_wpm INT NOT NULL DEFAULT 30,
    target_strokes INT NOT NULL DEFAULT 600,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_cat_practice (category, practice_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS practice_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    category VARCHAR(64) NOT NULL,
    practice_number INT NOT NULL DEFAULT 1,
    content_type VARCHAR(20) NOT NULL DEFAULT 'paragraph',
    duration_sec INT NOT NULL DEFAULT 0,
    strokes INT NOT NULL DEFAULT 0,
    wpm INT NOT NULL DEFAULT 0,
    accuracy_pct INT NOT NULL DEFAULT 100,
    errors INT NOT NULL DEFAULT 0,
    weak_chars VARCHAR(255) DEFAULT '',
    target_met TINYINT(1) NOT NULL DEFAULT 0,
    practiced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_session_student FOREIGN KEY (student_id)
        REFERENCES students(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
