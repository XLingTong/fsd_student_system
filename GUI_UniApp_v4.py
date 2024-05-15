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
        self.root.geometry("430x860")
        self.root.configure(bg="#eeba30")
        self.current_student = None

        self.login_window()

    def login_window(self):
        self.clear_window()
        
        box = tk.LabelFrame(self.root, text='SIGN IN', bg="#eeba30", fg='#372e29', padx=20, pady=20, font='Helvetica 12 bold')
        box.columnconfigure(0, weight=1)
        box.columnconfigure(1, weight=3)
        box.place(rely=0.5, relx=0.5, anchor='center')

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

        if not self.student_exists(email):  # Call the student_exists function as an instance method
            messagebox.showerror("Error", "Invalid login credentials.")
            return

        with open("students.data", "r") as file:
            students = json.load(file)

        student = next((s for s in students if s['email'] == email and s['password'] == password), None)  # Find student by email and password

        if student:
            self.current_student = student
            self.home_window()
        else:
            messagebox.showerror("Error", "Invalid login credentials.")

    def student_exists(self, email):
        try:
            with open("students.data", "r") as file:
                students = json.load(file)
            for student in students:
                if isinstance(student, dict) and student.get('email') == email:
                    return True
            return False
        except (json.JSONDecodeError, FileNotFoundError):
            return False
    
    def home_window(self):
            self.clear_window()

            welcome_label = tk.Label(self.root, text="Welcome to UniApp", bg="#eeba30", fg='#372e29', font='Helvetica 16 bold')
            welcome_label.pack(pady=20)

            select_label = tk.Label(self.root, text="Please select:", bg="#eeba30", fg='#372e29', font='Helvetica 14')
            select_label.pack(pady=10)

            button_box = tk.Frame(self.root, bg="#eeba30")
            button_box.pack(pady=20)

            enroll_button = tk.Button(button_box, text="Enroll", command=self.enrollment_window, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
            enroll_button.pack(side="top", pady=5)

            show_subjects_button = tk.Button(button_box, text="Show Enrollments", command=self.show_subjects, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
            show_subjects_button.pack(side="top", pady=5)

            logout_button = tk.Button(button_box, text="Logout", command=self.logout, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
            logout_button.pack(side="top", pady=5)

    def enrollment_window(self):
        self.clear_window()

        subject_name_label = tk.Label(self.root, text="Please enter the subject you want to enroll", bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
        subject_name_label.pack(pady=20)

        subject_name_frame = tk.Frame(self.root, bg="#eeba30")
        subject_name_frame.pack(pady=10)

        self.subject_entry = tk.Entry(subject_name_frame)
        self.subject_entry.pack(side="left", padx=5)

        button_box = tk.Frame(self.root, bg="#eeba30")
        button_box.pack(pady=20)

        enroll_button = tk.Button(button_box, text="Enroll", command=self.enroll_subject, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
        enroll_button.pack(side="left", padx=5)

        cancel_button = tk.Button(button_box, text="Cancel", command=self.clear_subject_entry, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
        cancel_button.pack(side="left", padx=5)

        back_to_home_button = tk.Button(button_box, text="Back to Home", command=self.home_window, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
        back_to_home_button.pack(side="left", padx=5)

    def clear_subject_entry(self):
            self.subject_entry.delete(0, tk.END)

    def enroll_subject(self):
        subject_name = self.subject_entry.get()

        if not subject_name:
            messagebox.showerror("Error", "Please enter a subject name.")
            return

        subject = Subject(subject_name)

        if 'subjects' not in self.current_student:
            self.current_student['subjects'] = []

        if len(self.current_student['subjects']) >= 4:
        # Check if the maximum number of subjects has been reached
            messagebox.showerror("Error", "Cannot enroll in more than 4 subjects.")
            return

        self.current_student['subjects'].append(subject.__dict__)

        with open("students.data", "w") as file:
            json.dump(self.current_student, file)

        messagebox.showinfo("Success", f"Subject '{subject_name}' enrolled successfully.")

    def show_subjects(self):
        self.clear_window()

        subjects = self.current_student.get('subjects', [])

        if not subjects:
            response = messagebox.askokcancel("Information", "No subjects enrolled. Do you want to enroll a subject?")
            if response:
            # Go back to the enroll subject window
                self.enrollment_window()
            else:
                self.enrollment_window()
            return

        subject_list = tk.Listbox(self.root, width=40)
        subject_list.pack(pady=30)

        for subject in subjects:
            subject_text = f"Subject: {subject['name']}"
            mark_text = f"Mark: {subject['mark']}"
            grade_text = f"Grade: {subject['grade']}"

            subject_label = tk.Label(subject_list, text=subject_text, anchor="w")
            subject_label.pack(fill=tk.X, expand=True)

            mark_label = tk.Label(subject_list, text=mark_text, anchor="w")
            mark_label.pack(fill=tk.X, expand=True)

            grade_label = tk.Label(subject_list, text=grade_text, anchor="w")
            grade_label.pack(fill=tk.X, expand=True)

            subject_list.pack(fill=tk.BOTH, expand=True)

        back_button = tk.Button(self.root, text="Back to Home", command=self.home_window, bg="#eeba30", fg='#372e29', font='Helvetica 12 bold')
        back_button.pack(pady=20)
  
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
