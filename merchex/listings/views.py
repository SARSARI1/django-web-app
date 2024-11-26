# ~/projects/django-web-app/merchex/listings/views.py
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import pandas as pd
from datetime import datetime
from collections import defaultdict
from datetime import datetime
from openpyxl import Workbook
from dateutil.relativedelta import relativedelta
from reportlab.lib.pagesizes import A4


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


from django.shortcuts import render, redirect
from django.contrib import messages




from django.shortcuts import render
from django.db.models import Count
from .models import Course, Professor, Department, RequiredSkill, GainedSkill
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncYear
from .models import Course, Professor, Department, RequiredSkill, GainedSkill
from datetime import datetime


from django.db.models import Count, F
from django.db.models.functions import TruncYear
from .models import Course, Professor, Department, RequiredSkill, GainedSkill
from datetime import datetime

from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncYear
from .models import Course, Department, RequiredSkill, GainedSkill, Professor, CourseProfessor
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Count, F
from django.db.models.functions import TruncYear
from .models import Course, Professor, Department, RequiredSkill, GainedSkill, CourseRequiredSkill  # Add CourseRequiredSkill here
from datetime import datetime
from .models import Course, Professor, Department, RequiredSkill, GainedSkill, CourseGainedSkill, CourseRequiredSkill, CourseProfessor
from django.db.models import Count
from django.db.models.functions import TruncYear
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect


from django.core.files.storage import default_storage
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import pandas as pd
from datetime import datetime
from collections import defaultdict
from datetime import datetime
from openpyxl import Workbook

from dateutil.relativedelta import relativedelta
from reportlab.lib.pagesizes import A4




# login views

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncYear
from listings.models import Department, Course, Professor, CourseRequiredSkill, CourseGainedSkill

def dashboard(request):
    # 1. Calculate course completion rate by department
    total_courses = Course.objects.count()
    completed_courses = Course.objects.filter(is_completed=True).count()
    completion_rate = (completed_courses / total_courses * 100) if total_courses else 0
    
    # 2. Counting required and gained skills
    skills_comparison = {
        "required": RequiredSkill.objects.count(),
        "gained": GainedSkill.objects.count(),
    }
    
    # 3. Counting the number of courses offered by each department
    courses_by_department_data = {
        "labels": list(Department.objects.values_list('name', flat=True)),
        "counts": list(Course.objects.values('department')
                       .annotate(total=Count('id'))
                       .values_list('total', flat=True))
    }
    
    # 4. The number of courses offered by each department, broken down by year (contract start date)
    courses_by_year_data = {
        "years": list(Course.objects.annotate(year=TruncYear('contract_start_date'))
                      .values('year')
                      .distinct()
                      .order_by('year')
                      .values_list('year', flat=True)),
        "counts": list(Course.objects.annotate(year=TruncYear('contract_start_date'))
                      .values('year')
                      .annotate(total=Count('id'))
                      .order_by('year')
                      .values_list('total', flat=True)),
    }

    # 5. Compare the number of required skills vs. gained skills for each course
    course_skills_comparison = []
    courses = Course.objects.all()
    for course in courses:
        required_skills = CourseRequiredSkill.objects.filter(course=course).count()
        gained_skills = CourseGainedSkill.objects.filter(course=course).count()
        course_skills_comparison.append({
            "course_title": course.title,
            "required_skills": required_skills,
            "gained_skills": gained_skills
        })
    
    # 6. Count the total number of days each professor worked
    professor_working_days = []
    professors = Professor.objects.all()
    for professor in professors:
        assigned_courses = CourseProfessor.objects.filter(professor=professor).values('assignment_date').distinct()
        working_days = len(assigned_courses)  # Count distinct assignment dates
        professor_working_days.append({
            "professor_name": f"{professor.first_name} {professor.last_name}",
            "working_days": working_days
        })
    
    # 7. Count the total number of departments, professors
    total_departments = Department.objects.count()
    total_professors = Professor.objects.count()

    # 8. Fetch all departments for the dropdown
    departments = Department.objects.all()
    
    # Send context to the template
    context = {
        "completion_rate": completion_rate,
        "total_courses": total_courses,
        "skills_comparison": skills_comparison,
        "courses_by_department_data": courses_by_department_data,
        "courses_by_year_data": courses_by_year_data,
        "course_skills_comparison": course_skills_comparison,
        "professor_working_days": professor_working_days,
        "total_departments": total_departments,
        "total_professors": total_professors,
        "departments": departments,  # Add departments to context
    }
    
    return render(request, 'listings/dashboard.html', context)




from django.http import JsonResponse
from django.db.models import Count, F
from django.db.models.functions import TruncMonth, TruncYear
from .models import Course, Department, CourseRequiredSkill, CourseGainedSkill, CourseProfessor, Professor

# Statistic 1: Visualize the completion rate of courses by department
def statistic_1(request):
    departments = Department.objects.all()
    completion_rates = []
    for department in departments:
        total_courses = Course.objects.filter(department=department).count()
        completed_courses = Course.objects.filter(department=department, is_completed=True).count()
        completion_rate = (completed_courses / total_courses * 100) if total_courses else 0
        completion_rates.append({
            "department": department.name,
            "completion_rate": completion_rate
        })
    return JsonResponse({"completion_rates": completion_rates})


