from django.shortcuts import render,redirect, resolve_url,reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models  import Employee, Department,Kin, Leave, Recruitment, JobPost, Performance, TrainingProgram
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView,View,DetailView,TemplateView,ListView,UpdateView,DeleteView
from .forms import RegistrationForm,LoginForm,EmployeeForm,KinForm,DepartmentForm, LeaveForm, RecruitmentForm, Attendanceform, JobPostForm, EventForm, TrainingProgramForm, CalendarCreate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Avg
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
# import plotly.graph_objs as go
from django.views.generic import RedirectView
from datetime import datetime
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import date, timedelta
import calendar
from django.forms import modelformset_factory


from .models import *
from .utils import Calendar

# Create your views here.
#Login 



class Index(TemplateView):
   template_name = 'hrms/home/home.html'

#   Authentication
class Register (CreateView):
    model = get_user_model()
    form_class  = RegistrationForm
    template_name = 'hrms/registrations/register.html'
    success_url = reverse_lazy('hrms:login')
    
class Login_View(LoginView):
    model = get_user_model()
    form_class = LoginForm
    template_name = 'hrms/registrations/login.html'

    def get_success_url(self):
        url = resolve_url('hrms:loginhome')
        return url

class Logout_View(View):

    def get(self,request):
        logout(self.request)
        return redirect ('hrms:login',permanent=True)
    
class LoginHomeView(TemplateView):
    template_name = 'hrms/loginhome/index.html'  # Path to your index.html containing the chatbot interface
    login_url = 'hrms:login'

 # Main Board   
class Dashboard(LoginRequiredMixin,ListView):
    template_name = 'hrms/dashboard/index.html'
    login_url = 'hrms:login'
    model = get_user_model()
    context_object_name = 'qset'            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['emp_total'] = Employee.objects.all().count()
        context['dept_total'] = Department.objects.all().count()
        context['admin_count'] = get_user_model().objects.all().count()
        context['workers'] = Employee.objects.order_by('-id')
        return context

# Employee's Controller
class Employee_New(LoginRequiredMixin,CreateView):
    model = Employee  
    form_class = EmployeeForm  
    template_name = 'hrms/employee/create.html'
    login_url = 'hrms:login'
    success_url = reverse_lazy('hrms:employee_all')
    
class Employee_All(LoginRequiredMixin,ListView):
    template_name = 'hrms/employee/index.html'
    model = Employee
    login_url = 'hrms:login'
    context_object_name = 'employees'
    paginate_by  = 5
    
class Employee_View(LoginRequiredMixin,DetailView):
    queryset = Employee.objects.select_related('department')
    template_name = 'hrms/employee/single.html'
    context_object_name = 'employee'
    login_url = 'hrms:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            query = Kin.objects.get(employee=self.object.pk)
            context["kin"] = query
            return context
        except ObjectDoesNotExist:
            return context
        
class Employee_Update(LoginRequiredMixin,UpdateView):
    model = Employee
    template_name = 'hrms/employee/edit.html'
    form_class = EmployeeForm
    login_url = 'hrms:login'
    success_url = reverse_lazy('hrms:employee_all')
    
    
class Employee_Delete(LoginRequiredMixin, View):
    login_url = 'hrms:login'

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)  # Retrieve the Employee object
            employee.delete()  # Delete the Employee object from the database
        except Employee.DoesNotExist:  # Handle the case where the Employee does not exist
            pass  # You can handle this case differently based on your requirements
        return redirect('hrms:employee_all')  # Redirect to the employee list

class Employee_Kin_Add (LoginRequiredMixin,CreateView):
    model = Kin
    form_class = KinForm
    template_name = 'hrms/employee/kin_add.html'
    login_url = 'hrms:login'
   

    def get_context_data(self):
        context = super().get_context_data()
        if 'id' in self.kwargs:
            emp = Employee.objects.get(pk=self.kwargs['id'])
            context['emp'] = emp
            return context
        else:
            return context

class Employee_Kin_Update(LoginRequiredMixin,UpdateView):
    model = Kin
    form_class = KinForm
    template_name = 'hrms/employee/kin_update.html'
    login_url = 'hrms:login'

    def get_initial(self):
        initial = super(Employee_Kin_Update,self).get_initial()
        
        if 'id' in self.kwargs:
            emp =  Employee.objects.get(pk=self.kwargs['id'])
            initial['employee'] = emp.pk
            
            return initial

#Department views

