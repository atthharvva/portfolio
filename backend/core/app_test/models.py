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

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    linkedin = models.URLField(blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Meal(models.Model):
    """
    Main meal model containing recipe information
    """
    DIET_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('nonvegetarian', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
    ]
    
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=200)
    description = models.TextField()
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Images
    image = models.ImageField(upload_to='meals/', blank=True, null=True)
    
    # Nutrition Info
    calories = models.IntegerField(help_text="Total calories")
    protein = models.IntegerField(help_text="Protein in grams")
    carbs = models.IntegerField(help_text="Carbohydrates in grams")
    fats = models.IntegerField(help_text="Fats in grams")
    
    # Cooking Info
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField(default=2)
    difficulty = models.CharField(
        max_length=20, 
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='medium'
    )
    
    # Video
    youtube_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)"
    )
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_diet_type_display()} - {self.get_category_display()})"
    
    def get_youtube_embed_url(self):
        """
        Convert YouTube URL to embed URL
        Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ
        Returns: https://www.youtube.com/embed/dQw4w9WgXcQ
        """
        if not self.youtube_url:
            return None
        
        # Extract video ID from various YouTube URL formats
        if 'youtube.com/watch?v=' in self.youtube_url:
            video_id = self.youtube_url.split('watch?v=')[1].split('&')[0]
        elif 'youtu.be/' in self.youtube_url:
            video_id = self.youtube_url.split('youtu.be/')[1].split('?')[0]
        else:
            return None
        
        return f"https://www.youtube.com/embed/{video_id}"
    
    @property
    def total_time(self):
        """Total time in minutes"""
        return self.prep_time + self.cook_time


class Ingredient(models.Model):
    """
    Ingredients for each meal
    """
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100, help_text="e.g., 2 cups, 500g, 1 tbsp")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.quantity} {self.name}"


class Instruction(models.Model):
    """
    Step-by-step cooking instructions
    """
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.IntegerField()
    instruction = models.TextField()
    
    class Meta:
        ordering = ['step_number']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.instruction[:50]}..."


class NutritionTip(models.Model):
    """
    Optional nutrition tips for meals
    """
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='tips')
    tip = models.TextField()
    
    def __str__(self):
        return self.tip[:50]
