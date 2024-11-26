from django.db import models

# Department model
class Department(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    department_code = models.TextField(null=True, blank=True)
    created_date = models.TextField(null=True, blank=True)
    phone_number = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name


# GainedSkill model
class GainedSkill(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


# RequiredSkill model
class RequiredSkill(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


# Professor model
class Professor(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    hire_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(null=True)
    password = models.TextField()
    birth_date = models.TextField(null=True, blank=True)
    phone_number = models.TextField(null=True, blank=True)
    salary = models.TextField(null=True, blank=True)
    professor_number = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# Course model
class Course(models.Model):
    title = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(null=True)
    course_manager_email = models.EmailField(null=True, blank=True)
    client_company_name = models.TextField(null=True, blank=True)
    contract_number = models.TextField(null=True, blank=True)
    invoice_status = models.TextField(null=True, blank=True)
    contract_start_date = models.DateField(null=True, blank=True)  # Change this to DateField
    approval_status = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title



# CourseGainedSkill model (Many-to-Many between Course and GainedSkill)
class CourseGainedSkill(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    gained_skill = models.ForeignKey(GainedSkill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'gained_skill')


# CourseProfessor model (Many-to-Many between Course and Professor with assignment dates)
class CourseProfessor(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    assignment_date = models.DateTimeField()
    finish_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('course', 'professor', 'assignment_date')


# CourseRequiredSkill model (Many-to-Many between Course and RequiredSkill)
class CourseRequiredSkill(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    required_skill = models.ForeignKey(RequiredSkill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'required_skill')




# Dataset model
class Dataset(models.Model):
    school_department = models.CharField(max_length=255, null=True, blank=True)
    course_title = models.CharField(max_length=255, null=True, blank=True)
    date_and_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    required_skill = models.CharField(max_length=255, null=True, blank=True)
    professors = models.CharField(max_length=255, null=True, blank=True)
    gained_skill = models.CharField(max_length=355, null=True, blank=True)

    def __str__(self):
        return f"Dataset for {self.course_title} - {self.school_department}"





# Dataset model
class Dataset(models.Model):
    school_department = models.CharField(max_length=255, null=True, blank=True)
    course_title = models.CharField(max_length=255, null=True, blank=True)
    date_and_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    required_skill = models.CharField(max_length=255, null=True, blank=True)
    professors = models.CharField(max_length=255, null=True, blank=True)
    gained_skill = models.CharField(max_length=355, null=True, blank=True)

    def _str_(self):
        return f"Dataset for {self.course_title} - {self.school_department}"



class AdminProfile(models.Model):
    admin_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # For simplicity, we'll keep this as plain text, but should be hashed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.admin_name






    