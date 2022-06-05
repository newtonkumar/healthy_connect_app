from django.db import models


class Hobbies(models.Model):
    class Meta:
        db_table = 'hobbies'

    hobby = models.CharField(max_length=50)

    def __str__(self):
        return self.hobby


class GoalSetting(models.Model):
    class Meta:
        db_table = 'goal_setting'

    goal = models.CharField(max_length=50)

    def __str__(self):
        return self.goal


class WorkoutPreferences(models.Model):
    class Meta:
        db_table = 'workout_preferences'

    preference = models.CharField(max_length=255)

    def __str__(self):
        return self.preference


class DietaryPreferences(models.Model):
    class Meta:
        db_table = 'dietary_preferences'

    preference = models.CharField(max_length=255)

    def __str__(self):
        return self.preference
