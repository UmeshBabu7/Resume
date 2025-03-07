from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

class Resume(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="resume")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    education = models.TextField()
    skills = models.TextField()
    languages = models.TextField()
    experience = models.TextField()
    training_certifications = models.TextField()
    projects = models.TextField()
    interests = models.TextField()

    def __str__(self):
        return self.full_name
