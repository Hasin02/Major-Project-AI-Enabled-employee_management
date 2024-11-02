from django.urls import path
from django.conf.urls import url

from . import views
app_name = 'hrms'
urlpatterns = [
    
#Calendar


    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('base/', views.base_view, name='base'),
    path('prev-month/', views.prev_month, name='prev_month'),
    path('next-month/', views.next_month, name='next_month'),
    path('event/new/$', views.event, name='event_new'),
    path('edit/<int:event_id>/', views.event, name='event_edit'),


# Authentication Routes
    path('', views.Index.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='reg'),
    path('login/', views.Login_View.as_view(), name='login'),
    path('logout/', views.Logout_View.as_view(), name='logout'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('loginhome/', views.LoginHomeView.as_view(), name='loginhome'),

# Employee Routes
    path('dashboard/employee/', views.Employee_All.as_view(), name='employee_all'),
    path('dashboard/employee/new/', views.Employee_New.as_view(), name='employee_new'),
    path('dashboard/employee/<int:pk>/view/', views.Employee_View.as_view(), name='employee_view'),
    path('dashboard/employee/<int:pk>/update/', views.Employee_Update.as_view(), name='employee_update'),
    path('dashboard/employee/<int:pk>/delete/', views.Employee_Delete.as_view(), name='employee_delete'),
    path('dashboard/employee/<int:id>/kin/add/', views.Employee_Kin_Add.as_view(), name='kin_add'),
    path('dashboard/employee/<int:id>/kin/<int:pk>/update/', views.Employee_Kin_Update.as_view(), name='kin_update'),

#Department Routes
    path('dashboard/department/<int:pk>/', views.Department_Detail.as_view(), name='dept_detail'),
    path('dashboard/department/add/', views.Department_New.as_view(), name='dept_new'),
    path('dashboard/department/<int:pk>/update/', views.Department_Update.as_view(), name='dept_update'),


#Attendance Routes
    path('dashboard/attendence/', views.Attendancecreate.as_view(), name='attendance'),



#Leave Routes

    path("dashboard/leave/new/", views.LeaveNew.as_view(), name="leave_new"),

#Recruitment
    path('recruitment/new/', views.RecruitmentCreateView.as_view(), name='recruitment_new'),  # Add this line
    path("recruitment/",views.RecruitmentNew.as_view(), name="recruitment"),
    path("recruitment/all/",views.RecruitmentAll.as_view(), name="recruitmentall"),
    path("recruitment/<int:pk>/delete/", views.RecruitmentDelete.as_view(), name="recruitment_delete"),
    path('manage/<int:pk>/', views.ManageApplicationView.as_view(), name='recruitment_manage'),
    path('shortlist/<int:pk>/', views.ShortlistCandidateView.as_view(), name='shortlist_candidate'),


#Payroll
    path("employee/pay/",views.Pay.as_view(), name="payroll"),



#Analytics 
path('analytics/', views.AnalyticsView.as_view(), name='analytics'),

#Training
path('training-programs/', views.TrainingProgramListView.as_view(), name='training_list'),
path('training-programs/create', views.TrainingProgramCreateView.as_view(), name='training_create'),
path('edit/<int:program_id>/', views.EditTrainingProgram.as_view(), name='training_edit'),
path('delete/<int:program_id>/', views.DeleteTrainingProgram.as_view(), name='training_delete'),




]



