# filters.py
import django_filters
from .models import User, EducationalHistory, ProfessionalHistory,StudyField,ProffesionalBody,QualificationType

class UserFilter(django_filters.FilterSet):
    status = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )
    profesional = (
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
   
        
    )
    educationalhistory__qualificationtype = django_filters.ModelChoiceFilter(queryset=QualificationType.objects.all(), field_name='usereducation__qualificationtype', label='Qualification Type')
    educationalhistory__studyfield = django_filters.ModelChoiceFilter(queryset=StudyField.objects.all(), field_name='usereducation__studyfield', label='Study Field')
    usereducation__status = django_filters.ChoiceFilter(choices=status, label='Educational History Status')
    userprofessional__profesionalbody = django_filters.ModelChoiceFilter(queryset=ProffesionalBody.objects.all(), field_name='userprofessional__profesionalbody', label='Professional Body')
    userprofessional__level = django_filters.ChoiceFilter(choices=profesional, label='Professional Body Level')
    userprofessional__status = django_filters.ChoiceFilter(choices=status, label='Professional Body Status')

    class Meta:
        model = User
        fields = []

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Fetch choices for ChoiceFilter fields
    #     educational_status_choices = usereducation.values_list('status', flat=True).distinct()
    #     professional_level_choices = ProfessionalHistory.objects.values_list('level', flat=True).distinct()
    #     professional_status_choices = ProfessionalHistory.objects.values_list('status', flat=True).distinct()
        
    #     # Update choices for ChoiceFilter fields
    #     self.filters['educationalhistory__status'].extra['choices'] = [(choice, choice) for choice in educational_status_choices]
    #     self.filters['userprofessional__level'].extra['choices'] = [(choice, choice) for choice in professional_level_choices]
    #     self.filters['userprofessional__status'].extra['choices'] = [(choice, choice) for choice in professional_status_choices]