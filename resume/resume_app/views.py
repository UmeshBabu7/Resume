from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
from .models import Resume
from .forms import CustomUserCreationForm
from django.contrib import messages
from resume_app.models import CustomUser


# Create your views here.

# home page
def home(request):
    if request.user.is_authenticated:
        resumes = Resume.objects.filter(user=request.user)
    else:
        resumes = []
    return render(request, 'home.html', {'resumes': resumes})


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('resume_app:login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})


# register/signup page
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            user = CustomUser.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('resume_app:login')
        else:
            # Handle the case where passwords do not match
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    return render(request, 'register.html')

# login page
# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('resume_app:home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})


# login page
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('resume_app:home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


# logout
def user_logout(request):
    logout(request)
    return redirect('resume_app:home')


# def create_resume(request):
#     if request.method == "POST":
#         profile_picture = request.FILES.get('profile_picture')
#         full_name = request.POST['full_name']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         education = request.POST['education']
#         skills = request.POST['skills']
#         languages = request.POST['languages']
#         experience = request.POST['experience']
#         training_certifications = request.POST['training_certifications']
#         projects = request.POST['projects']
#         interests = request.POST['interests']

#         # Check if a resume already exists for the user
#         resume, created = Resume.objects.get_or_create(
#             user=request.user,
#             defaults={
#                 'profile_picture': profile_picture,
#                 'full_name': full_name,
#                 'email': email,
#                 'phone': phone,
#                 'education': education,
#                 'skills': skills,
#                 'languages': languages,
#                 'experience': experience,
#                 'training_certifications': training_certifications,
#                 'projects': projects,
#                 'interests': interests
#             }
#         )

#         if not created:
#             # Update the existing resume
#             resume.profile_picture=profile_picture
#             resume.full_name = full_name
#             resume.email = email
#             resume.phone = phone
#             resume.education = education
#             resume.skills = skills
#             resume.languages = languages
#             resume.experience = experience
#             resume.training_certifications = training_certifications
#             resume.projects = projects
#             resume.interests = interests
#             resume.save()

#         return redirect('resume_app:home')
#     return render(request, 'create_resume.html')


# create resume
def create_resume(request):
    if request.method == "POST":
        profile_picture = request.FILES.get('profile_picture')
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        education = request.POST['education']
        skills = request.POST['skills']
        languages = request.POST['languages']
        experience = request.POST['experience']
        training_certifications = request.POST['training_certifications']
        projects = request.POST['projects']
        interests = request.POST['interests']

        
        resume, created = Resume.objects.get_or_create(
            user=request.user,
            defaults={
                'profile_picture': profile_picture,
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'education': education,
                'skills': skills,
                'languages': languages,
                'experience': experience,
                'training_certifications': training_certifications,
                'projects': projects,
                'interests': interests
            }
        )

        if not created:
            # Update the existing resume
            resume.profile_picture = profile_picture
            resume.full_name = full_name
            resume.email = email
            resume.phone = phone
            resume.education = education
            resume.skills = skills
            resume.languages = languages
            resume.experience = experience
            resume.training_certifications = training_certifications
            resume.projects = projects
            resume.interests = interests
            resume.save()

        return redirect('resume_app:home')
    return render(request, 'create_resume.html')


# update/edit
def update_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.user != resume.user:
        return redirect('home')
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        resume.full_name = request.POST.get('full_name', '')
        resume.email = request.POST.get('email', '')
        resume.phone = request.POST.get('phone', '')
        resume.education = request.POST.get('education', '')
        resume.skills = request.POST.get('skills', '')
        resume.languages = request.POST.get('languages', '')
        resume.experience = request.POST.get('experience', '')
        resume.training_certifications = request.POST.get('training_certifications', '')
        resume.projects = request.POST.get('projects', '')
        resume.interests = request.POST.get('interests', '')

        if profile_picture:
            resume.profile_picture = profile_picture

        try:
            resume.save()
        except Exception as e:
            print(f"Error saving resume: {e}")
            return render(request, 'update_resume.html', {'resume': resume, 'error': str(e)})

        return redirect('resume_app:home')
    return render(request, 'update_resume.html', {'resume': resume})



# delete
def delete_resume(request, resume_id):
    resume = Resume.objects.get(id=resume_id)
    if resume.user == request.user:
        resume.delete()
    return redirect('resume_app:home')


# def generate_pdf(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id)
#     html = render_to_string('resume_pdf.html', {'resume': resume})

#     config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    
#     options = {
#         'enable-local-file-access': None,
#     }
    
#     pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    

# pdf generator(download method)
def generate_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    profile_picture_url = request.build_absolute_uri(resume.profile_picture.url) if resume.profile_picture else None
    html = render_to_string('resume_pdf.html', {'resume': resume, 'profile_picture_url': profile_picture_url})

    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    
    options = {
        'enable-local-file-access': None,
    }
    
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    
    return response


# View/detail resume
def view_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    return render(request, 'view_resume.html', {'resume': resume})

