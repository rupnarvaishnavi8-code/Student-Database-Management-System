import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database connection
con = sqlite3.connect("database.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT,
    marks REAL
)
""")
con.commit()

# Main window
root = tk.Tk()
root.title("Student Database Management System")
root.geometry("900x650")
root.configure(bg="#EAF2F8")

# Colors
BLUE = "#1565C0"
WHITE = "#FFFFFF"
DARK = "#17365D"

# Heading
header = tk.Frame(root, bg=BLUE, height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="STUDENT DATABASE MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold"),
    bg=BLUE,
    fg=WHITE
).pack(pady=22)

# Input section
form = tk.Frame(root, bg=WHITE, padx=20, pady=15)
form.pack(padx=25, pady=15, fill="x")

labels = ["Roll Number", "Name", "Age", "Course", "Marks"]
entries = []

for i, label in enumerate(labels):
    tk.Label(
        form,
        text=label,
        bg=WHITE,
        fg=DARK,
        font=("Arial", 10, "bold")
    ).grid(row=i, column=0, sticky="w", pady=5)

    entry = tk.Entry(form, width=35, font=("Arial", 10))
    entry.grid(row=i, column=1, padx=15, pady=5)
    entries.append(entry)

e1, e2, e3, e4, e5 = entries


# Clear input boxes
def clear_fields():
    for entry in entries:
        entry.delete(0, tk.END)


# Display student records
def view_students():
    for item in table.get_children():
        table.delete(item)

    cur.execute("SELECT * FROM students ORDER BY roll")

    for row in cur.fetchall():
        table.insert("", tk.END, values=row)


# Read and validate details
def get_details():
    try:
        roll = int(e1.get())
        name = e2.get().strip()
        age = int(e3.get())
        course = e4.get().strip()
        marks = float(e5.get())

        if roll <= 0 or not name or not course or age <= 0:
            raise ValueError

        if not 0 <= marks <= 100:
            raise ValueError

        return roll, name, age, course, marks

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter valid details and marks between 0 and 100."
        )
        return None


# Add student
def add_student():
    data = get_details()

    if data is None:
        return

    try:
        cur.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
            data
        )
        con.commit()

        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()
        view_students()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists.")


# Search student
def search_student():
    try:
        roll = int(e1.get())

        cur.execute(
            "SELECT * FROM students WHERE roll = ?",
            (roll,)
        )
        row = cur.fetchone()

        if row:
            clear_fields()

            for entry, value in zip(entries, row):
                entry.insert(0, str(value))

            for item in table.get_children():
                table.delete(item)

            table.insert("", tk.END, values=row)

        else:
            messagebox.showinfo("Result", "Student not found.")

    except ValueError:
        messagebox.showerror("Error", "Enter a valid roll number.")


# Update student
def update_student():
    data = get_details()

    if data is None:
        return

    cur.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?, marks = ?
        WHERE roll = ?
    """, (data[1], data[2], data[3], data[4], data[0]))

    con.commit()

    if cur.rowcount > 0:
        messagebox.showinfo("Success", "Student updated successfully!")
    else:
        messagebox.showinfo("Result", "Student not found.")

    clear_fields()
    view_students()


# Delete student
def delete_student():
    try:
        roll = int(e1.get())

        if not messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?"
        ):
            return

        cur.execute(
            "DELETE FROM students WHERE roll = ?",
            (roll,)
        )
        con.commit()

        if cur.rowcount > 0:
            messagebox.showinfo("Success", "Student deleted.")
        else:
            messagebox.showinfo("Result", "Student not found.")

        clear_fields()
        view_students()

    except ValueError:
        messagebox.showerror("Error", "Enter a valid roll number.")


# Buttons
button_frame = tk.Frame(root, bg="#EAF2F8")
button_frame.pack(pady=5)

buttons = [
    ("Add Student", add_student),
    ("View Students", view_students),
    ("Search Student", search_student),
    ("Update Student", update_student),
    ("Delete Student", delete_student),
    ("Clear Fields", clear_fields)
]

for i, (text, command) in enumerate(buttons):
    tk.Button(
        button_frame,
        text=text,
        command=command,
        bg=BLUE,
        fg=WHITE,
        activebackground="#0D47A1",
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        width=15,
        relief="flat",
        cursor="hand2"
    ).grid(
        row=i // 3,
        column=i % 3,
        padx=6,
        pady=5
    )


# Student table
table_frame = tk.Frame(root, bg=WHITE)
table_frame.pack(padx=25, pady=15, fill="both", expand=True)

columns = ("roll", "name", "age", "course", "marks")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

headings = {
    "roll": "Roll Number",
    "name": "Name",
    "age": "Age",
    "course": "Course",
    "marks": "Marks"
}

for col, heading in headings.items():
    table.heading(col, text=heading)
    table.column(col, width=140, anchor="center")

table.pack(fill="both", expand=True)

# Table design
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview.Heading",
    background=BLUE,
    foreground=WHITE,
    font=("Arial", 10, "bold")
)

style.configure(
    "Treeview",
    rowheight=28,
    font=("Arial", 10),
    background=WHITE,
    fieldbackground=WHITE
)

# Display existing records
view_students()


# Close application
def close_app():
    con.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_app)

# Start application
root.mainloop()