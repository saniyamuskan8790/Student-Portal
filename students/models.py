from django.db import models


class Student(models.Model):

    name = models.CharField(max_length=100)

    roll_number = models.CharField(
        max_length=20,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(max_length=10)

    course = models.CharField(max_length=100)

    photo = models.ImageField(
        upload_to='students/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
class Attendance(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.name} - {self.date}"
class Marks(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.CharField(max_length=100)

    exam_name = models.CharField(max_length=100)

    marks_obtained = models.FloatField()

    max_marks = models.FloatField(default=100)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"
