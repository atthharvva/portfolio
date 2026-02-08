from django.db import models

# Create your models here.
class Profile(models.Model):
    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    summary = models.TextField()
    about = models.TextField()
    email = models.EmailField()
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


# class Skill(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name
    
class About(models.Model):
    heading = models.CharField(max_length=100, default="About Me")
    body = models.TextField(
        help_text="Write in paragraphs. Line breaks will be preserved."
    )

    def __str__(self):
        return self.heading
    
class Experience(models.Model):
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.role} @ {self.company}"


class Education(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=150)
    year = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.degree
    
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("backend", "Backend"),
        ("frontend", "Frontend"),
        ("database", "Database"),
        ("tools", "Tools"),
        ("languages", "Languages"),
        ("frameworks", "Frameworks"),
        ("concepts", "Concepts"),
        ("ai_ml", "AI & ML"),
        ("devops", "DevOps"),
        ("security", "Security"),
    ]

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    level = models.IntegerField(help_text="Skill level from 1 to 100", blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name
