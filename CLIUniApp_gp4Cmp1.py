import json
import os
import re
import random
from pathlib import Path

class Subject:
    def __init__(self, name, id=None, mark=None, grade=None):
        self.id = id if id is not None else str(random.randint(1, 999)).zfill(3)
        self.name = name
        self.mark = mark if mark is not None else random.randint(25, 100)
        self.grade = grade if grade is not None else self.assign_grade(self.mark)

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mark': self.mark,
            'grade': self.grade
        }

class Student:
    def __init__(self, id=None, name=None, email=None, password=None, subjects=None):
        self.id = id if id is not None else str(random.randint(1, 999999)).zfill(6)
        self.name = name
        self.email = email
        self.password = password
        self.subjects = [Subject(**subj) for subj in subjects] if subjects else []

    def enroll_subject(self, subject_name):
        if len(self.subjects) >= 4:
            print("\033[91mCannot enroll in more than 4 subjects.\033[0m")
            return

        if any(subject.name == subject_name for subject in self.subjects):
            print("\033[91mSubject already enrolled.\033[0m")
            return

        subject = Subject(name=subject_name)
        self.subjects.append(subject)
        print("\033[93mSubject enrolled successfully.\033[0m")
        print(f"\033[93mYou are now enrolled in {len(self.subjects)} out of 4 subjects.\033[0m")

    def remove_subject(self, subject_id):
        if any(subject.id == subject_id for subject in self.subjects):
            self.subjects = [subject for subject in self.subjects if subject.id != subject_id]
            print("\033[93mSubject removed successfully.\033[0m")
        else:
            print("\033[91mSubject not found.\033[0m")

    def show_subjects(self):
        if not self.subjects:
            print("\033[91mNo subjects enrolled.\033[0m")
            return
        print(f"\033[93mShowing {len(self.subjects)} subjects\033[0m")
        for subject in self.subjects:
            print(f"Subject ID: {subject.id}, Name: {subject.name}, Mark: {subject.mark:.2f}, Grade: {subject.grade}")

    def change_password(self, new_password):
        # Check new password format
        if not validate_password(new_password):
            print("\033[91mInvalid password format, please try again.\033[0m")
            return

        # Confirm new password
        confirm_password = input("Confirm new password: ")
        if confirm_password != new_password:
            print("\033[91mPassword does not match. Please try again.\033[0m")
            return

        # Update password
        self.password = new_password
        print("\033[93mPassword updated successfully.\033[0m")

    
    def calculate_average_mark(self):
        if not self.subjects:
            return 0
        return sum(subject.mark for subject in self.subjects) / len(self.subjects)

    def is_passing(self):
        return self.calculate_average_mark() >= 50

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'subjects': [subject.to_dict() for subject in self.subjects]
        }

class Database:
    @staticmethod
    def load_students():
        if not os.path.exists("students.data") or os.path.getsize("students.data") == 0:
            return []
        try:
            with open("students.data", "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading students data: {e}")
            return []

    @staticmethod
    def save_students(students):
        with open("students.data", "w") as file:
            json.dump(students, file, indent=4)

    @staticmethod
    def clear_database():
        confirmation = input("\033[91mAre you sure you want to clear the database (YES)/(NO): \033[0m").upper()
        if confirmation == 'YES':
            open("students.data", 'w').close()
            print("\033[93mStudents data cleared.\033[0m")
        else:
            print("\033[93mDatabase clearing canceled.\033[0m")

def register_student():
    print("\033[38;2;0;128;0mStudent Sign up\033[0m")
    email = input("Enter email: ")
    if not validate_email(email):
        print("\033[38;2;255;0;0mInvalid email format.\033[0m")
        return
    password = input("Enter password: ")
    if not validate_password(password):
        print("\033[38;2;255;0;0mInvalid password format.\033[0m")
        return
    students = Database.load_students()
    if any(student['email'] == email for student in students):
        print("\033[38;2;255;0;0mStudent already registered.\033[0m")
        return

    name = input("Enter your name: ")
    student = Student(name=name, email=email, password=password)
    students.append(student.to_dict())
    Database.save_students(students)
    print("\033[38;2;255;255;0mStudent registered successfully.\033[0m")

def update_student_data(student):
    with open("students.data", "r") as file:
        students = json.load(file)
    updated_students = [s if s['id'] != student['id'] else student.to_dict() for s in students]
    with open("students.data", "w") as file:
        json.dump(updated_students, file, indent=4)

