from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from .models import Student, Attendance, Marks
from .forms import StudentForm, AttendanceForm, MarksForm

def home(request):
    return render(request, 'home.html')


def register(request):

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student Registered Successfully!"
            )

            return redirect('/')

    else:
        form = StudentForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/dashboard/')

    return render(request, 'login.html')


@login_required
def dashboard(request):

    total_students = Student.objects.count()

    total_courses = Student.objects.values(
        'course'
    ).distinct().count()

    total_marks = Marks.objects.count()

    total_attendance = Attendance.objects.count()

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_marks': total_marks,
        'total_attendance': total_attendance,
    }

    return render(
        request,
        'dashboard.html',
        context
    )

@login_required
def student_list(request):

    query = request.GET.get('q')

    if query:

        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(roll_number__icontains=query)
        )

    else:

        students = Student.objects.all()

    return render(
        request,
        'student_list.html',
        {
            'students': students,
            'query': query
        }
    )


def logout_view(request):

    logout(request)

    return redirect('/')


@login_required
def edit_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == "POST":

        student.name = request.POST['name']
        student.roll_number = request.POST['roll_number']
        student.email = request.POST['email']
        student.phone = request.POST['phone']
        student.course = request.POST['course']

        student.save()

        messages.success(
            request,
            "Student Updated Successfully!"
        )

        return redirect('/students/')

    return render(
        request,
        'edit_student.html',
        {'student': student}
    )


@login_required
def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    student.delete()

    messages.success(
        request,
        "Student Deleted Successfully!"
    )

    return redirect('/students/')


@login_required
def student_profile(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    return render(
        request,
        'student_profile.html',
        {'student': student}
    )
@login_required
def attendance(request):

    if request.method == "POST":

        form = AttendanceForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Attendance Saved Successfully!"
            )

            return redirect('/attendance/')

    else:

        form = AttendanceForm()

    return render(
        request,
        'attendance.html',
        {'form': form}
    )
@login_required
def attendance_history(request):

    records = Attendance.objects.select_related('student').order_by('-date')

    return render(
        request,
        'attendance_history.html',
        {'records': records}
    )
@login_required
def attendance_percentage(request):

    students = Student.objects.all()

    attendance_data = []

    for student in students:

        total = Attendance.objects.filter(
            student=student
        ).count()

        present = Attendance.objects.filter(
            student=student,
            status=True
        ).count()

        if total > 0:
            percentage = (present / total) * 100
        else:
            percentage = 0

        attendance_data.append({
            'student': student,
            'total': total,
            'present': present,
            'absent': total - present,
            'percentage': round(percentage, 2)
        })

    return render(
        request,
        'attendance_percentage.html',
        {
            'attendance_data': attendance_data
        }
    )
@login_required
def add_marks(request):

    if request.method == "POST":

        form = MarksForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Marks Added Successfully!"
            )

            return redirect('/marks/')

    else:

        form = MarksForm()

    return render(
        request,
        'marks.html',
        {'form': form}
    )
@login_required
def marks_list(request):

    student_id = request.GET.get('student')

    students = Student.objects.all()

    if student_id:
        marks = Marks.objects.filter(
            student_id=student_id
        ).select_related('student')
    else:
        marks = Marks.objects.select_related('student').all()

    return render(
        request,
        'marks_list.html',
        {
            'marks': marks,
            'students': students,
            'selected_student': student_id
        }
    )
@login_required
def student_report(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    # Attendance

    total_attendance = Attendance.objects.filter(
        student=student
    ).count()

    present_attendance = Attendance.objects.filter(
        student=student,
        status=True
    ).count()

    if total_attendance > 0:
        attendance_percentage = round(
            (present_attendance / total_attendance) * 100,
            2
        )
    else:
        attendance_percentage = 0

    # Marks

    marks = Marks.objects.filter(
        student=student
    )

    total_marks_obtained = sum(
        mark.marks_obtained for mark in marks
    )

    total_max_marks = sum(
        mark.max_marks for mark in marks
    )

    if total_max_marks > 0:
        overall_percentage = round(
            (total_marks_obtained / total_max_marks) * 100,
            2
        )
    else:
        overall_percentage = 0

    context = {
        'student': student,
        'marks': marks,
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
        'attendance_percentage': attendance_percentage,
        'total_marks_obtained': total_marks_obtained,
        'total_max_marks': total_max_marks,
        'overall_percentage': overall_percentage,
    }

    return render(
        request,
        'student_report.html',
        context
    )