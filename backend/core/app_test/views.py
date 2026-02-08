from collections import defaultdict
import json
import resend
from urllib import response
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from django.conf import settings
from .models import About, Profile, Skill, Experience, Education, Contact

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

resend.api_key = settings.RESEND_API_KEY

@require_http_methods(["POST"])
def contact_form(request):
    try:
        data = json.loads(request.body)
        
        # Create contact entry
        contact = Contact.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            linkedin=data.get('linkedin', ''),
            mobile=data.get('mobile', ''),
            message=data.get('message', '')
        )

        try:
            resend.Emails.send({
                "from": "onboarding@resend.dev",  # Or use onboarding@resend.dev for testing, portfolio@yourdomain.com for production
                "to": "atharva2003.swami@gmail.com",
                "subject": f"New Contact from {contact.name}",
                "html": f"""
                    <h2>New Contact Form Submission!</h2>
                    <p><strong>Name:</strong> {contact.name}</p>
                    <p><strong>Email:</strong> {contact.email}</p>
                    <p><strong>LinkedIn:</strong> {contact.linkedin or 'Not provided'}</p>
                    <p><strong>Mobile:</strong> {contact.mobile or 'Not provided'}</p>
                    <p><strong>Message:</strong></p>
                    <p>{contact.message or 'No message provided'}</p>
                    <hr>
                    <p><small>Submitted at: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}</small></p>
                """
            })
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Your message has been sent successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)