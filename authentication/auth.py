# from msilib.schema import Error
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import *
from .forms import *
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView
from .forms import UserGroupForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from .notification import *
from django.core.files.storage import FileSystemStorage
# from appsystem.models import *
import os
from .utils import *
from io import BytesIO
from .filters import UserFilter



def login_view(request):
       
    form = UserLoginForm()
    if request.method == 'POST':
        # create an instance the UserLoginForm in the form.py passing in request.Post or None as an argument
        form = UserLoginForm(request.POST)
        if form.is_valid():  # if the data passed to the UserLoginForm in the form.py is passes all the clean data methods
            # get the username form the already clearned data in UserLoginForm class in the form.py and store it into a varible called username
           email = form.cleaned_data.get('email')
            # get the password form the already clearned data in UserLoginForm class in the form.py and store it into a varible called password
           password = form.cleaned_data.get('password')
            # re-authenticate the username and password and store it into variable called user
           user = authenticate(username=email, password=password)
           print(user)
           if user is not None:
               login(request, user)
               if user.is_authenticated and user.is_active and  user.status == 'Pending' and user.is_applicant  and  not user.is_new:
                    messages.success(request, 'Login Successful')
                    return redirect('authentication:biodata',user.id)
               elif user.is_authenticated and user.is_active and  user.status == 'Submitted' and user.is_applicant and  not user.is_new:
                   messages.success(request, 'Login Successful')
                   return redirect('authentication:application-overview',user.id)

               elif user.is_authenticated and user.is_active and not user.is_applicant and  not user.is_new:
                   messages.success(request, 'Login Successful')
                   return redirect('authentication:applicants')

               elif user.is_authenticated and user.is_active and user.is_new and  user.status == 'Pending' and user.is_applicant:
                    return redirect("authentication:change-password", user.id)
               elif user.is_authenticated and not user.is_active:
                    messages.info(request, 'User Account Deactivated')
                # redirect the user to the managers
                    return redirect("authentication:login")
            #    elif user.is_authenticated and not user.devision.tenant_id.status:
            #         messages.info(request, 'User Institutuin Deactivated')
            #         return redirect("authentication:login")
           else:
                            
                messages.info(request, 'Username or Password is incorrect')
                # redirect the user to the managers
                return redirect("authentication:login")


    context = {
        'form': form,  # context is the form itself
    }
    template = 'authentication/auth-login.html'
    return render(request, template, context)


