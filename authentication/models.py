from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from simple_history.models import HistoricalRecords
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group
from .validators import validate_file_extension


class Region(models.Model):
    name = models.CharField(max_length=255)
    history = HistoricalRecords()

    class Meta:
        db_table = 'Region'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        permissions = [
            ("custom_create_region", "Can Create Region"),
        ]
    def __str__(self):
        return f"{self.name}"



class Grade(models.Model):
    name = models.CharField(max_length=100)
    history = HistoricalRecords()
    class Meta:
        db_table = 'Rank'
        verbose_name = 'Rank'
        verbose_name_plural = 'Ranks'

        permissions = [
            ("custom_create_rank", "Can Create Rank"),
           
        ]

    def __str__(self):
        return self.name
    
class QualificationType(models.Model):
    name = models.CharField(max_length=100)
    history = HistoricalRecords()
    class Meta:
        db_table = 'QualificationType'
        verbose_name = 'QualificationType'
        verbose_name_plural = 'QualificationTypes'

        permissions = [
            ("custom_create_qualification", "Can Create Qualification"),
           
        ]

    def __str__(self):
        return self.name

class StudyField(models.Model):
    name = models.CharField(max_length=100)
    history = HistoricalRecords()
    class Meta:
        db_table = 'StudyField'
        verbose_name = 'StudyField'
        verbose_name_plural = 'StudyFields'

        permissions = [
            ("custom_create_field_of_study", "Can Create StudyField"),
           
        ]

    def __str__(self):
        return self.name

class ProffesionalBody(models.Model):
    name = models.CharField(max_length=100)
    history = HistoricalRecords()
    class Meta:
        db_table = 'ProffesionalBody'
        verbose_name = 'ProffesionalBody'
        verbose_name_plural = 'ProffesionalBodys'

        permissions = [
            ("custom_create_professional_body", "Can Create ProffesionalBody"),
           
        ]

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone_message = 'Phone number must begin with 0 and contain only 10 digits' 
    sex = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    status = (
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
    )
    decide = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    marrital = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Divorced','Divorced'),
        ('Separated','Separated'),
    )
     # your desired format 
    phone_regex = RegexValidator(
        regex=r'^(0)\d{9}$',
        message=phone_message
    )
    email = models.CharField(max_length=200,unique=True)
    last_name = models.CharField(max_length=250,null=True)
    first_name = models.CharField(max_length=250,null=True)
    middle_name = models.CharField(max_length=250,null=True)
    ghanacard = models.CharField(max_length=200,unique=True,null=True)
    gender = models.CharField(max_length=50,choices=sex,null=True)
    dob = models.DateField(null=True)
    phone_number = models.CharField(max_length=20,validators=[phone_regex],null=True)
    place_of_birth = models.CharField(max_length=200,null=True)
    marital_status = models.CharField(max_length=50,choices=marrital,null=True)
    address = models.CharField(max_length=250,null=True)
    city = models.CharField(max_length=250,null=True)
    gps = models.CharField(max_length=250,null=True)
    grade = models.ForeignKey('Grade', related_name='position', on_delete=models.CASCADE,null=True)
    region = models.ForeignKey('Region', related_name='posting', on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=50,choices=status,null=True)
    attachment=models.FileField(upload_to='documents/',validators=[validate_file_extension],null=True)
    qualificationtype  = models.ForeignKey('QualificationType', related_name='userqualification', on_delete=models.CASCADE,null=True)
    profesionalbody  = models.ForeignKey('ProffesionalBody', related_name='userprofessionalbody', on_delete=models.CASCADE,null=True)
    group  = models.ForeignKey(Group, blank=True, null=True, related_name = 'groups',on_delete=models.CASCADE)
    password = models.CharField(max_length=255, blank=True, null=True) 
    is_admin = models.BooleanField(default=False)
    is_new =models.BooleanField(default=False)
    is_applicant =models.BooleanField(default=False)
    code = models.CharField(max_length=50,null=True)
    is_applicant =models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    # history = HistoricalRecords()

    class Meta:
        
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        permissions = [
            ("custom_create_application", "Can Create Application"),
            ("custom_view_report", "Can View Reports"),
            ("custom_system_admin", "Is System Administratior"),
        ]
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.last_name } { self.middle_name } {self.first_name}"

class EducationalHistory(models.Model):
    status = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )
    user = models.ForeignKey('User', related_name='usereducation', on_delete=models.CASCADE)
    qualificationtype  = models.ForeignKey('QualificationType', related_name='applicant_qualification', on_delete=models.CASCADE)
    studyfield = models.ForeignKey('StudyField', related_name='studyfield', on_delete=models.CASCADE)
    others = models.CharField(max_length=250,null=True)
    name = models.CharField(max_length=250)
    completion_date = models.DateField(null=True)
    status = models.CharField(max_length=50,choices=status)
    history = HistoricalRecords()
    class Meta:
        db_table = 'EducationalHistory'
        verbose_name = 'EducationalHistory'
        verbose_name_plural = 'EducationalHistorys'

    def __str__(self):
        return self.name

class ProfessionalHistory(models.Model):
    status = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )
    profesional = (
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
       
        
    )
    user = models.ForeignKey('User', related_name='userprofessional', on_delete=models.CASCADE)
    profesionalbody  = models.ForeignKey('ProffesionalBody', related_name='applicantprofessionalbody', on_delete=models.CASCADE)
    others = models.CharField(max_length=250,null=True)
    level = models.CharField(max_length=50,choices=profesional)
    qualification_date = models.DateField(null=True)
    status = models.CharField(max_length=50,choices=status)
    
    history = HistoricalRecords()
    class Meta:
        db_table = 'ProfessionalHistory'
        verbose_name = 'ProfessionalHistory'
        verbose_name_plural = 'ProfessionalHistorys'

    def __str__(self):
        return self.profesionalbody.name

class CVHistory(models.Model):
    status = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )
    user = models.ForeignKey('User', related_name='usercv', on_delete=models.CASCADE)
    attachment=models.FileField(upload_to='documents/',validators=[validate_file_extension])
    history = HistoricalRecords()
    class Meta:
        db_table = 'CVHistory'
        verbose_name = 'CVHistory'
        verbose_name_plural = 'CVHistorys'

    def __str__(self):
        return str(self.id)

class WorkHistory(models.Model):
    phone_message = 'Phone number must begin with 0 and contain only 10 digits' 
    phone_regex = RegexValidator(
        regex=r'^(0)\d{9}$',
        message=phone_message
    )
    
    user = models.ForeignKey('User', related_name='userwork', on_delete=models.CASCADE)
    name  = models.CharField(max_length=250)
    position  = models.CharField(max_length=250,null=True)
    startdate =models.DateField(null=True)
    enddate = models.DateField(null=True)
    refnumber = models.CharField(max_length=20,validators=[phone_regex],null=True)
   
    history = HistoricalRecords()
    class Meta:
        db_table = 'WorkHistory'
        verbose_name = 'WorkHistory'
        verbose_name_plural = 'WorkHistorys'

    def __str__(self):
        return self.name
