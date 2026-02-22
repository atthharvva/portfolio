from django.contrib import admin
from .models import Profile, Skill, Meal, Ingredient, Instruction, NutritionTip

admin.site.register(Profile)
admin.site.register(Skill)

class IngredientInline(admin.TabularInline):
    """
    Inline admin for ingredients - allows editing ingredients within meal page
    """
    model = Ingredient
    extra = 3
    fields = ['name', 'quantity', 'order']


class InstructionInline(admin.TabularInline):
    """
    Inline admin for instructions
    """
    model = Instruction
    extra = 3
    fields = ['step_number', 'instruction']


class NutritionTipInline(admin.TabularInline):
    """
    Inline admin for nutrition tips
    """
    model = NutritionTip
    extra = 1


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'diet_type', 
        'category', 
        'calories', 
        'protein',
        'difficulty',
        'total_time',
        'is_active',
        'order'
    ]
    list_filter = ['diet_type', 'category', 'difficulty', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'diet_type', 'category', 'image')
        }),
        ('Nutrition Facts', {
            'fields': ('calories', 'protein', 'carbs', 'fats')
        }),
        ('Cooking Information', {
            'fields': ('prep_time', 'cook_time', 'servings', 'difficulty')
        }),
        ('Video', {
            'fields': ('youtube_url',),
            'description': 'Paste YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)'
        }),
        ('Settings', {
            'fields': ('is_active', 'order'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [IngredientInline, InstructionInline, NutritionTipInline]
    
    def total_time(self, obj):
        return f"{obj.total_time} min"
    total_time.short_description = 'Total Time'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['meal', 'name', 'quantity', 'order']
    list_filter = ['meal__diet_type', 'meal__category']
    search_fields = ['name', 'meal__name']


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ['meal', 'step_number', 'instruction_preview']
    list_filter = ['meal__diet_type', 'meal__category']
    search_fields = ['instruction', 'meal__name']
    
    def instruction_preview(self, obj):
        return obj.instruction[:100] + '...' if len(obj.instruction) > 100 else obj.instruction
    instruction_preview.short_description = 'Instruction'


@admin.register(NutritionTip)
class NutritionTipAdmin(admin.ModelAdmin):
    list_display = ['meal', 'tip_preview']
    list_filter = ['meal__diet_type', 'meal__category']
    search_fields = ['tip', 'meal__name']
    
    def tip_preview(self, obj):
        return obj.tip[:100] + '...' if len(obj.tip) > 100 else obj.tip
    tip_preview.short_description = 'Tip'