from django.db import models
from django.contrib.auth import get_user_model

import random
from django.urls import reverse
from django.utils import timezone
import time
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=70, null=False, blank=False)
    history = models.TextField(max_length=1000,null=True,blank=True, default='No History')
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("hrms:dept_detail", kwargs={"pk": self.pk})
    

class Employee(models.Model):
    LANGUAGE = (('english','ENGLISH'),('yoruba','YORUBA'),('hausa','HAUSA'),('french','FRENCH'))
    GENDER = (('male','MALE'), ('female', 'FEMALE'),('other', 'OTHER'))
    emp_id = models.CharField(max_length=70, default='emp'+str(random.randrange(100,999,1)))
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=125, null=False)
    address = models.TextField(max_length=100, default='')
    emergency = models.CharField(max_length=11)
    gender = models.CharField(choices=GENDER, max_length=10)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL, null=True)
    joined = models.DateTimeField(default=timezone.now)
    language = models.CharField(choices=LANGUAGE, max_length=10, default='english')
    nuban = models.CharField(max_length=10, default='0123456789')
    bank = models.CharField(max_length=25, default='First Bank Plc')
    salary = models.CharField(max_length=16,default='00,000.00')      
    def __str__(self):
        return self.first_name
        
    def get_absolute_url(self):
        return reverse("hrms:employee_view", kwargs={"pk": self.pk})
    head_of_department = models.ForeignKey('Head_of_department', on_delete=models.SET_NULL, blank=True, null=True)

    
attendance_choices = (
    ('absent', 'Absent'),
    ('present', 'Present')
)

class Head_of_department(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name 



class Attendance(models.Model):
    head_of_department = models.ForeignKey('Head_of_department', on_delete=models.SET_NULL, blank=True, null=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, )
    attendance = models.CharField(max_length=8, choices=attendance_choices, blank=True)
    

class Kin(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.TextField(max_length=100)
    occupation = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)
    employee = models.OneToOneField(Employee,on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.first_name+'-'+self.last_name
    
    def get_absolute_url(self):
        return reverse("hrms:employee_view",kwargs={'pk':self.employee.pk})
    



class Leave (models.Model):
    STATUS = (('approved','APPROVED'),('unapproved','UNAPPROVED'),('decline','DECLINED'))
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    start = models.CharField(blank=False, max_length=15)
    end = models.CharField(blank=False, max_length=15)
    status = models.CharField(choices=STATUS,  default='Not Approved',max_length=15)

    def __str__(self):
        return self.employee + ' ' + self.start

class Recruitment(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    phone = models.CharField(max_length=11)
    education = models.TextField(max_length=100,default='')  # New field
    skills = models.TextField(max_length=100,default='')     # New field
    certifications = models.TextField(default='')  # Default value added here
    resume = models.FileField(upload_to='resumes/')

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

class JobPost(models.Model):
    role = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.role

class ShortlistedApplication(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    resume = models.FileField(upload_to='shortlisted_resumes/')

    def __str__(self):
        return f"{self.name} - {self.role}"
    
    
    
class Task(models.Model):
    STATUS_CHOICES = (
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Not Started', 'Not Started'),
    )

    name = models.CharField(max_length=100)
    progress = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    team = models.ManyToManyField(Employee)

    def __str__(self):
        return self.name

    
class Performance(models.Model):
    employee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    performance_rating = models.PositiveSmallIntegerField(default=0)
    feedback = models.TextField(blank=True)
    goal_description = models.CharField(max_length=255, blank=True)
    goal_target_completion_date = models.DateField(null=True, blank=True)
    goal_actual_completion_date = models.DateField(null=True, blank=True)
    goal_status = models.CharField(max_length=50, blank=True)
    project_name = models.CharField(max_length=100, blank=True)
    project_role = models.CharField(max_length=100, blank=True)
    project_duration = models.CharField(max_length=50, blank=True)
    project_achievements = models.TextField(blank=True)
    project_impact = models.TextField(blank=True)
    skill_assessments = models.TextField(blank=True)
    training_programs_attended = models.TextField(blank=True)
    certifications_obtained = models.TextField(blank=True)
    skill_proficiency_levels = models.TextField(blank=True)
    feedback_comments = models.TextField(blank=True)
    recognition_awards = models.TextField(blank=True)
    commendations = models.TextField(blank=True)
    customer_feedback_ratings = models.TextField(blank=True)
    service_response_times = models.CharField(max_length=50, blank=True)
    resolution_rates = models.CharField(max_length=50, blank=True)
    error_rates = models.CharField(max_length=50, blank=True)
    accuracy_levels = models.CharField(max_length=50, blank=True)
    adherence_to_standards = models.CharField(max_length=50, blank=True)
    leadership_roles_held = models.TextField(blank=True)
    team_projects_led = models.TextField(blank=True)
    team_performance_evaluations = models.TextField(blank=True)
    collaboration_feedback = models.TextField(blank=True)
    ideas_proposed = models.TextField(blank=True)
    initiatives_implemented = models.TextField(blank=True)
    process_improvements = models.TextField(blank=True)
    innovation_projects_contributed = models.TextField(blank=True)
    adaptability_change_initiatives = models.TextField(blank=True)
    overcoming_obstacles = models.TextField(blank=True)
    resilience_demonstrations = models.TextField(blank=True)
    engagement_scores = models.TextField(blank=True)
    retention_rates = models.CharField(max_length=50, blank=True)
    turnover_reasons = models.TextField(blank=True)
    exit_interview_feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee}'s Performance on {self.task}"
    
class TrainingProgram(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    employees = models.ManyToManyField(Employee,blank=True)

    def __str__(self):
        return self.name
    
    @property
    def all_employees(self):
       return  ", ".join([x.first_name+" "+x.last_name for x in self.employees.all()])
# calander

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()   
    
    @property
    def get_html_url(self):
        url = reverse('hrms:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    