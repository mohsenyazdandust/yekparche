from django.db import models


class Course(models.Model):
    course_number = models.CharField(max_length=10, default='000')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mid_term = models.FloatField(default=0)
    final = models.FloatField(default=0)
    activities = models.FloatField(default=0)
    total = models.FloatField(default=0)
    

