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


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class About(models.Model):
    heading = models.CharField(max_length=100, default="About Me")
    body = models.TextField(
        help_text="Write in paragraphs. Line breaks will be preserved."
    )

    def __str__(self):
        return self.heading