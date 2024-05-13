from django.urls import path
from django.views.generic import TemplateView
from . import auth
# grades

app_name = 'authentication'

urlpatterns = [

    # path('login/',auth.login_view,name='login'),
    path('user/',auth.users,name='user-list'),
    # path('user/<str:user_id>/update/',auth.edit_user,name='edit-user'),
    # path('user/<str:user_id>/self_update/',auth.user_edit_user,name='self-edit-user'),
    path('user/new/',auth.add_user,name='new-user'),
    path('user/<str:user_id>/biodata/',auth.bio_data,name='biodata'),
    path('user/applicants/',auth.users,name='applicants'),
    path('user/<str:user_id>/academic_qualification/',auth.add_education,name='education'),
    path('user/academic_qualification/<str:edu_id>/update/',auth.edit_education,name='update-education'),
    path('user/academic_qualification/<str:education_id>/delete/',auth.remove_education,name='remove-education'),
    path('user/<str:user_id>/professional_qualification/',auth.add_professional,name='professional'),
    path('user/<str:user_id>/review/',auth.application_overview,name='application-overview'),
    path('user/admin/<str:user_id>/review/',auth.admin_application_overview,name='admin-application-overview'),
    path('user/<str:user_id>/application/comfirm/',auth.application_comfirm,name='application-comfirm'),
    path('user/professional_qualification/<str:prof_id>/delete/',auth.remove_professional,name='remove-professional'),
    path('user/<str:user_id>/upload_cv/',auth.add_cv,name='add-cv'),
    # path('user/<str:user_id>/delete/',auth.delete_user,name='delete-user'),
    path('user/<str:user_id>/detail/',auth.detail_user,name='detail-user'),
    path('user/<str:user_id>/change/',auth.change_userstatus,name='user-status'),
    path('user/<str:user_id>/otp/',auth.change_password,name='change-password'),
    path('logout/',auth.logout_request,name='log-out'),
    path('user/<str:user_id>/work_experience/',auth.add_work,name='work'),
     path('user/work_experience/<str:work_id>/delete/',auth.remove_work,name='delete-work'),

    
]