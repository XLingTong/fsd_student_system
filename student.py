import json
import os
import re
import random
from pathlib import Path

# Class Definitions
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
    
def register_student():
    """注册新学生，同时生成一个唯一的ID。"""
    email = input("Enter email: ")
    if not validate_email(email):
        print("Invalid email format.")
        return
    password = input("Enter password: ")
    if not validate_password(password):
        print("Invalid password format.")
        return
    if student_exists(email):
        print("Student already registered.")
        return
    
    # 假设每个学生的ID是学生列表长度加1
    student = {
        "id": generate_student_id(),
        "name": input("Enter your name: "),
        "email": email,
        "password": password,
        "subjects": []  # 初始化空的科目列表
    }
    save_student(student)
    print("Student registered successfully.")

def generate_student_id():
    """生成唯一的学生ID。"""
    try:
        with open("students.data", "r") as file:
            students = json.load(file)
        return len(students) + 1
    except (FileNotFoundError, json.JSONDecodeError):
        return 1

def save_student(student):
    """将学生数据保存到文件。"""
    try:
        with open("students.data", "r") as file:
            students = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        students = []

    students.append(student)
    with open("students.data", "w") as file:
        json.dump(students, file, indent=4)

def student_exists(email):
    """检查学生是否已在文件中注册。"""
    try:
        with open("students.data", "r") as file:
            students = json.load(file)
        return any(student['email'] == email for student in students)
    except (json.JSONDecodeError, FileNotFoundError):
        return False

def validate_email(email):
    """验证电子邮件格式是否正确。"""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validate_password(password):
    """验证密码格式。密码必须以大写字母开头，至少有6个字母，之后是至少三位数字。"""
    return re.match(r"[A-Z][a-zA-Z]{5,}[0-9]{3,}$", password) is not None

def update_student_data(student):
    """更新学生数据到文件。"""
    with open("students.data", "r") as file:
        students = json.load(file)
    updated_students = [s if s['id'] != student['id'] else student for s in students]
    with open("students.data", "w") as file:
        json.dump(updated_students, file, indent=4)

def login_student():
    """学生登录。"""
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    # 检查文件是否存在且不为空
    if not os.path.exists("students.data") or os.path.getsize("students.data") == 0:
        print("No registered students. Please register first.")
        return
    # 从文件读取学生数据
    with open("students.data", "r") as file:
        students = json.load(file)
    # 验证学生是否存在
    student = next((s for s in students if s['email'] == email and s['password'] == password), None)
    if student:
        print("Login successful.")
        student_course_menu(student)
    else:
        print("Invalid login credentials.")

def change_password(student):
    """允许学生更改密码。"""
    new_password = input("Enter new password: ")
    if not validate_password(new_password):
        print("Invalid password format.")
        return
    student['password'] = new_password
    update_student_data(student)
    print("Password updated successfully.")

def enrol_subject(student):
    """允许学生注册科目。"""
    if len(student['subjects']) >= 4:
        print("Cannot enrol in more than 4 subjects.")
        return
    subject_name = input("Enter subject name: ")
    subject = {
        "id": subject_name,
        "name": subject_name,
        "mark": random.randint(25, 100)
    }
    subject['grade'] = Subject.assign_grade(subject['mark'])
    student['subjects'].append(subject)
    update_student_data(student)
    print("Subject enrolled successfully.")

def remove_subject(student):
    """允许学生移除科目。"""
    subject_id = input("Enter subject ID to remove: ")
    student['subjects'] = [subject for subject in student['subjects'] if subject['id'] != subject_id]
    update_student_data(student)
    print("Subject removed successfully.")

def show_subjects(student):
    """显示学生已注册的所有科目及其成绩和等级。"""
    if not student['subjects']:
        print("No subjects enrolled.")
        return
    for subject in student['subjects']:
        print(f"Subject ID: {subject['id']}, Name: {subject['name']}, Mark: {subject['mark']}, Grade: {subject['grade']}")

