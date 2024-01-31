from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)
        print(f"{self.name} enrolled in {course.name}.")

    def drop_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
            print(f"{self.name} dropped {course.name}.")
        else:
            print(f"{self.name} is not enrolled in {course.name}.")

    def display_courses(self):
        if self.courses:
            print(f"{self.name}'s Enrolled Courses:")
            for course in self.courses:
                print("- ", course.name)
        else:
            print(f"{self.name} is not enrolled in any courses.")

class Course:
    def __init__(self, name, instructor):
        self.name = name
        self.instructor = instructor
        self.students = []


    def enroll_student(self, student):
        self.students.append(student)
        print(f"{student.name} enrolled in {self.name}.")


    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
            print(f"{student.name} removed from {self.name}.")
        else:
            print(f"{student.name} is not enrolled in {self.name}.")

    def display_students(self):
        if self.students:
            print(f"Students Enrolled in {self.name}:")
            for student in self.students:
                print("- ", student.name)
        else:
            print(f"No students enrolled in {self.name}.")

    # Add methods to your Course class, such as enroll_student, remove_student, and display_students

students = []  # Create an empty list to store students
courses = []   # Create an empty list to store courses

@app.route('/')
def home():
    return render_template('index.html', students=students, courses=courses)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    title = request.args.get("title", "Add Student")
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        grade = int(request.form['grade'])
        student = Student(name, age, grade)
        students.append(student)
        return redirect(url_for('home'))
    return render_template('add_student.html',title=title)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    title = request.args.get("title", "Add Course")
    if request.method == 'POST':
        name = request.form['name']
        instructor = request.form['instructor']
        course = Course(name, instructor)
        courses.append(course)
        return redirect(url_for('home'))
    return render_template('add_course.html', title=title)

@app.route('/enroll_student', methods=['GET', 'POST'])
def enroll_student():
    title = request.args.get("title", "Enroll Student")
    if request.method == 'POST':
        student_name = request.form['student_name']
        course_name = request.form['course_name']
        student = next((s for s in students if s.name == student_name), None)
        course = next((c for c in courses if c.name == course_name), None)

        if student and course:
            course.enroll_student(student)
            student.add_course(course)  # Pass the 'course' object, not just the name
        else:
            # Handle the case where the student or course is not found
            flash("Student or course not found.")

        return redirect(url_for('home'))

    return render_template('enroll_student.html', students=students, courses=courses, title=title)


@app.route('/remove_student', methods=['GET', 'POST'])
def remove_student():
    title = request.args.get("title", "Remove Student")
    if request.method == 'POST':
        student_name = request.form['student_name']
        course_name = request.form['course_name']
        student = next((s for s in students if s.name == student_name), None)
        course = next((c for c in courses if c.name == course_name), None)
        if student and course:
            course.remove_student(student)
            student.drop_course(course)  # Pass the 'course' object, not just the name
        return redirect(url_for('home'))
    return render_template('remove_student.html', students=students, courses=courses, title=title)

@app.route('/display_student_courses', methods=['GET', 'POST'])
def display_student_courses():
    title = request.args.get("title", "Display Student Course")
    if request.method == 'POST':
        student_name = request.form['student_name']
        student = next((s for s in students if s.name == student_name), None)

        if student:
            return render_template('display_student_courses.html', student=student, students=students, title=title)
        else:
            flash("Student not found.")

    return render_template('display_student_courses.html', students=students, title=title)

@app.route('/display_course_students', methods=['GET', 'POST'])
def display_course_students():
    title = request.args.get("title", "Display Course Student")
    selected_course = None  # Initialize with None in case no course is selected
    if request.method == 'POST':
        course_name = request.form['course_name']
        selected_course = next((c for c in courses if c.name == course_name), None)

        # Debug: Print the selected course name to the console
        print("Selected Course:", selected_course)

        if selected_course:
            return render_template('display_course_students.html', selected_course=selected_course, courses=courses, title=title)
        else:
            flash("Course not found.")

    # Pass the list of courses to the template for course selection
    return render_template('display_course_students.html', courses=courses, selected_course=selected_course, title=title)


if __name__ == '__main__':
    app.run(debug=True)
