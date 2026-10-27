"""Student Record Management - Tkinter GUI + MySQL (CRUD)."""
import re
import tkinter as tk
from tkinter import ttk, messagebox

import mysql.connector
from mysql.connector import Error, IntegrityError

# ---- Change these to match your MySQL setup ----
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "nira",
    "database": "student_db",
}
# -------------------------------------------------

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def run_query(sql, params=(), fetch=False):
    """Run a query and return rows if fetch=True. Each call uses a fresh connection."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        if fetch:
            return cur.fetchall()
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


class StudentApp:
    def __init__(self, root):
        self.root = root
        root.title("Student Record Management")
        root.geometry("760x520")

        self.selected_id = None
        self.vars = {k: tk.StringVar() for k in ("name", "email", "course", "semester")}
        self.search_var = tk.StringVar()

        self.build_form()
        self.build_table()
        self.load_students()

    # ---------- UI ----------
    def build_form(self):
        form = ttk.LabelFrame(self.root, text="Student Details", padding=10)
        form.pack(fill="x", padx=10, pady=8)

        labels = [("Name", "name"), ("Email", "email"),
                  ("Course", "course"), ("Semester (1-8)", "semester")]
        for i, (text, key) in enumerate(labels):
            ttk.Label(form, text=text).grid(row=i // 2, column=(i % 2) * 2, sticky="w", padx=5, pady=4)
            ttk.Entry(form, textvariable=self.vars[key], width=28).grid(
                row=i // 2, column=(i % 2) * 2 + 1, padx=5, pady=4)

        btns = ttk.Frame(form)
        btns.grid(row=2, column=0, columnspan=4, pady=8)
        for text, cmd in [("Add", self.add_student), ("Update", self.update_student),
                          ("Delete", self.delete_student), ("Clear", self.clear_form)]:
            ttk.Button(btns, text=text, command=cmd, width=12).pack(side="left", padx=5)

    def build_table(self):
        search = ttk.Frame(self.root)
        search.pack(fill="x", padx=10)
        ttk.Label(search, text="Search (name/course):").pack(side="left")
        ttk.Entry(search, textvariable=self.search_var, width=25).pack(side="left", padx=5)
        ttk.Button(search, text="Search", command=self.load_students).pack(side="left")
        ttk.Button(search, text="Show All", command=self.show_all).pack(side="left", padx=5)

        cols = ("ID", "Name", "Email", "Course", "Semester")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=12)
        for c, w in zip(cols, (50, 160, 220, 150, 80)):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w)
        self.tree.pack(fill="both", expand=True, padx=10, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # ---------- Helpers ----------
    def validate(self):
        name = self.vars["name"].get().strip()
        email = self.vars["email"].get().strip()
        course = self.vars["course"].get().strip()
        sem = self.vars["semester"].get().strip()

        if not (name and email and course and sem):
            messagebox.showwarning("Invalid input", "All fields are required.")
            return None
        if not EMAIL_RE.match(email):
            messagebox.showwarning("Invalid input", "Enter a valid email address.")
            return None
        if not sem.isdigit() or not 1 <= int(sem) <= 8:
            messagebox.showwarning("Invalid input", "Semester must be a number from 1 to 8.")
            return None
        return name, email, course, int(sem)

    def clear_form(self):
        for v in self.vars.values():
            v.set("")
        self.selected_id = None
        self.tree.selection_remove(self.tree.selection())

    def show_all(self):
        self.search_var.set("")
        self.load_students()

    def on_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        sid, name, email, course, sem = self.tree.item(sel[0])["values"]
        self.selected_id = sid
        self.vars["name"].set(name)
        self.vars["email"].set(email)
        self.vars["course"].set(course)
        self.vars["semester"].set(sem)

    # ---------- CRUD ----------
    def load_students(self):  # SELECT
        try:
            term = self.search_var.get().strip()
            if term:
                like = f"%{term}%"
                rows = run_query(
                    "SELECT student_id, name, email, course, semester FROM students "
                    "WHERE name LIKE %s OR course LIKE %s ORDER BY student_id",
                    (like, like), fetch=True)
            else:
                rows = run_query(
                    "SELECT student_id, name, email, course, semester FROM students "
                    "ORDER BY student_id", fetch=True)
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert("", "end", values=r)
        except Error as e:
            messagebox.showerror("Database error", str(e))

    def add_student(self):  # INSERT
        data = self.validate()
        if not data:
            return
        try:
            run_query("INSERT INTO students (name, email, course, semester) "
                      "VALUES (%s, %s, %s, %s)", data)
            messagebox.showinfo("Success", "Student added.")
            self.clear_form()
            self.load_students()
        except IntegrityError:
            messagebox.showerror("Duplicate", "A student with this email already exists.")
        except Error as e:
            messagebox.showerror("Database error", str(e))

    def update_student(self):  # UPDATE
        if self.selected_id is None:
            messagebox.showwarning("Select a record", "Click a student in the table first.")
            return
        data = self.validate()
        if not data:
            return
        try:
            run_query("UPDATE students SET name=%s, email=%s, course=%s, semester=%s "
                      "WHERE student_id=%s", data + (self.selected_id,))
            messagebox.showinfo("Success", "Student updated.")
            self.clear_form()
            self.load_students()
        except IntegrityError:
            messagebox.showerror("Duplicate", "Another student already uses this email.")
        except Error as e:
            messagebox.showerror("Database error", str(e))

    def delete_student(self):  # DELETE
        if self.selected_id is None:
            messagebox.showwarning("Select a record", "Click a student in the table first.")
            return
        if not messagebox.askyesno("Confirm", "Delete this student permanently?"):
            return
        try:
            run_query("DELETE FROM students WHERE student_id=%s", (self.selected_id,))
            messagebox.showinfo("Success", "Student deleted.")
            self.clear_form()
            self.load_students()
        except Error as e:
            messagebox.showerror("Database error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    StudentApp(root)
    root.mainloop()
