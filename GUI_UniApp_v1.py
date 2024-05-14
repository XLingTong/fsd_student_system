import tkinter as tk
from tkinter import messagebox
import json
import re
import random

class Subject:
    def __init__(self, name):
        self.id = name
        self.name = name
        self.mark = random.randint(25, 100)
        self.grade = self.assign_grade(self.mark)

    @staticmethod
    def assign_grade(mark):
        if mark >= 90:
            return 'A'
        elif mark >= 80:
            return 'B'
        elif mark >= 70:
            return 'C'
        elif mark >= 60:
            return 'D'
        elif mark >= 50:
            return 'E'
        else:
            return 'F'

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CLIUniApp")
        self.root.geometry("430x430")
        self.root.configure(bg="#eeba30")
        self.current_student = None

        self.login_window()

    def login_window(self):
        self.clear_window()

        box = tk.LabelFrame(self.root, text='SIGN IN', bg="#eeba30", fg='#372e29', padx=20, pady=20, font='Helvetica 12 bold')
        box.columnconfigure(0, weight=1)
        box.columnconfigure (1, weight=3)
        box.place(rely=0.5, relx=0.5, anchor='center')

        emailLbl = tk.Label(box, text="Email:", justify='left', fg='#372e29', font='Helvetica 12 bold', bg='#eeba30')
        emailLbl.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        passwordLbl = tk.Label(box, text="Password:", fg='#372e29', font='Helvetica 12 bold', bg='#eeba30')
        passwordLbl.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        self.emailText = tk.StringVar()
        self.emailField = tk.Entry(box, textvariable=self.emailText)
        self.emailField.grid(column=1, row=0, padx=5, pady=5)
        self.emailField.focus()

        self.passwordTxt = tk.StringVar()
        self.passwordField = tk.Entry(box, textvariable=self.passwordTxt, show="*")
        self.passwordField.grid(column=1, row=1, padx=5, pady=5)

        loginBtn = tk.Button(box, text='Login', command=self.login)
        loginBtn.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

        cancelBtn = tk.Button(box, text='Cancel')
        cancelBtn.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

    def login(self):
        email = self.emailField.get()
        password = self.passwordField.get()

        if not self.student_exists(email):  # Check if student exists
            messagebox.showerror("Error", "Invalid login credentials.")
            return

        with open("students.data", "r") as file:
            students = json.load(file)

        student = next((s for s in students if s['email'] == email and s['password'] == password), None)  # Find student by email and password

        if student:
            self.current_student = student
            self.enrollment_window()
        else:
            messagebox.showerror("Error", "Invalid login credentials.")

    def student_exists(self, email):
        try:
            with open("students.data", "r") as file:
                students = json.load(file)
            return any(student['email'] == email for student in students)  # Check if any student has the same email
        except (json.JSONDecodeError, FileNotFoundError):
            return False

    def enrollment_window(self):
        self.clear_window()

        self.subject_label = tk.Label(self.root, text="Subject Name:", bg="#eeba30")
        self.subject_label.grid(row=0, column=0, pady=5)
        self.subject_entry = tk.Entry(self.root)
        self.subject_entry.grid(row=0, column=1, pady=5)

        button_box = tk.Frame(self.root, bg="#eeba30")  # Create a box to contain the buttons
        button_box.grid(row=1, column=0, columnspan=2, pady=10)

        self.enroll_button = tk.Button(button_box, text="Enroll", command=self.enroll_subject, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
        self.enroll_button.pack(side="left", padx=5)

        self.show_subjects_button = tk.Button(button_box, text="Show Enrolled Subjects", command=self.show_subjects, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
        self.show_subjects_button.pack(side="left", padx=5)

        self.logout_button = tk.Button(button_box, text="Logout", command=self.logout, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
        self.logout_button.pack(side="left", padx=5)

    def enroll_subject(self):
        subject_name = self.subject_entry.get()

        if not subject_name:
            messagebox.showerror("Error", "Please enter a subject name.")
            return

        subject = Subject(subject_name)

        if 'subjects' not in self.current_student:
            self.current_student['subjects'] = []

        self.current_student['subjects'].append(subject.__dict__)

        with open("students.data", "w") as file:
            json.dump(self.current_student, file)

        messagebox.showinfo("Success", f"Subject '{subject_name}' enrolled successfully.")

    def show_subjects(self):
        self.clear_window()

        subjects = self.current_student.get('subjects', [])

        if not subjects:
            messagebox.showinfo("Information", "No subjects enrolled.")
            return

        subject_list = tk.Listbox(self.root, width=40)
        subject_list.pack(pady=30)

        for subject in subjects:
            subject_list.insert(tk.END, f"Subject: {subject['name']}\nMark: {subject['mark']}\nGrade: {subject['grade']}\n")

    def logout(self):
        self.current_student = None
        self.login_window()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


app = App()
app.run()
