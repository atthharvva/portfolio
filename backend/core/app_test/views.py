from django.shortcuts import render
from .models import About, Profile, Skill, Experience, Education

# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    about = About.objects.first()
    experiences = Experience.objects.all().order_by('order')
    education = Education.objects.all().order_by('order')
    
    return render(request, "core.html", {
        "profile": profile,
        "skills": skills,
        "about": about,
        "experiences": experiences,
        "education": education
    })