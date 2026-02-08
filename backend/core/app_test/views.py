from collections import defaultdict
from urllib import response
from django.shortcuts import render
from django.http import JsonResponse
from .models import About, Profile, Skill, Experience, Education

# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

# def home(request):
#     profile = Profile.objects.first()
#     skills = Skill.objects.order_by("category", "order")
#     # print("Skills:", skills)
#     about = About.objects.first()
#     experiences = Experience.objects.all().order_by('order')
#     education = Education.objects.all().order_by('order')

#     grouped_skills = defaultdict(list)
#     for skill in skills:
#         grouped_skills[skill.category].append(skill)

#     grouped_skills = dict(grouped_skills) 
#     print("Grouped Skills:", grouped_skills)
#     # return response(grouped_skills)
    
#     return render(request, "core.html", {
#         "profile": profile,
#         "skills": grouped_skills,
#         "about": about,
#         "experiences": experiences,
#         "education": education
#     })
def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.order_by("category", "order")
    about = About.objects.first()
    experiences = Experience.objects.all().order_by('order')
    education = Education.objects.all().order_by('order')

    grouped_skills = defaultdict(list)
    for skill in skills:
        display_name = skill.get_category_display()  # <-- This is the key line
        grouped_skills[display_name].append(skill)
    
    grouped_skills = dict(grouped_skills)
    
    return render(request, "core.html", {
        "profile": profile,
        "skills": grouped_skills,
        "about": about,
        "experiences": experiences,
        "education": education
    })