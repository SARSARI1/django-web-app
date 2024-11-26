# ~/projects/django-web-app/merchex/merchex/urls.py
from django.contrib import admin
from django.urls import path
from listings import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/<int:id>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('professors/', views.ProfessorListView.as_view(), name='professor_list'),
    path('professors/<int:id>/', views.ProfessorDetailView.as_view(), name='professor_detail'),
    path('login/', views.login_view, name='login'),  # Map the login view to '/login/'
    path('admin_profile/', views.admin_profile_view, name='admin_profile'),
    path('professor_profile/', views.professor_profile_view, name='professor_profile'),
    path('professor/<int:id>/profile/', views.professor_profile_view, name='professor_profile'),
    path('professor/<int:id>/courses/', views.professor_courses_view, name='professor_courses'),
    path('professor/<int:professor_id>/courses/<int:course_id>/', views.professor_course_detail_view, name='professor_course_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('statistic_1', views.statistic_1, name='statistic_1'),
    path('statistic_2', views.statistic_2, name='statistic_2'),
    path('statistic_3', views.statistic_3, name='statistic_3'),
    path('statistic_4', views.statistic_4, name='statistic_4'),
    path('statistic_5/<int:id_employee>', views.statistic_5, name='statistic_5'),
    path('statistics/', views.statistics_view, name='statistics'),
   path('statistic-data/<int:department_id>/', views.statistic_data, name='statistic_data')
]
