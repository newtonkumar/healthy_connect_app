from django.contrib import admin
from .models import Hobbies, GoalSetting, WorkoutPreferences, DietaryPreferences

admin.site.register(Hobbies)
admin.site.register(GoalSetting)
admin.site.register(WorkoutPreferences)
admin.site.register(DietaryPreferences)