@login_required(login_url='login')
@permission_required('authentication.custom_view_user',raise_exception = True)
def usergroups(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    group_list = Group.objects.all()
    template = 'authentication/groups.html'
    context = {
        'group_list': group_list,
        'heading': 'List of Groups',
        'pageview': 'Groups',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='login')
@permission_required('authentication.custom_create_user',raise_exception = True)
def add_usergroups(request):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            permissions = form.cleaned_data['permissions']
            name = form.cleaned_data['name']
            group = Group(name=name.title())
            group.save()
            group.permissions.set(permissions)
            messages.info(request,'Group Saved')
            return redirect('authentication:detail-group', group.id )
    else:
        form = UserGroupForm()

    template = 'authentication/creategroup.html'
    context = {
        'form':form,
        'heading': 'Group List',
        'pageview': 'New Group',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='login')
@permission_required('authentication.custom_update_user',raise_exception = True)
def edit_usergroups(request,group_id):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    group_list = Group.objects.all().order_by('-id')
    group=Group.objects.get(id=group_id)
    if request.method == 'POST':
        form = UserGroupEditForm(request.POST,instance=group)
        if form.is_valid():
            group=form.save()
            messages.info(request,'Group Updated')
            return redirect('authentication:detail-group', group.id )
    else:
        form = UserGroupEditForm(instance=group)

    template = 'authentication/creategroup.html'
    context = {
        'form':form,
        'heading': 'List of Groups',
        'pageview': 'Update',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='login')
@permission_required('authentication.custom_delete_user',raise_exception = True)
def delete_usergroups(request,group_id):
    group=Group.objects.get(id=group_id)
    group.delete()
    messages.error(request,'Group Deleted')
    return redirect('authentication:group-list')
   
@login_required(login_url='login')
@permission_required('authentication.custom_view_user',raise_exception = True)
def detail_usergroups(request,group_id):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    group=Group.objects.get(id=group_id)
    group_permissions = group.permissions.all()
    template = 'authentication/group-detail-view.html'
    context = {
        'group':group,
        'group_permissions':group_permissions,
        'heading': 'List of Groups',
        'pageview': 'Details'
    }
    return render(request,template,context)



@login_required(login_url='login')
@permission_required('authentication.custom_view_user',raise_exception = True)
def users(request):

   
    user_list = User.objects.filter(is_applicant=True,status='Submitted')
    # completed_list = User.objects.filter(is_applicant=True,status='Submitted')
    total_user = user_list.count()
    female_users = user_list.filter(gender='Female').count()
    male_users = user_list.filter(gender='Male').count()

    myFilter = UserFilter(request.GET, queryset=User.objects.filter(is_applicant=True,status='Submitted'))
    user_list = myFilter.qs
    total_user = user_list.count()
    female_users = user_list.filter(gender='Female').count()
    male_users = user_list.filter(gender='Male').count()
    template = 'authentication/users.html'
    context = {
        'user_list': user_list,
        'total_user':total_user,
        'female_users':female_users,
        'male_users':male_users,
        'myFilter':myFilter,
        'heading': 'Applications',
        'pageview': 'Applications',
        
    }
    return render(request,template,context)


def add_user(request):
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_new = True
            user.status = 'Pending'
            user.save()
            group,created =Group.objects.get_or_create(name='Standard')
            if created:
                permission=Permission.objects.get(codename='custom_create_application')
                group.permissions.add(permission)
                group.save()
            user.groups.add(group)
            user.group = group
            code = verification_code(6)
            user.code = code
            user.is_applicant = True
            user.save()
            NotificationThread(user).start()
            messages.info(request,'Registration Succesful, Application Verification has been sent to your email and phone number.You will be required to provide it after firt time login')
            return redirect('login')
        else:
            print('form is not valid')
    else:
        form = CreateUserForm()
        user= request.user
    template = 'authentication/auth-register-2.html'
    context = {
        'form':form,
        # 'heading': 'List Of Users',
        # 'pageview': 'New User',
        
    }
    return render(request,template,context)

@login_required(login_url='login')
@permission_required('authentication.custom_delete_user',raise_exception = True)
def change_userstatus(request,user_id):
    user=User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    messages.info(request,'User Status Changed')
    return redirect('authentication:detail-user', user.id)

@login_required(login_url='login')
@permission_required('authentication.custom_view_user',raise_exception = True)
def detail_user(request,user_id):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    user=User.objects.get(id=user_id)
    # print(user_permission)
    template = 'authentication/user-detail-view.html'
    context = {
        'user':user,
        'heading': 'List of Users',
        'pageview': 'Details',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='login')
def change_password(request,user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            user.is_new = False
            user.save()
            messages.info(request,'Application verification Comfirmed')
            return redirect('authentication:biodata',user.id)  # Redirect to a success page after password change
    else:
        form = VerificationForm()

    return render(request, 'authentication/change-password.html', {'form': form,'user':user})

def bio_data(request,user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = BioForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save()
            messages.info(request,'Bio Data Updated')
            return redirect('authentication:education',user.id)
    else:
        form = BioForm(instance = user )
        user= request.user
    template = 'authentication/create-user.html'
    context = {
        'form':form,
        'heading': 'Bio Data',
        'pageview': 'Application',
        
    }
    return render(request,template,context)

@login_required(login_url='login')
def logout_request(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_education(request,user_id):
    user =User.objects.get(id=user_id)
    education = EducationalHistory.objects.filter(user=user.id).order_by('-id')
    if request.method == 'POST':
        if request.FILES:
            form = EducationForm(request.POST, request.FILES)
        else:
            form = EducationForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            qualificationtype = form.cleaned_data['qualificationtype']
            studyfield=form.cleaned_data['studyfield']
            status=form.cleaned_data['status']
            
            others = form.cleaned_data['others']
           
            if status == 'Completed':
                completion_date=form.cleaned_data['completion_date']
            else:
                completion_date = None
            if request.FILES:
               attachment = form.cleaned_data['file']
            else:
                attachment = None 
            EducationalHistory.objects.get_or_create(user=user,qualificationtype=qualificationtype,studyfield=studyfield,others=others,name=name,completion_date=completion_date,status=status)
            if qualificationtype.name == 'First Degree' and status == 'Completed':
                if user.qualificationtype is None:
                    user.qualificationtype = qualificationtype
                    
            elif qualificationtype.name == 'Masters' and status == 'Completed':
                if user.qualificationtype is None or user.qualificationtype.name == 'First Degree':
                    user.qualificationtype = qualificationtype
                    
            elif qualificationtype.name == 'Doctorate' and status == 'Completed':
                if user.qualificationtype is None or user.qualificationtype.name == 'First Degree' or qualificationtype.name == 'Masters':
                    user.qualificationtype = qualificationtype
                    
                user.qualificationtype = None
            user.save()
            
            messages.success(request,'Academic Qualification Added')
            return redirect('authentication:education',user.id)       
    else:
        form = EducationForm()

    template = 'authentication/create-education.html'
    context = {
        'form': form,
        'education':education ,
        'user': user,
        'heading': 'Educational Qualification',
        'pageview': 'Application',
    }
    return render(request, template, context)

@login_required(login_url='login')
def edit_education(request,edu_id):
    educations = EducationalHistory.objects.get(id=edu_id)
    user =User.objects.get(id=educations.user.id)
    education = EducationalHistory.objects.filter(user=user.id).order_by('-id')
    if request.method == 'POST':
        if request.FILES:
            form = EducationForm(request.POST, request.FILES,instance=educations)
        else:
            form = EducationForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            qualificationtype = form.cleaned_data['qualificationtype']
            studyfield=form.cleaned_data['studyfield']
         
            status=form.cleaned_data['status']
            
            others = form.cleaned_data['others']
           
            if status == 'Completed':
                completion_date=form.cleaned_data['completion_date']
            else:
                completion_date = None
            if request.FILES:
               attachment = form.cleaned_data['file']
            else:
                attachment = None 
            educations.qualificationtype=qualificationtype
            educations.studyfield=studyfield
            educations.others=others
            educations.name = name
            educations.completion_date =completion_date
            educations.status =status
            educations.attachment=attachment
            educations.save()

            # EducationalHistory.objects.get_or_create(user=user,qualificationtype=qualificationtype,studyfield=studyfield,others=others,name=name,completion_date=completion_date,status=status,attachment=attachment)
            messages.success(request,'Academic Qualification Updated')
            return redirect('authentication:education',user.id)       
    else:
        form = EducationForm(instance=educations)

    template = 'authentication/create-education.html'
    context = {
        'form': form,
        'education':education ,
        'user': user,
        'heading': 'Educational Qualification',
        'pageview': 'Application',
    }
    return render(request, template, context)

def remove_education(request,education_id):
    education = EducationalHistory.objects.get(id=education_id)
    user = User.objects.get(id=education.user.id)
    
    if education.qualificationtype == user.qualificationtype:
        user.qualificationtype = None
        user.save()
    education.delete()
    alledu = EducationalHistory.objects.filter(user=user)
    numedu = alledu.count()
    
    if numedu >= 1:
        aa =alledu.order_by('-id').first()
        user.qualificationtype = aa.qualificationtype
        user.save()
        
    messages.error(request,'Academic Qualification Deleted')
    return redirect('authentication:education',user.id) 



@login_required(login_url='login')
def add_professional(request,user_id):
    user =User.objects.get(id=user_id)
    education = ProfessionalHistory.objects.filter(user=user.id).order_by('-id')
    if request.method == 'POST':
        
        form = ProfessionalForm(request.POST)
       
        if form.is_valid():
            profesionalbody=form.cleaned_data['profesionalbody']
            others = form.cleaned_data['others']
            level=form.cleaned_data['level']
            status=form.cleaned_data['status']
            qualification_date = form.cleaned_data['qualification_date']
            ProfessionalHistory.objects.get_or_create(user=user,profesionalbody=profesionalbody,others=others,level=level,status=status,qualification_date=qualification_date)
            user.profesionalbody = profesionalbody
            user.save()
            print(user.profesionalbody)
            messages.success(request,'Professional Qualification Added')
            return redirect('authentication:professional',user.id)       
    else:
        form = ProfessionalForm()

    template = 'authentication/create-professional.html'
    context = {
        'form': form,
        'education':education ,
        'user': user,
        'heading': 'Professional Qualification',
        'pageview': 'Application',
    }
    return render(request, template, context)

def remove_professional(request,prof_id):
    education = ProfessionalHistory.objects.get(id=prof_id)
    user = User.objects.get(id=education.user.id)
    education.delete()
    user.profesionalbody = None
    user.save()
    print(user.profesionalbody)
    messages.error(request,'Professional Qualification Deleted')
    return redirect('authentication:professional',user.id) 

@login_required(login_url='login')
def add_cv(request,user_id):
    user =User.objects.get(id=user_id)
    if request.method == 'POST':
        form = CvForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.cleaned_data['file']
            if attachment is None:
                pass
            else:
                user.attachment = attachment
            user.save()
            messages.success(request,'Curriculum Vitae Uploaded Successfully')
            return redirect('authentication:application-overview',user.id)       
    else:
        form = CvForm()
    template = 'authentication/upload-cv.html'
    context = {
        'form': form,
        'user': user,
        'heading': 'Curriculum Vitae',
        'pageview': 'Application',
    }
    return render(request, template, context)


@login_required(login_url='login')
def application_overview(request,user_id):
    user =User.objects.get(id=user_id)
    education = EducationalHistory.objects.filter(user=user.id).order_by('-id')
    profesional = ProfessionalHistory.objects.filter(user=user.id).order_by('-id')
    work = WorkHistory.objects.filter(user=user.id).order_by('-id')
    cv = CVHistory.objects.filter(user=user.id).first()
    # pdf_document = get_object_or_404(Documentattachement, pk=document_id)
    template = 'authentication/application-review.html'
    context = {
    
        'education':education ,
        'user': user,
        'profesional':profesional,
        'education':education,
        'work':work,
        'heading': 'Application Review',
        'pageview': 'Application',
    }
    return render(request, template, context)

@login_required(login_url='login')
def add_work(request,user_id):
    user =User.objects.get(id=user_id)
    education = WorkHistory.objects.filter(user=user.id).order_by('-id')
    if request.method == 'POST':
      
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.user = user
            work.save()
            messages.success(request,'Work Experience Added')
            return redirect('authentication:work',user.id)       
    else:
        form = WorkForm()

    template = 'authentication/create-work.html'
    context = {
        'form': form,
        'education':education ,
        'user': user,
        'heading': 'Work Experience',
        'pageview': 'Application',
    }
    return render(request, template, context)

def remove_work(request,work_id):
    education = WorkHistory.objects.get(id=work_id)
    user = User.objects.get(id=education.user.id)
    education.delete()
    messages.error(request,'Work Experience Deleted')
    return redirect('authentication:work',user.id) 

@login_required(login_url='login')
def application_comfirm(request,user_id):
    user =User.objects.get(id=user_id)
    user.status='Submitted'
    user.save()
    CompleteNotificationThread(user).start()
    messages.success(request,'Application Submitted')
    return redirect('authentication:application-overview',user.id)
    

@login_required(login_url='login')
def admin_application_overview(request,user_id):
    user =User.objects.get(id=user_id)
    education = EducationalHistory.objects.filter(user=user.id).order_by('-id')
    profesional = ProfessionalHistory.objects.filter(user=user.id).order_by('-id')
    work =WorkHistory.objects.filter(user=user.id).order_by('-id')
    cv = CVHistory.objects.filter(user=user.id).first()
    # pdf_document = get_object_or_404(Documentattachement, pk=document_id)
    template = 'authentication/admin-application-review.html'
    context = {
    
        'education':education ,
        'user': user,
        'profesional':profesional,
        'education':education,
        'work':work,
        'heading': 'Application Review',
        'pageview': 'Application',
    }
    return render(request, template, context)