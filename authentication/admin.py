from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','first_name','middle_name','last_name','ghanacard','dob','phone_number','code','group')
    search_fields = ['id','email','first_name','middle_name','last_name','ghanacard','dob','phone_number']


class GradeAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ['id','name']


admin.site.register(User,UserAdmin)
admin.site.register(Grade,GradeAdmin)
admin.site.register(Region,GradeAdmin)
admin.site.register(QualificationType,GradeAdmin)
admin.site.register(StudyField,GradeAdmin)
admin.site.register(ProffesionalBody,GradeAdmin)

