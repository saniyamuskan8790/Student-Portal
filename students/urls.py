from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('students/', views.student_list, name='student_list'),

    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('profile/<int:id>/', views.student_profile, name='student_profile'),
    path('attendance/', views.attendance, name='attendance'),
    path(
    'attendance-history/',
    views.attendance_history,
    name='attendance_history'
),
    path(
    'attendance-percentage/',
    views.attendance_percentage,
    name='attendance_percentage'
),
    path('marks/', views.add_marks, name='add_marks'),
    path('marks-list/', views.marks_list, name='marks_list'),
    path(
    'report/<int:id>/',
    views.student_report,
    name='student_report'
),
]