def clear_database():
    """清空数据文件。"""
    open("students.data", 'w').close()
    print("Database cleared.")

def group_students():
    """按成绩组织显示学生。"""
    with open("students.data", 'r') as file:
        students = json.load(file)
    grade_groups = {}
    for student in students:
        for subject in student['subjects']:
            grade = subject['grade']
            if grade not in grade_groups:
                grade_groups[grade] = []
            grade_groups[grade].append(student)
    for grade, students in grade_groups.items():
        print(f"Grade {grade}:")
        for student in students:
            print(f"  Student ID: {student['id']}, Name: {student['name']}")

def partition_students():
    """显示通过/未通过的学生分配。"""
    with open("students.data", 'r') as file:
        students = json.load(file)
    pass_students = [s for s in students if all(sub['grade'] != 'F' for sub in s['subjects'])]
    fail_students = [s for s in students if any(sub['grade'] == 'F' for sub in s['subjects'])]
    print("Pass Students:")
    for student in pass_students:
        print(f"  ID: {student['id']}, Name: {student['name']}")
    print("Fail Students:")
    for student in fail_students:
        print(f"  ID: {student['id']}, Name: {student['name']}")

def remove_student():
    """按ID移除学生。"""
    student_id = input("Enter student ID to remove: ")
    with open("students.data", 'r') as file:
        students = json.load(file)
    students = [student for student in students if student['id'] != student_id]
    with open("students.data", 'w') as file:
        json.dump(students, file)
    print("Student removed.")
   
def show_students():
    """显示文件中的所有学生。"""
    with open("students.data", 'r') as file:
        students = json.load(file)
    for student in students:
        print(f"ID: {student['id']}, Name: {student['name']}")

# Main Menu Functions
def university_system_menu():
    while True:
        print("\nWelcome to CLIUniApp")
        print("Please choose an option:")
        print("(A) Admin Menu")
        print("(S) Student Menu")
        print("(X) Exit")
        choice = input("Enter your choice (A, S, X): ").upper()
        if choice == 'A':
            admin_menu()
        elif choice == 'S':
            student_system_menu()
        elif choice == 'X':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose again.")

def student_system_menu():
    while True:
        print("\nStudent Menu")
        print("(L) Login")
        print("(R) Register")
        print("(X) Exit")
        choice = input("Enter your choice (L, R, X): ").upper()

        if choice == 'L':
            login_student()
        elif choice == 'R':
            register_student()
        elif choice == 'X':
            print("Exiting Student Menu.")
            break
        else:
            print("Invalid choice. Please try again.")

def student_course_menu(student):
    """学生课程系统菜单。"""
    while True:
        print("\nStudent Course Menu")
        print("(C) Change Password")
        print("(E) Enrol in a Subject")
        print("(R) Remove a Subject")
        print("(S) Show Enrolled Subjects")
        print("(X) Exit")
        choice = input("Enter your choice (C, E, R, S, X): ").upper()

        if choice == 'C':
            change_password(student)
        elif choice == 'E':
            enrol_subject(student)
        elif choice == 'R':
            remove_subject(student)
        elif choice == 'S':
            show_subjects(student)
        elif choice == 'X':
            print("Exiting Student Course Menu.")
            break
        else:
            print("Invalid choice. Please try again.")


def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("(C) Clear Database")
        print("(G) Group Students")
        print("(P) Partition Students")
        print("(R) Remove a Student")
        print("(S) Show Students")
        print("(X) Exit")
        choice = input("Enter your choice (C, G, P, R, S, X): ").upper()
        if choice == 'C':
            clear_database()
        elif choice == 'G':
            group_students()
        elif choice == 'P':
            partition_students()
        elif choice == 'R':
            remove_student()
        elif choice == 'S':
            show_students()
        elif choice == 'X':
            print("Exiting Admin Menu.")
            break
        else:
            print("Invalid choice. Please try again.")

# 确保students.data文件存在
Path("students.data").touch()

if __name__ == "__main__":
    university_system_menu()

