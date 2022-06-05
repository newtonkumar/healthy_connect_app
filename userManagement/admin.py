from django.contrib import admin
from .models import Hobbies, GoalSettings, WorkoutPreferences, DietaryPreferences

admin.site.register(Hobbies)
admin.site.register(GoalSettings)
admin.site.register(WorkoutPreferences)
admin.site.register(DietaryPreferences)