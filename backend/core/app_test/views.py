from django.shortcuts import render
from .models import About, Profile, Skill

# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    about = About.objects.first()
    
    return render(request, "core.html", {
        "profile": profile,
        "skills": skills,
        "about": about
    })