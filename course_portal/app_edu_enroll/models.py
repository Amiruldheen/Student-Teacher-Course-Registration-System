from django.db import models


class Student(models.Model):
    '''
    To represent the Student Deatils
    '''
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField()
    course = models.ManyToManyField('Course', related_name='students')

    def __str__(self) -> str:
        return self.name


class Teacher(models.Model):
    '''
    To represent teacher Deatails
    '''
    name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.name}-{self.id}"
    
    @property
    def name_length(self):
        return len(self.name)



class Course(models.Model):
    '''
    To represent Course Deatails.
    '''
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, related_name='teacher_courses', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


'''
To Summarize:
If the attribute exists directly in the model (e.g., name, age, email), you can query using that attribute name directly.
If the attribute exists in a related model (via ForeignKey or ManyToManyField), you can query from the reverse side using the related_name.
related_name is required when you want to query from the reverse side of a relationship. It enables you to access related objects from the related model.
So, your understanding is mostly correct! If you don't have a direct attribute, but you have a relationship, you can use the related_name to query from the reverse side.
'''
'''
from app_edu_enroll.models import Student, Teacher, Course

In [2]: teacher = Teacher.objects.get(name__contains="Ash")
In [3]: teacher
Out[3]: <Teacher: Ashok-4>
In [4]: course_taught_by = teacher.teacher_courses.all()
In [5]: course_taught_by
Out[5]: <QuerySet [<Course: Cartography>, <Course: Photogrametry>]>
In [6]: type(course_taught_by)
Out[6]: django.db.models.query.QuerySet

In [10]: course = Course.objects.filter(teacher=teacher)

In [11]: course
Out[11]: <QuerySet [<Course: Cartography>, <Course: Photogrametry>]>
In [7]: course = Course.objects.get(title__contains="Python")
In [8]: students_in_course = course.students.all()
In [9]: students_in_course
Out[9]: <QuerySet [<Student: Amir>, <Student: SHOMESH>, <Student: Praveen>, <Student: Agny>]>
---------------------------
traverse using dunder (__)
---------------------------
In [21]: courses = Course.objects.filter(teacher__name="Ashok") #line2 & 10 combined here

In [22]: courses
Out[22]: <QuerySet [<Course: Cartography>, <Course: Photogrametry>]>

In [23]: courses = Course.objects.filter(teacher__email="revathi@gmail.com")

In [24]: courses
Out[24]: <QuerySet [<Course: EVS>]>

In [25]: teacher = Teacher.objects.get(name__contains="Ash")

In [26]: courses = teacher.teacher_courses.all()

In [27]: courses
Out[27]: <QuerySet [<Course: Cartography>, <Course: Photogrametry>]>

In [28]: students = Student.objects.filter(course__title="HTML")

In [29]: students
Out[29]: <QuerySet [<Student: SHOMESH>]>

In [30]: students = Student.objects.filter(course__title="Python") #line 7,8

In [31]: students
Out[31]: <QuerySet [<Student: Amir>, <Student: SHOMESH>, <Student: Praveen>, <Student: Agny>]>
'''
'''
Without select_related:
courses = Course.objects.all()
for course in courses:
    print(course.title, course.teacher.name)  # This hits the DB once for each course's teacher

If there are 100 courses, this will make 101 queries: 1 for the courses and 1 for each course-s teacher.

With select_related:
courses = Course.objects.select_related('teacher').all()
for course in courses:
    print(course.title, course.teacher.name)  # Single query with JOIN to fetch teacher

This performs a single query using a SQL join to retrieve both Course and Teacher data.

---------------------------------------------------------------------------------------

Without prefetch_related:

students = Student.objects.all()
for student in students:
    print(student.name)
    for course in student.course.all():  # This hits the DB once for each student's courses
        print(course.title)
If there are 100 students, and each student has 5 courses, this will make 101 queries (1 for the students and 1 for each students courses).



With prefetch_related:
students = Student.objects.prefetch_related('course').all()
for student in students:
    print(student.name)
    for course in student.course.all():  # Only two queries: 1 for students, 1 for courses
        print(course.title)

This performs two queries: one for the Student objects and another for the Course objects related to those students.

'''