def validate_email(email):
    return re.match(r"[^@]+@university.com", email) is not None

def validate_password(password):
    pattern = r"^[A-Z][a-zA-Z]{5,}[0-9]{3,}$"
    match = re.match(pattern, password)
    if match:
        return True
    else:
        print("\033[91mPassword format is invalid.\033[0m")
        if not re.match(r"^[A-Z]", password):
            print("\033[91mPassword does not start with an uppercase letter.\033[0m")
        if not re.match(r"^[A-Z][a-zA-Z]{5,}", password):
            print("\033[91mPassword does not have at least 5 letters after the initial uppercase letter.\033[0m")
        if not re.match(r"^[A-Z][a-zA-Z]{5,}[0-9]{3,}$", password):
            print("\033[91mPassword does not end with at least 3 digits.\033[0m")
        return False

def login_student():
    print("\033[92mStudent Log in\033[0m")
    email = input("Enter your email: ")
    if not validate_email(email):
        print("\033[38;2;255;0;0mInvalid email format.\033[0m")
        return
    password = input("Enter your password: ")
    if not validate_password(password):
        print("\033[38;2;255;0;0mInvalid password format.\033[0m")
        return

    students = Database.load_students()
    student_data = next((student for student in students if student['email'] == email and student['password'] == password), None)
    if not student_data:
        print("\033[38;2;255;255;0mEmail and password formats acceptable.\033[0m")
        print("\033[91mStudent does not exist.\033[0m")
        return
    student = Student(**student_data)
    student_course_menu(student, students)

def student_course_menu(student, students):
    while True:
        print("\033[38;2;0;206;209mStudent Course Menu\033[0m")
        print("\033[38;2;0;206;209m(C) Change Password\033[0m")
        print("\033[38;2;0;206;209m(E) Enroll in a Subject\033[0m")
        print("\033[38;2;0;206;209m(R) Remove a Subject\033[0m")
        print("\033[38;2;0;206;209m(S) Show Enrolled Subjects\033[0m")
        print("\033[38;2;0;206;209m(X) Exit\033[0m")
        choice = input("\033[38;2;0;206;209mEnter your choice (C, E, R, S, X): \033[0m").upper()

        if choice == 'C':
            new_password = input("Enter new password: ")
            if validate_password(new_password):
                student.change_password(new_password)
                Database.save_students([s if s['id'] != student.id else student.to_dict() for s in students])
        elif choice == 'E':
            subject_name = input("Enter subject name: ")
            student.enroll_subject(subject_name)
            Database.save_students([s if s['id'] != student.id else student.to_dict() for s in students])
        elif choice == 'R':
            subject_id = input("Enter subject ID to remove: ")
            student.remove_subject(subject_id)
            Database.save_students([s if s['id'] != student.id else student.to_dict() for s in students])
        elif choice == 'S':
            student.show_subjects()
        elif choice == 'X':
            print("\033[93mExiting Student Course Menu.\033[0m")
            break
        else:
            print("\033[91mInvalid choice. Please try again.\033[0m")

def admin_menu():
    while True:
        print("\033[38;2;0;206;209mAdmin Menu\033[0m")
        print("\033[38;2;0;206;209m(C) Clear Database\033[0m")
        print("\033[38;2;0;206;209m(G) Group Students\033[0m")
        print("\033[38;2;0;206;209m(P) Partition Students\033[0m")
        print("\033[38;2;0;206;209m(R) Remove a Student\033[0m")
        print("\033[38;2;0;206;209m(S) Show Students\033[0m")
        print("\033[38;2;0;206;209m(X) Exit\033[0m")
        choice = input("\033[38;2;0;206;209mEnter your choice (C, G, P, R, S, X): \033[0m").upper()
        if choice == 'C':
            Database.clear_database()
        elif choice == 'G':
            print("\033[38;2;255;255;0mGrade Grouping.\033[0m")
            subject_name = input("\033[38;2;0;206;209mEnter the subject name:\033[0m")
            group_students(subject_name)
        elif choice == 'P':
            print("\033[38;2;255;255;0mPass/Fail Partition\033[0m")
            subject_name = input("\033[38;2;0;206;209mEnter the subject name:\033[0m")
            partition_students(subject_name)
        elif choice == 'R':
            remove_student()
        elif choice == 'S':
            show_students()
        elif choice == 'X':
            print("\033[38;2;255;255;0mExiting Admin Menu.\033[0m")
            break
        else:
            print("\033[38;2;255;0;0mInvalid choice. Please try again.\033[0m")

