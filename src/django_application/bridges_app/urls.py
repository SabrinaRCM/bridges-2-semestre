from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='bridges_app/login.html'), name='login'),
    path('logout', views.logout_request, name='logout'),
    path('import_excel', views.import_excel, name='import_excel'),
    path('gantt', views.gantt, name='gantt'),
    path('update_gantt', views.update_gantt, name='update_gantt'),
    path('tarefas', views.tarefas, name='Tarefas'),
    path('update_task/<int:pk>', views.update_task, name='update_task'),
    path('delete_task/<int:pk>', views.delete_task, name='delete_task'),
    path('projetos', views.projetos, name='projetos'),
    path('update_project/<int:pk>', views.update_project, name='update_project'),
    path('delete_project/<int:pk>', views.delete_project, name='delete_project'),
    path('funcionarios', views.funcionarios, name='funcionarios'),
    path('update_worker/<int:pk>', views.update_worker, name='update_worker'),
    path('delete_worker/<int:pk>', views.delete_worker, name='delete_worker'),
    path('agenda', views.agenda, name='agenda'),
    path('update_schedule/<int:pk>', views.update_schedule, name='update_schedule'),
    path('delete_schedule/<int:pk>', views.delete_schedule, name='delete_schedule'),
]