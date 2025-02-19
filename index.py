import random
import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog

# Database Connection
con = mysql.connector.connect(host="localhost", user="root", password="Da882601")
cur = con.cursor()
cur.execute("drop database if exists timetable")
cur.execute("create database if not exists timetable")
cur.execute("use timetable")
con.commit()

# GUI Window Setup
root = tk.Tk()
root.title("Timetable Generator")
root.geometry("500x400")

def get_user_input():
    global periods, days, classes, subjects, subjects2, classs
    
    periods = simpledialog.askinteger("Input", "Enter the number of periods:", parent=root)
    days = simpledialog.askinteger("Input", "Enter the number of days:", parent=root)
    
    subjectT = simpledialog.askstring("Input", "Enter the theory subjects separated by commas:", parent=root).split(',')
    subjectL = simpledialog.askstring("Input", "Enter the practical subjects separated by commas:", parent=root).split(',')
    
    subjects = [sub.strip() for sub in subjectT]
    subjects2 = subjects + [sub.strip() for sub in subjectL]
    
    classes = simpledialog.askinteger("Input", "Enter the number of classes:", parent=root)
    classs = ["Class " + str(i) for i in range(1, classes + 1)]
    messagebox.showinfo("Info", "User inputs recorded successfully!")

def assign_teachers():
    global assigned_teachers
    assigned_teachers = {}
    subject_teachers = {}
    
    for subject in subjects2:
        if subject:
            teachers = simpledialog.askstring("Input", f"Enter teachers for {subject} separated by commas:", parent=root).split(',')
            subject_teachers[subject] = [t.strip() for t in teachers]
    
    for cls in classs:
        assigned_teachers[cls] = {}
        for subject, teachers in subject_teachers.items():
            assigned_teachers[cls][subject] = random.choice(teachers)
    
    messagebox.showinfo("Info", "Teachers assigned successfully!")

def create_tables():
    for k in range(1, classes + 1):
        cur.execute(f"CREATE TABLE class{k} (DAY VARCHAR(244))")
        for i in range(1, days + 1):
            cur.execute(f"INSERT INTO class{k} VALUES ('day{i}')")
            con.commit()
        for i in range(1, periods + 1):
            cur.execute(f"ALTER TABLE class{k} ADD period{i} VARCHAR(244)")
            con.commit()
    messagebox.showinfo("Info", "Database tables created successfully!")

def generate_timetable():
    for i in range(1, classes + 1):
        for j in range(1, days + 1):
            available_subjects = list(subjects2)
            for k in range(1, periods + 1):
                if available_subjects:
                    subject = random.choice(available_subjects)
                    teacher = assigned_teachers[f"Class {i}"][subject]
                    cur.execute(f"UPDATE class{i} SET period{k}='{subject} {teacher}' WHERE DAY='day{j}'")
                    con.commit()
                    available_subjects.remove(subject)
    messagebox.showinfo("Info", "Timetable generated successfully! Open MySQL to view it.")

# GUI Buttons
tk.Button(root, text="Enter User Data", command=get_user_input).pack(pady=10)
tk.Button(root, text="Assign Teachers", command=assign_teachers).pack(pady=10)
tk.Button(root, text="Create Tables", command=create_tables).pack(pady=10)
tk.Button(root, text="Generate Timetable", command=generate_timetable).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()
