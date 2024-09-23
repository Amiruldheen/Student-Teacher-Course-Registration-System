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
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.name}-{self.id}"



class Course(models.Model):
    '''
    To represent Course Deatails.
    '''
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, related_name='teacher_courses', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title



