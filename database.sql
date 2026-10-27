-- Student Record Management - MySQL schema and sample data
CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(50)  NOT NULL,
    email      VARCHAR(100) NOT NULL UNIQUE,
    course     VARCHAR(50)  NOT NULL,
    semester   INT          NOT NULL CHECK (semester BETWEEN 1 AND 8)
);

-- Sample data
INSERT INTO students (name, email, course, semester) VALUES
('Aarav Sharma', 'aarav@example.com', 'BCA', 3),
('Meera Nair',   'meera@example.com', 'B.Sc Criminology', 5),
('Rohan Das',    'rohan@example.com', 'BBA', 2);
