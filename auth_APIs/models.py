from statistics import mode
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser
from userManagement.models import Hobbies, GoalSettings, WorkoutPreferences, DietaryPreferences


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    deviceType = ((1, "Android"), (2, "IOS"))
    genderType = ((1, "Male"), (2, "Female"), (3, "Transgender"), (4, "Non-Binary"), (5, "Prefer Not to Answer"))
    userApprovalStatus = ((1, "pending"), (2, "approved"), (3, "disapproved"))

    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    fullName = models.CharField(max_length=255, null=True)
    mobileNo = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    dob = models.CharField(max_length=255, null=True)
    phoneNumberCountryCode = models.CharField(max_length=5, null=True)
    age = models.CharField(max_length=10, null=True)
    activityLevel = models.IntegerField(null=True)
    height = models.CharField(max_length=10, null=True)
    currentWeight = models.CharField(max_length=10, null=True)
    goalWeight = models.CharField(max_length=10, null=True)
    hobbies = models.TextField(null=True)
    goals = models.TextField(null=True)
    workoutPreferences = models.TextField(null=True)
    dietaryPreferences = models.TextField(null=True)
    zipCode = models.CharField(max_length=255, null=False)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)
    deviceType = models.IntegerField(choices=deviceType, null=True)
    gender = models.IntegerField(choices=genderType, null=True)
    deviceToken = models.CharField(max_length=255, null=True)
    profileImage = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(default=0.00, blank=True, null=True)
    lng = models.FloatField(default=0.00, blank=True, null=True)
    last_login = models.DateTimeField(default=now, editable=False)
    isAvailable = models.BooleanField(default=False)
    isApproved = models.IntegerField(
        choices=userApprovalStatus, null=False, default=1)
    createdAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'mobileNo']
    objects = CustomAccountManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class UserHobbies(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserHobbyData', db_column='userId')
    hobbyId = models.ForeignKey(Hobbies, on_delete=models.CASCADE, related_name='HobbyData', db_column='hobbyId')

    def __str__(self):
        return self.userId

    class Meta:
        db_table = 'user_hobbies'


class UserGoalSettings(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserGoalData', db_column='userId')
    goalSettingsId = models.ForeignKey(GoalSettings, on_delete=models.CASCADE, related_name='GoalSettingsData',
                                       db_column='goalSettingsId')

    def __str__(self):
        return self.userId

    class Meta:
        db_table = 'user_goal_settings'


class UserWorkoutPreferences(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserWorkoutData', db_column='userId')
    workoutPreferencesId = models.ForeignKey(WorkoutPreferences, on_delete=models.CASCADE,
                                             related_name='WorkoutPreferenceData', db_column='workoutPreferencesId')

    def __str__(self):
        return self.userId

    class Meta:
        db_table = 'user_workout_preferences'


class UserDietaryPreferences(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserDietaryData', db_column='userId')
    dietaryPreferencesId = models.ForeignKey(DietaryPreferences, on_delete=models.CASCADE,
                                             related_name='DietaryPreferencesData', db_column='dietaryPreferencesId')

    def __str__(self):
        return self.userId

    class Meta:
        db_table = 'user_dietary_preferences'
