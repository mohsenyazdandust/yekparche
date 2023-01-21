from django.db import models


class Course(models.Model):
    course_number = models.CharField(max_length=20, default='000')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.CharField(max_length=100)
    total = models.FloatField(default=0)


class Student(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    grades = models.ManyToManyField(Grade, blank=True)
    student_number = models.CharField(max_length=20, default='0000')
    def __str__(self):
        return self.name


    