# Statistic 2: Number of courses offered by each department
def statistic_2(request):
    data = Course.objects.values(department_name=F('department__name')).annotate(course_count=Count('id'))
    return JsonResponse({"courses_by_department": list(data)})


# Statistic 3: Compare the number of required skills vs. gained skills for each course
def statistic_3(request):
    data = []
    courses = Course.objects.all()
    for course in courses:
        required_skills = CourseRequiredSkill.objects.filter(course=course).count()
        gained_skills = CourseGainedSkill.objects.filter(course=course).count()
        data.append({
            "course_title": course.title,
            "required_skills": required_skills,
            "gained_skills": gained_skills
        })
    return JsonResponse({"course_skills_comparison": data})


# Statistic 4: The number of courses offered by each department, broken down by year or month
def statistic_4(request):
    data = {}
    departments = Department.objects.all()
    for department in departments:
        yearly_data = Course.objects.filter(department=department).annotate(year=TruncYear('contract_start_date')).values('year').annotate(course_count=Count('id'))
        monthly_data = Course.objects.filter(department=department).annotate(month=TruncMonth('contract_start_date')).values('month').annotate(course_count=Count('id'))
        data[department.name] = {
            "yearly": list(yearly_data),
            "monthly": list(monthly_data)
        }
    return JsonResponse({"courses_by_department": data})


# Statistic 5: Counts the total number of days a professor worked
def statistic_5(request, id_employee):
    try:
        professor = Professor.objects.get(id=id_employee)
    except Professor.DoesNotExist:
        return JsonResponse({"error": "Professor not found"}, status=404)
    
    # Calculate unique working days
    unique_working_days = CourseProfessor.objects.filter(professor=professor).values_list('assignment_date', flat=True).distinct()
    working_days_count = len(unique_working_days)

    return JsonResponse({
        "professor_name": f"{professor.first_name} {professor.last_name}",
        "working_days": working_days_count
    })

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count

# Render the main page
def statistics_view(request):
    departments = Department.objects.all()
    return render(request, 'statistics.html', {'departments': departments})

from django.http import JsonResponse
from .models import Department, Course

def statistic_data(request, department_id):
    print(f"Fetching data for department_id={department_id}")
    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        print("Department not found")
        return JsonResponse({"error": "Department not found"}, status=404)

    courses_count = Course.objects.filter(department=department).count()
    
    data = {
        "department_name": department.name,
        "labels": ["Course Count"],
        "values": [courses_count],
    }
    print(f"Data: {data}")
    return JsonResponse(data)



def department_dropdown(request):
    departments = Department.objects.all()
    print(departments)  # This will show the queryset in your console
    return render(request, 'listings/dashboard.html', {'departments': departments})



# ~/projects/django-web-app/merchex/listings/views.py
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect


from django.core.files.storage import default_storage
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import pandas as pd
from datetime import datetime
from collections import defaultdict
from datetime import datetime
from openpyxl import Workbook

from dateutil.relativedelta import relativedelta
from reportlab.lib.pagesizes import A4




# login views

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'listings/homePage.html')

def signup(request):
    return render(request, 'listings/signup.html')






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
import json
from .models import AdminProfile, Course, Professor