def group_students(subject_name):
    try:
        with open("students.data", 'r') as file:
            try:
                students = json.load(file)
            except json.JSONDecodeError:
                print("<Nothing to display>")
                return
    except FileNotFoundError:
        print("<Nothing to display>")
        return

    grade_groups = {}
    subject_found = False

    for student in students:
        for subject in student['subjects']:
            if subject['name'].lower() == subject_name.lower():
                subject_found = True
                grade = subject['grade']
                if grade not in grade_groups:
                    grade_groups[grade] = []
                grade_groups[grade].append(student)

    if not subject_found:
        print(f"\033[91mInvalid subject: {subject_name}\033[0m")
        return

    if not grade_groups:
        print("\033[93m<Nothing to display>\033[0m")
        return

    for grade, students in grade_groups.items():
        print(f"Grade {grade} in {subject_name}:")
        for student in students:
            print(f"  Student ID: {student['id']}, Name: {student['name']}")


def partition_students(subject_name):
    try:
        with open("students.data", 'r') as file:
            try:
                students = json.load(file)
            except json.JSONDecodeError:
                print("<Nothing to display>")
                return
    except FileNotFoundError:
        print("<Nothing to display>")
        return

    pass_students = []
    fail_students = []
    subject_found = False

    for student in students:
        for subject in student['subjects']:
            if subject['name'].lower() == subject_name.lower():
                subject_found = True
                if subject['grade'] != 'F':
                    pass_students.append(student)
                else:
                    fail_students.append(student)
                break

    if not subject_found:
        print(f"\033[91mInvalid subject: {subject_name}\033[0m")
        return

    print(f"Pass Students in {subject_name}:")
    for student in pass_students:
        print(f"  ID: {student['id']}, Name: {student['name']}")

    print(f"Fail Students in {subject_name}:")
    for student in fail_students:
        print(f"  ID: {student['id']}, Name: {student['name']}")

def remove_student():
    student_id = input("Enter student ID to remove: ")
    students = Database.load_students()
    student_found = any(str(student['id']) == student_id for student in students)
    if student_found:
        students = [student for student in students if str(student['id']) != student_id]
        Database.save_students(students)
        print(f"\033[93mStudent (ID: {student_id}) removed.\033[0m")
    else:
        print(f"\033[91mStudent (ID: {student_id}) does not exist.\033[0m")

def show_students():
    print("\033[93mStudent List\033[0m")
    students = Database.load_students()
    if not students:
        print("<Nothing to Display>")
        return
    for student in students:
        print(f"ID: {student['id']}, Name: {student['name']}, Email: {student['email']}")

def university_system_menu():
    while True:
        print("\033[38;2;0;206;209mWelcome to CLIUniApp\033[0m")
        print("\033[38;2;0;206;209mPlease choose an option:\033[0m")
        print("\033[38;2;0;206;209m(A) Admin Menu\033[0m")
        print("\033[38;2;0;206;209m(S) Student Menu\033[0m")
        print("\033[38;2;0;206;209m(X) Exit\033[0m")
        choice = input("\033[38;2;0;206;209mEnter your choice (A, S, X): \033[0m").upper()
        if choice == 'A':
            admin_menu()
        elif choice == 'S':
            student_system_menu()
        elif choice == 'X':
            print("\033[38;2;255;255;0mExiting the application. Goodbye!\033[0m")
            break
        else:
            print("\033[38;2;255;0;0mInvalid choice. Please choose again.\033[0m")

def student_system_menu():
    while True:
        print("\033[38;2;0;206;209mStudent Menu\033[0m")
        print("\033[38;2;0;206;209m(L) Login\033[0m")
        print("\033[38;2;0;206;209m(R) Register\033[0m")
        print("\033[38;2;0;206;209m(X) Exit\033[0m")
        choice = input("\033[38;2;0;206;209mEnter your choice (L, R, X): \033[0m").upper()

        if choice == 'L':
            login_student()
        elif choice == 'R':
            register_student()
        elif choice == 'X':
            print("\033[38;2;255;255;0mExiting Student Menu.\033[0m")
            break
        else:
            print("\033[38;2;255;0;0mInvalid choice. Please try again.\033[0m")

Path("students.data").touch()

if __name__ == "__main__":
    university_system_menu()