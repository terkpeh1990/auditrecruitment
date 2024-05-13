from django import forms
from django.contrib.auth import authenticate, get_user_model,password_validation
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import Group, Permission
from .import models
from .models import *
from django.forms.widgets import NumberInput

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Email'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Please Enter Password'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Username or Password incorrect')
            if not user.check_password(password):
                raise forms.ValidationError('Username or Password incorrect')
            if not user.is_active:
                raise forms.ValidationError('Username or Password incorrect')
        return super(UserLoginForm, self).clean(*args, **kwargs)

    class Meta():
        model = User
        fields = ('email', 'password')

class UserGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__icontains='custom'),
        widget=forms.CheckboxSelectMultiple,
        label=False
    )
    name = forms.CharField(label=False)
    class Meta:
        model = Group
        fields = ('name','permissions')

    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        name_exists = Group.objects.filter(name=name.title()) 
        if name:
            if name_exists.exists():
                raise forms.ValidationError(
                    {'name': ["A Group with this name already exist"]})
        return super(UserGroupForm, self).clean(*args, **kwargs)

class UserGroupEditForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__icontains='custom'),
        widget=forms.CheckboxSelectMultiple,
        label=False
    )
    name = forms.CharField(label=False)
    class Meta:
        model = Group
        fields = ('name','permissions')

class GradeForm(forms.ModelForm):
    name = forms.CharField(label=False)
    class Meta:
        model = Grade
        fields = ('name',)


class CreateUserForm(UserCreationForm):
    stat =(
        ('Yes','Yes'),
        ('No','No'),
    )
    email = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Email'}))
    last_name = forms.CharField(label=False, required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Surname'}))
    first_name = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter First Name'}))
    middle_name = forms.CharField(label=False,required=False,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Other Name(s)'}))
    ghanacard = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Ghana Card Number'}))
    phone_number = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Phone Number'}))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=False, widget=forms.PasswordInput)
   
    class Meta:
        model = User
        fields = ('email','last_name','first_name','middle_name','ghanacard','phone_number','password1', 'password2')
    
    def clean_first_name(self):
        return self.cleaned_data['first_name'].title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].title()

    def clean_email(self):
        return self.cleaned_data['email'].lower()
    
    def clean_email_staff(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        ghanacard = self.cleaned_data.get('ghanacard')
        email_exists = User.objects.filter(email=email)
        ghanacard_exists = User.objects.filter(ghanacard=ghanacard)
        
        if email:
            if email_exists.exists():
                raise forms.ValidationError(
                    {'email': ["A user with this email address already exist"]})
        if ghanacard:
            if ghanacard_exists.exists():
                raise forms.ValidationError(
                    {'staffid': ["A user with this National Identification Number already exist. Multiple Registration Not Allowed "]})
        
        if password and password2:
            if not password == password2 :
                raise forms.ValidationError(
                    {'password2': ["Password Mismatch "]})
        return super(CreateUserForm, self).clean(*args, **kwargs)

    
class VerificationForm(forms.ModelForm):
    code = forms.CharField(required=True,label=False,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Verification Code'}))

    class Meta:
        model = User
        fields = ('code',)
    
    

    def clean(self, *args, **kwargs):
        code = self.cleaned_data.get('code')
        user_exist = User.objects.filter(code=code)
        if code:
            if not user_exist.exists():
                raise forms.ValidationError(
                    {'code': ["Invalid Code"]})
        return super(VerificationForm, self).clean(*args, **kwargs)


class BioForm(forms.ModelForm):
    sex = (
        ('-----','-----'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    marrital = (
        ('-----','-----'),
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Divorced','Divorced'),
        ('Separated','Separated'),
    )
    email = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Email'}))
    last_name = forms.CharField(label=False, required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Surname'}))
    first_name = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter First Name'}))
    middle_name = forms.CharField(label=False,required=False,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Other Name(s)'}))
    gender = forms.ChoiceField(label=False,choices=sex,required=True)   
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    place_of_birth  = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Place of Birth'}))
    ghanacard = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Ghana Card Number'}))
    phone_number = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Phone Number'}))
    
    marital_status = forms.ChoiceField(label=False,choices=marrital,required=True)
    address = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'P.o.Box M96'}))
    city = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Adenta/Greater Accra'}))
    gps = forms.CharField(label=False,required=True,widget=forms.TextInput(
        attrs={'placeholder': 'GA-000-000'}))
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
           )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
           )
    
    class Meta:
        model = User
        fields = ('email','last_name','first_name','middle_name','gender','dob','place_of_birth','ghanacard','phone_number','marital_status','address','city','gps','grade','region')
    
    

    def clean(self, *args, **kwargs):
        gender = self.cleaned_data.get('gender')
        marital_status = self.cleaned_data.get('marital_status')
        if gender:
            if gender == '-----' :
                raise forms.ValidationError(
                    {'gender': ["Please Select Gender"]})

        if marital_status:
            if marital_status == '-----':
                raise forms.ValidationError(
                    {'marital_status': ["Please Select Marital Status"]})
        return super(BioForm, self).clean(*args, **kwargs)


class EducationForm(forms.Form):
    status = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )
    name = forms.CharField(label=False,required=True)
    qualificationtype = forms.ModelChoiceField(
        queryset=QualificationType.objects.all().order_by('id'),
        label=False,
        empty_label="Select One",
        required=True
           )
    studyfield = forms.ModelChoiceField(
        queryset=StudyField.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
           )
    others =forms.CharField(label=False,required=False)
    status = forms.ChoiceField(label=False,choices=status,required=True)
    completion_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=False)
    

   

class ProfessionalForm(forms.Form):
    status = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )
    profesional = (
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
        
        
    )
    profesionalbody = forms.ModelChoiceField(
        queryset=ProffesionalBody.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
           )
    others =forms.CharField(label=False,required=False)
    level = forms.ChoiceField(label=False,choices=profesional,required=False)
    status = forms.ChoiceField(label=False,choices=status,required=True)
    qualification_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=False)
    

class CvForm(forms.Form):
    file = forms.FileField(label=False,
    help_text=('Supported formats: PDF'),
    validators=[validate_file_extension],
    required=False)

    def clean_file(self,*args, **kwargs):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        if file:
            validate_file_extension(file)
        return file

class WorkForm(forms.ModelForm):
    name  = forms.CharField(required=True,label=False,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Organization Name'}))
    position  = forms.CharField(required=True,label=False,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Organization Name'}))
    startdate=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    enddate=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=False)
    refnumber = forms.CharField(label=False,required=False,widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Reference contact'}))
    class Meta:
        model = WorkHistory
        fields = ('name','position','startdate','enddate','refnumber')