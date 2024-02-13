
import os
from functools import wraps
from datetime import datetime

def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            x_res = (f"Вызывается функция {old_function.__name__} с аргументами {args} и {kwargs}.\n"
                     f"Результатом функции является: {result}.\n"
                     f" Функция вызвана в {datetime.now()} .\n")
            with open(path, 'a', encoding='utf-8') as file:
                file.write(x_res)

            return result
        return new_function
    return __logger

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []  # оконченные курсы
        self.courses_in_progress = []  # курсы на данный момент
        self.grades = {}  # оценки

    def rate_hw(self, lecturer, course, grade):  # оценки выставляемые студентами лекторам
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grades(self):
        mid_sum = 0
        for course_grades in self.grades.values():
            course_sum = 0
            for grades in course_grades:
                course_sum += grades
            course_mid = course_sum / len(course_grades)
            mid_sum += course_mid
        if mid_sum == 0:
            return f'Оценок нет!'
        else:
            return f"{mid_sum / len(self.grades.values()):.2f}"
    @logger(path="log_4.log")
    def __str__(self):
        self.courses_in_progress = ", ".join(self.courses_in_progress)
        self.finished_courses = ", ".join(self.finished_courses)
        return (f"Имя:{self.name}\nФамилия:{self.surname}\n"
                f"Средняя оценка за домашние задания: {self.average_grades()}\n"
                f"Курсы в процессе изучения: {self.courses_in_progress}\nЗавершенные курсы: {self.finished_courses}")

    def __eq__(self, student):
        if not isinstance(student, Student):
            print(f'Такого преподавателя нет, сравнение невозможно!')
            return
        else:
            return self.average_grades() == student.average_grades()

    def __gt__(self, other):
        if not isinstance(other, Student):
            print('Такого студента нет, сравнение невозможно!')
            return
        return self.average_grades() > other.average_grades()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []  # прикрепленные курсы


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grades(self):
        mid_sum = 0
        for course_grades in self.grades.values():
            course_sum = 0
            for grades in course_grades:
                course_sum += grades
            course_mid = course_sum / len(course_grades)
            mid_sum += course_mid
        if mid_sum == 0:
            return f'Оценок нет!'
        else:
            return f"{mid_sum / len(self.grades.values()):.2f}"

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.average_grades()}"

    def __gt__(self, lecturer):
        if not isinstance(lecturer, Lecturer):
            print('Такого преподавателя нет, сравнение невозможно!')
            return
        return self.average_grades() > lecturer.average_grades()

    def __eq__(self, lecturer):
        if not isinstance(lecturer, Lecturer):
            print(f'Такого преподавателя нет, сравнение невозможно!')
            return
        else:
            return self.average_grades() == lecturer.average_grades()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):  # оценки за дз
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя:{self.name}\nФамилия:{self.surname}"


# студенты
best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['Git']
best_student.finished_courses += ['Введение в программирование']

new_best_student = Student('Harry', 'Potter', 'your_gender')
new_best_student.courses_in_progress += ['Python']
new_best_student.courses_in_progress += ['Git']
new_best_student.finished_courses += ['Введение в программирование']

# Менторы
cool_mentor = Mentor('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']

new_cool_mentor = Mentor('ED', 'Single')
new_cool_mentor.courses_attached += ['Git']

# проверяющие
any_reviewer = Reviewer("Danny", "Murat")
any_reviewer.courses_attached += ['Python']

any_reviewer1 = Reviewer("Tanya", "Kristal")
any_reviewer1.courses_attached += ['Git']

# оценки студентам
any_reviewer.rate_hw(best_student, 'Python', 10)
any_reviewer.rate_hw(best_student, 'Python', 10)
any_reviewer.rate_hw(best_student, 'Python', 10)

any_reviewer.rate_hw(new_best_student, 'Python', 10)
any_reviewer.rate_hw(new_best_student, 'Python', 10)
any_reviewer.rate_hw(new_best_student, 'Python', 10)

# лекторы
any_lecturer = Lecturer("Diana", "Still")
any_lecturer.courses_attached += ['Python']

new_any_lecturer = Lecturer("Petter", "Parker")
new_any_lecturer.courses_attached += ['Python']

# оценки лекторам
best_student.rate_hw(any_lecturer, 'Python', 10)
best_student.rate_hw(any_lecturer, 'Python', 10)
best_student.rate_hw(any_lecturer, 'Python', 10)

new_best_student.rate_hw(new_any_lecturer, 'Python', 10)
new_best_student.rate_hw(new_any_lecturer, 'Python', 10)
new_best_student.rate_hw(new_any_lecturer, 'Python', 10)

# оценки студента и лектора
print(best_student.grades)
print(any_lecturer.grades)


print(new_best_student.grades)
print(new_any_lecturer.grades)

# общая информация
print(any_reviewer)
print(any_lecturer)
print(best_student)

# сравнения
print(any_lecturer.__eq__(new_any_lecturer))
print(best_student.__eq__(new_best_student))

print(any_lecturer.__gt__(new_any_lecturer))
print(best_student.__gt__(new_best_student))

# функция для определения средней оценки студентов по данному курсу


def middle_grades_students(course, students):
    grades_students = []
    for student in students:
        if course in student.grades.keys():
            grades_students.extend(student.grades[course])
    return sum(grades_students)/len(grades_students)

# функция для определения средней оценки лекторов по данному курсу


def middle_grades_lectors(course, lectors):
    grades_lectors = []
    for student in lectors:
        if course in student.grades.keys():
            grades_lectors.extend(student.grades[course])
    return sum(grades_lectors)/len(grades_lectors)


print(f"{best_student.name} {best_student.surname}: {best_student.grades['Python']}",
      f"{new_best_student.name} {new_best_student.surname}: {new_best_student.grades['Python']}",
      f"Среднее значение оценок домашнего задания по "
      f"курсу Python: {middle_grades_students('Python', [best_student, new_best_student])}", sep='\n', end='\n\n')

print(f"{any_lecturer.name} {any_lecturer.surname}: {any_lecturer.grades['Python']}",
      f"{new_any_lecturer.name} {new_any_lecturer.surname}: {new_any_lecturer.grades['Python']}",
      f"Среднее значение оценок лекторов "
      f"по курсу Python: {middle_grades_lectors('Python', [any_lecturer, new_any_lecturer])}", sep='\n')
