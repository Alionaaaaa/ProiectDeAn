# Singleton Design Pattern

class University:
    _instance = None

    @staticmethod
    def get_instance():
        if not University._instance:
            University()
        return University._instance

    def __init__(self):
        if University._instance:
            raise Exception("University class is a singleton.")
        else:
            University._instance = self
            self.students = []
            self.teachers = []


# Factory Design Pattern

class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name):
        super().__init__(name)
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def get_average_grade(self):
        if len(self.grades) == 0:
            return 0
        return sum(self.grades) / len(self.grades)

    def __str__(self):
        return f"Student: {self.name}"


class Teacher(Person):
    def __init__(self, name):
        super().__init__(name)
        self.subjects = []

    def add_subject(self, subject):
        self.subjects.append(subject)

    def get_subjects(self):
        return self.subjects

    def __str__(self):
        return f"Teacher: {self.name}"


class PersonFactory:
    def create_person(self, name, person_type):
        if person_type == "student":
            return Student(name)
        elif person_type == "teacher":
            return Teacher(name)
        else:
            raise ValueError("Invalid person type.")


# Decorator Design Pattern

class PersonDecorator(Person):
    def __init__(self, person):
        self.person = person

    def __str__(self):
        return self.person.__str__()


class GoodStudentDecorator(PersonDecorator):
    def __str__(self):
        return f"Good {self.person.__str__()}"


# Facade Design Pattern

class UniversityFacade:
    def __init__(self):
        self.university = University.get_instance()
        self.person_factory = PersonFactory()

    def enroll_student(self, name):
        student = self.person_factory.create_person(name, "student")
        self.university.students.append(student)

    def hire_teacher(self, name):
        teacher = self.person_factory.create_person(name, "teacher")
        self.university.teachers.append(teacher)

    def display_students(self):
        for student in self.university.students:
            print(student)
            print("Grades:", student.grades)
            print("Average Grade:", student.get_average_grade())
            print()

    def enter_grades(self):
        student_name = input("Enter student name: ")
        found_student = None
        for student in self.university.students:
            if student.name == student_name:
                found_student = student
                break
        if found_student:
            grades_str = input("Enter grades (comma-separated): ")
            grades = [float(grade.strip()) for grade in grades_str.split(",")]
            found_student.grades.extend(grades)
        else:
            print("Student not found.")
        if grades != 0:
            print("Grades added successfully.")

    def display_grades(self):
        student_name = input("Enter student name: ")
        for student in self.university.students:
            if student.name == student_name:
                print(f"Grades for {student.name}:")
                for grades in student.grades:
                    print(grades)
                return
        print("Student not found.")

    def display_teachers(self):
        for teacher in self.university.teachers:
            print(teacher)

    def display_students_with_only_tens(self):
        print("Students with only grade 10:")
        student_list = StudentList(self.university.students)
        student_iterator = iter(student_list)
        try:
            while True:
                student = next(student_iterator)
                print(student)
                print("Grades:", student.grades)
                print("Average Grade:", student.get_average_grade())
                print()
        except StopIteration:
            pass


# Observer Design Pattern

class Observer:
    def update(self):
        pass


class StudentCountObserver(Observer):
    def __init__(self, facade):
        self.facade = facade

    def update(self):
        student_count = len(self.facade.university.students)
        print(f"Student count changed. Total students: {student_count}")


class UniversityObservable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()


# Iterator Design Pattern
class Iterator:
    def __next__(self):
        pass


class StudentIterator(Iterator):
    def __init__(self, students):
        self.students = students
        self.index = 0

    def __next__(self):
        while self.index < len(self.students):
            student = self.students[self.index]
            grades = student.grades
            if all(grade == 10 for grade in grades):
                self.index += 1
                return student
            self.index += 1

        raise StopIteration


class StudentList:
    def __init__(self, students):
        self.students = students

    def __iter__(self):
        return StudentIterator(self.students)


# Usage

def display_menu():
    print("\n"
          "Welcome to the University Management System")
    print("1. Enroll Student")
    print("2. Hire Teacher")
    print("3. Display Students")
    print("4. Display Students with Only Tens")
    print("5. Enter Grades")
    print("6. Display Grades")
    print("7. Decorate Student")
    print("q. Quit\n")


def main():
    facade = UniversityFacade()
    observable = UniversityObservable()
    observable.add_observer(StudentCountObserver(facade))

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter student name: ")
            facade.enroll_student(name)
            observable.notify_observers()

        elif choice == "2":
            name = input("Enter teacher name: ")
            facade.hire_teacher(name)

        elif choice == "3":
            print("Students:")
            for student in facade.university.students:
                print(student)

        elif choice == "4":
            facade.display_students_with_only_tens()

        elif choice == "5":
            facade.enter_grades()

        elif choice == "6":
            print("Grades:")
            facade.display_grades()

        elif choice == "7":
            name = input("Enter student name: ")
            student = facade.person_factory.create_person(name, "student")
            decorated_student = GoodStudentDecorator(student)
            print(decorated_student)

        elif choice.lower() == "q":
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    main()
