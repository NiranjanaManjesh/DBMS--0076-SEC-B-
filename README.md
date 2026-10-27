# Student Record Management (Python + Tkinter + MySQL)

A small desktop application that stores student records in a MySQL database.
Supports Add, View, Search, Update and Delete, with input validation.

## Project structure
```
student_project/
├── app.py          # Application code (GUI + MySQL connection)
├── database.sql    # Database/table creation + sample data
├── README.md       # This file
└── screenshots/    # Add your screenshots here
```

## Setup
1. Install MySQL Server and make sure it is running.
2. Install the connector:
   ```
   pip install mysql-connector-python
   ```
3. Create the database and table:
   ```
   mysql -u root -p < database.sql
   ```
   (or paste database.sql into MySQL Workbench and run it)
4. Open `app.py` and set your MySQL password in `DB_CONFIG`.
5. Run:
   ```
   python app.py
   ```

## Database design
Table `students`: student_id (PK, auto increment), name, email (UNIQUE), course, semester (1-8).

## Testing checklist (take a screenshot of each)
| Test | Expected result |
|------|-----------------|
| Add a student in the app, then run `SELECT * FROM students;` in MySQL | New row visible in MySQL |
| Click "Show All" | All rows from MySQL listed in the table |
| Select a row, change course, click Update, check MySQL | Change reflected in MySQL |
| Select a row, click Delete, check MySQL | Row removed from MySQL |
| Leave a field blank / semester = 12 / email = "abc" | Warning message, nothing saved |
| Add the same email twice | "Duplicate" error shown |

## Report outline (2-4 pages)
1. Title, name, course, date
2. Objective and chosen application
3. Database design (table structure + the SQL from database.sql)
4. Screenshots: application interface, MySQL table, record added via app, record updated, record deleted
5. Conclusion
