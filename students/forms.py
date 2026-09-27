from django import forms
from .models import Student, Attendance, Marks

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            'name',
            'roll_number',
            'email',
            'phone',
            'course',
            'photo'
        ]
class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance

        fields = [
            'student',
            'date',
            'status'
        ]
class MarksForm(forms.ModelForm):

    class Meta:
        model = Marks

        fields = [
            'student',
            'subject',
            'exam_name',
            'marks_obtained',
            'max_marks'
        ]