@method_decorator(csrf_exempt, name='dispatch')
class CourseListView(View):
    def get(self, request):
        """Get all courses."""
        courses = list(Course.objects.values())
        return JsonResponse(courses, safe=False)

    def post(self, request):
        """Create a new course."""
        try:
            data = json.loads(request.body)
            course = Course.objects.create(
                title=data.get('title'),
                department_id=data.get('department'),
                is_completed=data.get('is_completed', False),
                course_manager_email=data.get('course_manager_email'),
                client_company_name=data.get('client_company_name'),
                contract_number=data.get('contract_number'),
                invoice_status=data.get('invoice_status'),
                contract_start_date=data.get('contract_start_date'),
                approval_status=data.get('approval_status'),
            )
            return JsonResponse({"id": course.id, "message": "Course created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class CourseDetailView(View):
    def get(self, request, id):
        """Get a course by ID."""
        try:
            course = Course.objects.values().get(id=id)
            return JsonResponse(course, safe=False)
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course not found"}, status=404)

    def put(self, request, id):
        """Update a course by ID."""
        try:
            data = json.loads(request.body)
            course = Course.objects.get(id=id)
            course.title = data.get('title', course.title)
            course.department_id = data.get('department', course.department_id)
            course.is_completed = data.get('is_completed', course.is_completed)
            course.course_manager_email = data.get('course_manager_email', course.course_manager_email)
            course.client_company_name = data.get('client_company_name', course.client_company_name)
            course.contract_number = data.get('contract_number', course.contract_number)
            course.invoice_status = data.get('invoice_status', course.invoice_status)
            course.contract_start_date = data.get('contract_start_date', course.contract_start_date)
            course.approval_status = data.get('approval_status', course.approval_status)
            course.save()
            return JsonResponse({"message": "Course updated successfully"})
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, id):
        """Delete a course by ID."""
        try:
            course = Course.objects.get(id=id)
            course.delete()
            return JsonResponse({"message": "Course deleted successfully"})
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course not found"}, status=404)



@method_decorator(csrf_exempt, name='dispatch')
class ProfessorListView(View):
    def get(self, request):
        """Get all professors."""
        professors = list(Professor.objects.values())
        return JsonResponse(professors, safe=False)

    def post(self, request):
        """Create a new professor."""
        try:
            data = json.loads(request.body)
            professor = Professor.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                hire_date=data.get('hire_date'),
                is_active=data.get('is_active', True),
                password=data.get('password'),
                birth_date=data.get('birth_date'),
                phone_number=data.get('phone_number'),
                salary=data.get('salary'),
                professor_number=data.get('professor_number')
            )
            return JsonResponse({"id": professor.id, "message": "Professor created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ProfessorDetailView(View):
    def get(self, request, id):
        """Get a professor by ID."""
        try:
            professor = Professor.objects.values().get(id=id)
            return JsonResponse(professor, safe=False)
        except Professor.DoesNotExist:
            return JsonResponse({"error": "Professor not found"}, status=404)

    def put(self, request, id):
        """Update a professor by ID."""
        try:
            data = json.loads(request.body)
            professor = Professor.objects.get(id=id)
            professor.first_name = data.get('first_name', professor.first_name)
            professor.last_name = data.get('last_name', professor.last_name)
            professor.email = data.get('email', professor.email)
            professor.hire_date = data.get('hire_date', professor.hire_date)
            professor.is_active = data.get('is_active', professor.is_active)
            professor.password = data.get('password', professor.password)
            professor.birth_date = data.get('birth_date', professor.birth_date)
            professor.phone_number = data.get('phone_number', professor.phone_number)
            professor.salary = data.get('salary', professor.salary)
            professor.professor_number = data.get('professor_number', professor.professor_number)
            professor.save()
            return JsonResponse({"message": "Professor updated successfully"})
        except Professor.DoesNotExist:
            return JsonResponse({"error": "Professor not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, id):
        """Delete a professor by ID."""
        try:
            professor = Professor.objects.get(id=id)
            professor.delete()
            return JsonResponse({"message": "Professor deleted successfully"})
        except Professor.DoesNotExist:
            return JsonResponse({"error": "Professor not found"}, status=404)
        
    
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminProfile, Professor
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Get 'next' URL from the query parameter or form data
        next_url = request.POST.get('next', request.GET.get('next', '/admin_profile/'))  # Default for admin profile

        # Validate inputs
        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'listings/login.html')

        # Admin login (unchanged)
        try:
            admin = AdminProfile.objects.get(email=email)
            if admin.password == password:
                request.session['user_role'] = 'admin'
                request.session['user_email'] = email
                logger.info(f"Admin {email} logged in.")
                return HttpResponseRedirect(next_url)
            else:
                messages.error(request, "Incorrect password for Admin.")
                return render(request, 'listings/login.html')
        except AdminProfile.DoesNotExist:
            pass

@login_required
def admin_profile_view(request):
    if request.session.get('user_role') != 'admin':
        logger.warning("Unauthorized access attempt to Admin Profile.")
        return redirect('login')

    try:
        admin = AdminProfile.objects.get(email=request.session.get('user_email'))
        logger.info(f"Admin profile loaded for {admin.email}.")
    except AdminProfile.DoesNotExist:
        messages.error(request, "Admin not found.")
        return redirect('login')

    return render(request, 'listings/admin_profile.html', {'admin': admin})@login_required
def admin_profile_view(request):
    if request.session.get('user_role') != 'admin':
        logger.warning("Unauthorized access attempt to Admin Profile.")
        return redirect('login')

    try:
        admin = AdminProfile.objects.get(email=request.session.get('user_email'))
        logger.info(f"Admin profile loaded for {admin.email}.")
    except AdminProfile.DoesNotExist:
        messages.error(request, "Admin not found.")
        return redirect('login')

    return render(request, 'listings/admin_profile.html', {'admin': admin})



from django.shortcuts import render, get_object_or_404
from .models import Professor

def professor_profile_view(request, id):
    # Fetch professor by ID
    professor = get_object_or_404(Professor, id=id)

    return render(request, 'listings/professor_profile.html', {'professor': professor})



from .models import Course

def professor_courses_view(request, id):
    # Fetch professor by ID
    professor = get_object_or_404(Professor, id=id)

    # Get all courses assigned to this professor
    courses = professor.courseprofessor_set.all()  # Assuming a relationship exists

    return render(request, 'listings/professor_courses.html', {'professor': professor, 'courses': courses})

def professor_course_detail_view(request, professor_id, course_id):
    # Fetch professor by ID
    professor = get_object_or_404(Professor, id=professor_id)

    # Fetch specific course by course ID
    course = get_object_or_404(professor.courseprofessor_set, id=course_id)

    return render(request, 'listings/professor_course_detail.html', {'professor': professor, 'course': course})

