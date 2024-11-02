from django.contrib.auth import get_user_model
from .models import Employee,Department,Kin, Leave, Recruitment, JobPost,TrainingProgram, Event, Attendance, Head_of_department
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.core import validators
from django.utils import timezone
from django.db.models import Q
import time
from django.forms import ModelForm, DateInput, inlineformset_factory, HiddenInput


class RegistrationForm (UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Valid Email is required'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))
    class Meta:
        model = get_user_model()
        fields = ('username','email','password1', 'password2')

class LoginForm(AuthenticationForm):
   username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True, 'placeholder':'Username Here', 'class':'form-control'}))
   password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'********'}))

class EmployeeForm (forms.ModelForm):
    first_name = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    mobile = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Valid Email'}))
    emergency = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Relative Mobile Number'}))
    gender = forms.ChoiceField(choices=Employee.GENDER,widget=forms.Select(attrs={'class':'form-control'}))
    department = forms.ModelChoiceField(Department.objects.all(),required=True, empty_label='Select a department',widget=forms.Select(attrs={'class':'form-control'}))
    language = forms.ChoiceField(choices=Employee.LANGUAGE,widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'mobile','email','emergency','salary','gender','department','bank','nuban','language')
        widgets={
            'salary':forms.TextInput(attrs={'class':'form-control'}),
            'bank':forms.TextInput(attrs={'class':'form-control'}),
            'nuban':forms.TextInput(attrs={'class':'form-control'})
        }

class KinForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    occupation = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    employee = forms.ModelChoiceField(Employee.objects.filter(kin__employee=None),required=False,widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Kin
        fields = '__all__'
    
class Attendanceform(ModelForm):
    class Meta:
        model = Attendance
        widgets = {'employee' : HiddenInput}
        fields = ('employee','attendance','head_of_department')
AttendanceFormset = inlineformset_factory(Head_of_department,Attendance,form=Attendanceform,fields=('attendance','employee'))

class DepartmentForm(forms.ModelForm):
    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Department Name'}))
    history = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Brief Department History'}))
    
    class Meta:
        model = Department
        fields = '__all__'

class CalendarCreate(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    duration = forms.IntegerField(label='Duration (hours)')
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'class': 'datepicker'}))

class EventForm(forms.ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

   
class LeaveForm (forms.ModelForm):

    class Meta:
        model = Leave
        fields = '__all__'

        widgets={
            'start': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'end': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'employee':forms.Select(attrs={'class':'form-control'}),
        }

class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = Recruitment
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control mt-2'}),
            'education': forms.Textarea(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control'}),
            'certifications': forms.Textarea(attrs={'class': 'form-control'}),
        }

class JobPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs['readonly'] = True

    class Meta:
        model = JobPost
        fields = ['role', 'description']
        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Make the field readonly
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description'})
        }

class TrainingProgramForm(forms.ModelForm):
    employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = TrainingProgram
        fields = ['name', 'duration', 'employees']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
