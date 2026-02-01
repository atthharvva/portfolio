from django.shortcuts import render
from .models import Profile, Skill

# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    return render(request, "core.html", {
        "profile": profile,
        "skills": skills
    })