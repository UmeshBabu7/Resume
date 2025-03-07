from django.urls import path
from .import views

app_name="resume_app"

urlpatterns = [
    # home page part
    path('', views.home, name='home'),

    # user part
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # resume part
    path('create/', views.create_resume, name='create_resume'),
    path('update/<int:resume_id>/', views.update_resume, name='update_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('resume/<int:resume_id>/', views.view_resume, name='view_resume'),
    path('generate_pdf/<int:resume_id>/', views.generate_pdf, name='generate_pdf'),
]