class Department_Detail(LoginRequiredMixin, ListView):
    context_object_name = 'employees'
    template_name = 'hrms/department/single.html'
    login_url = 'hrms:login'
    def get_queryset(self): 
        queryset = Employee.objects.filter(department=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dept"] = Department.objects.get(pk=self.kwargs['pk']) 
        return context
    
class Department_New (LoginRequiredMixin,CreateView):
    model = Department
    template_name = 'hrms/department/create.html'
    form_class = DepartmentForm
    login_url = 'hrms:login'

class Department_Update(LoginRequiredMixin,UpdateView):
    model = Department
    template_name = 'hrms/department/edit.html'
    form_class = DepartmentForm
    login_url = 'hrms:login'
    success_url = reverse_lazy('hrms:dashboard')


    
class CreateCalendarEvent(FormView):
    template_name = 'hrms/calendar/create.html'
    form_class = CalendarCreate
    success_url = reverse_lazy('hrms:calendar')

    def form_valid(self, form):
        # Process the form data (save to the database, etc.)
        # Access cleaned data directly from the form instance
        name = form.cleaned_data['name']
        duration = form.cleaned_data['duration']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        print(f'Name: {name}, Duration: {duration}, Start Date: {start_date}, End Date: {end_date}')
        # Redirect to the success page
        return super().form_valid(form)

#Attendance View
class Attendancecreate(CreateView):
    model = Attendance
    form_class = Attendanceform
    success_url = reverse_lazy('hrms:dashboard')

    def get_context_data(self,** kwargs):
        context = super(Attendancecreate, self).get_context_data(**kwargs)
        context['formset'] = AttendanceFormset(queryset=Attendance.objects.none(), instance=Head_of_department.objects.get(email=self.request.user.email), initial=[{'employee': employee} for employee in self.get_initial()['employee']])
        return context

    def get_initial(self):
        email = self.request.user.email
        head_of_department = Head_of_department.objects.get(email=email)
        initial = super(Attendancecreate , self).get_initial()
        initial['employee'] = Employee.objects.filter(head_of_department=head_of_department)
        return initial

    def post(self, request, *args, **kwargs,):
        formset = AttendanceFormset(request.POST,queryset=Attendance.objects.none(), instance=Head_of_department.objects.get(email=self.request.user.email), initial=[{'employee': employee} for employee in self.get_initial()['employee']])
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self,formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.head_of_department = get_object_or_404(Head_of_department, email=self.request.user.email)
            instance.save()
        return HttpResponseRedirect('hrms/dashboard/index.html')


   

class LeaveNew (LoginRequiredMixin,CreateView, ListView):
    model = Leave
    template_name = 'hrms/leave/create.html'
    form_class = LeaveForm
    login_url = 'hrms:login'
    success_url = reverse_lazy('hrms:leave_new')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leaves"] = Leave.objects.all()
        return context

class Payroll(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'hrms/payroll/index.html'
    login_url = 'hrms:login'
    context_object_name = 'stfpay'
    success_url = reverse_lazy('hrms:leave_new')



class RecruitmentNew(CreateView):
    model = Recruitment
    template_name = 'hrms/recruitment/index.html'
    form_class = RecruitmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_job_post = JobPost.objects.latest('id')
        context['job_role'] = latest_job_post.role
        context['job_description'] = latest_job_post.description
        context['form'] = RecruitmentForm()  # Add this line if the form is used in the template
        return context
    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:

        print(request.POST)
        form =  RecruitmentForm(request.POST,request.FILES)
        print(form,"form")
        return super().post(request, *args, **kwargs)
        
    success_url ="/"

# class RecruitmentCreateView(LoginRequiredMixin, CreateView):
#     model = JobPost
#     form_class = JobPostForm
#     template_name = 'hrms/recruitment/create_job.html'  # Update the template path as needed
#     login_url = 'hrms:login'
#     success_url = reverse_lazy('hrms:recruitmentall')

class RecruitmentCreateView(CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'hrms/recruitment/create_job.html'  # Update with your actual template path
    success_url = reverse_lazy('hrms:recruitmentall')  # Update with your desired success URL

    def form_valid(self, form):
        # Set status to 'Pending' before saving the form
        form.instance.status = 'Pending'
        return super().form_valid(form)


class RecruitmentAll(LoginRequiredMixin,ListView):
    model = Recruitment
    login_url = 'hrms:login'
    template_name = 'hrms/recruitment/all.html'
    context_object_name = 'recruit'

class ManageApplicationView(DetailView):
    model = Recruitment
    template_name = 'hrms/recruitment/manage.html'
    context_object_name = 'candidate'

class ShortlistCandidateView(View):
    def post(self, request, pk):
        candidate = Recruitment.objects.get(pk=pk)
        candidate.status = 'Shortlisted'
        candidate.save()
        return redirect(reverse_lazy('hrms:recruitmentall'))
    
class RecruitmentDelete (LoginRequiredMixin,View):
    login_url = 'hrms:login'
    def get (self, request,pk):
     form_app = Recruitment.objects.get(pk=pk)
     form_app.delete()
     return redirect('hrms:recruitmentall', permanent=True)

class Pay(LoginRequiredMixin,ListView):
    model = Employee
    template_name = 'hrms/payroll/index.html'
    context_object_name = 'emps'
    login_url = 'hrms:login'

class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'hrms/analytics/index.html'
    login_url = 'hrms:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get total number of employees
        context['total_employees'] = Employee.objects.all().count()

        # Get total number of employees present today
        context['total_attendence'] = Attendance.objects.filter(date=timezone.localdate(), status='PRESENT').count()

        # Get total number of leave applications
        context['total_leave_applications'] = Leave.objects.all().count()

        context['avg_performance_rating'] = Performance.objects.aggregate(avg_rating=Avg('performance_rating'))['avg_rating']

        # Calculate total goal completion count
        context['total_goal_completion'] = Performance.objects.filter(goal_status='Completed').count()

        # Calculate total training programs attended
        context['total_training_programs_attended'] = Performance.objects.exclude(training_programs_attended='').count()

        performances = Performance.objects.all()
        employee_names = [performance.employee.username for performance in performances]
        performance_ratings = [performance.performance_rating for performance in performances]

        data = [
            go.Bar(
                x=employee_names,
                y=performance_ratings,
                marker=dict(color='rgb(26, 118, 255)'),
            )
        ]

        layout = go.Layout(
            title='Performance Ratings of Employees',
            xaxis=dict(title='Employee'),
            yaxis=dict(title='Performance Rating'),
        )

        chart = go.Figure(data=data, layout=layout)
        chart_html = chart.to_html(full_html=False)

        context['performance_chart'] = chart_html

        return context
    

    
class TrainingProgramListView(ListView):
    model = TrainingProgram
    template_name = 'hrms/training/index.html'
    context_object_name = 'training_programs'

class TrainingProgramCreateView(CreateView):
    model = TrainingProgram
    form_class = TrainingProgramForm
    template_name = 'hrms/training/add.html'
    success_url = reverse_lazy('hrms:training_list')  # Specify the URL name for success redirect

    def form_valid(self, form):
        # Do any additional processing if needed
        return super().form_valid(form)
    
    
class EditTrainingProgram(UpdateView):
    model = TrainingProgram
    form_class = TrainingProgramForm
    template_name = 'hrms/training/edit.html'
    success_url = reverse_lazy('hrms:training_list')

    def get_object(self, queryset=None):
        program_id = self.kwargs.get('program_id')
        return get_object_or_404(TrainingProgram, pk=program_id)
    
class DeleteTrainingProgram(DeleteView):
    model = TrainingProgram
    success_url = reverse_lazy('training_program_list')  # Redirect to the list of training programs after deletion

    def get_object(self, queryset=None):
        program_id = self.kwargs.get('program_id')
        return get_object_or_404(TrainingProgram, pk=program_id)
    
class CalendarView(generic.ListView):
    model = Event
    template_name = 'hrms/cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('day', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        
        events = Event.objects.filter(start_time__year=d.year, start_time__month=d.month)
        context['events'] = events
        # Get the current month
        current_month = d.month
        current_year = d.year

        # Calculate previous month
        prev_month = current_month - 1
        prev_year = current_year
        if prev_month == 0:
            prev_month = 12
            prev_year -= 1

        # Calculate next month
        next_month = current_month + 1
        next_year = current_year
        if next_month == 13:
            next_month = 1
            next_year += 1

        # Construct URLs for previous and next month
        context['prev_month'] = f'day={prev_year}-{prev_month}'
        context['next_month'] = f'day={next_year}-{next_month}'

        return context


    
       


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()    

def base_view(request):
     # Your context data here (if any)
     context = {}
     return render(request, 'hrms/cal/base.html', context)

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

# def event(request, event_id=None):
#     instance = Event()
#     if event_id:
#         instance = get_object_or_404(Event, pk=event_id)
#     else:
#         instance = Event()
    
#     form = EventForm(request.POST or None, instance=instance)
#     if request.POST and form.is_valid():
#         form.save()
#         return HttpResponseRedirect(reverse('hrms:calendar'))
#     return render(request, 'hrms/cal/event.html', {'form': form})

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=instance)
        if form.is_valid():
            event = form.save()
            return HttpResponseRedirect(reverse('hrms:calendar'))
    else:
        form = EventForm(instance=instance)
    
    return render(request, 'hrms/cal/event.html', {'form': form})
# class CalendarView(generic.ListView):
#     model = Event
#     template_name = 'hrms/cal/calendar.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['calendar'] = self.get_calendar()
#         return context

#     def get_calendar(self):
#         # use today's date for the calendar
#         d = self.get_date(self.request.GET.get('day'))

#         # Instantiate our calendar class with today's year and date
#         cal = Calendar(d.year, d.month)

#         # Call the formatmonth method, which returns our calendar as a table
#         html_cal = cal.formatmonth(withyear=True)
#         return mark_safe(html_cal)

#     def get_date(self, req_day):
#         if req_day:
#             year, month = (int(x) for x in req_day.split('-'))
#             return datetime(year, month, day=1)
#         return datetime.today()    

"""def prev_month(request):
     current_month = datetime.strptime(request.GET.get('day'), '%Y-%m')
     prev_month = current_month - timedelta(days=1)
     return redirect(reverse('hrms/cal:calendar') + f'?day={prev_month.strftime("%Y-%m")}')"""

# def next_month(request):
#     current_month = datetime.strptime(request.GET.get('day'), '%Y-%m')
#     next_month = current_month + timedelta(days=32)
#     return redirect(reverse('cal:calendar') + f'?day={next_month.strftime("%Y-%m")}')