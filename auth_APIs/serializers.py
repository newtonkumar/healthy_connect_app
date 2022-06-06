from rest_framework.serializers import ModelSerializer
from .models import User, Hobbies, GoalSettings, DietaryPreferences, WorkoutPreferences, \
    UserHobbies, UserGoalSettings, UserWorkoutPreferences, UserDietaryPreferences
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'fullName', 'password', 'email', 'mobileNo', 'profileImage',
                  'deviceType', 'gender', 'lat', 'lng', 'zipCode', 'dob', 'phoneNumberCountryCode', 'age',
                  'activityLevel', 'height', 'currentWeight', 'goalWeight'
                  ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if "deviceToken" in validated_data:
            deviceToken = validated_data['deviceToken']
        else:
            deviceToken = None
        if "mobileNo" in validated_data:
            mobileNo = validated_data['mobileNo']
        else:
            mobileNo = None

        if "gender" in validated_data:
            gender = validated_data['gender']
        else:
            gender = None

        if "lat" in validated_data:
            lat = validated_data['lat']
        else:
            lat = None

        if "lng" in validated_data:
            lng = validated_data['lng']
        else:
            lng = None

        if "goals" in validated_data:
            goals = validated_data['goals']
        else:
            goals = None

        user = User.objects.create(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            fullName=validated_data["fullName"],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            phoneNumberCountryCode=validated_data['phoneNumberCountryCode'],
            age=validated_data['age'],
            activityLevel=validated_data['activityLevel'],
            height=validated_data['height'],
            currentWeight=validated_data['currentWeight'],
            goalWeight=validated_data['goalWeight'],
            mobileNo=mobileNo,
            deviceType=validated_data['deviceType'],
            gender=gender,
            lat=lat,
            lng=lng,
            zipCode=validated_data["zipCode"],
            dob=validated_data['dob']
        )
        return user


class HobbiesSerializer(ModelSerializer):
    class Meta:
        model = Hobbies
        fields = ['id', 'hobby', 'isActive']


class GoalSettingsSerializer(ModelSerializer):
    class Meta:
        model = GoalSettings
        fields = ['id', 'goal']


class WorkoutPreferencesSerializer(ModelSerializer):
    class Meta:
        model = WorkoutPreferences
        fields = ['id', 'preference', 'isActive']


class DietaryPreferencesSerializer(ModelSerializer):
    class Meta:
        model = DietaryPreferences
        fields = ['id', 'preference', 'isActive']


class UserHobbiesSerializer(ModelSerializer):
    class Meta:
        model = UserHobbies
        fields = ['hobbyId']


class UserGoalSettingsSerializer(ModelSerializer):
    class Meta:
        model = UserGoalSettings
        fields = ['goalSettingsId']


class UserWorkoutPreferencesSerializer(ModelSerializer):
    class Meta:
        model = UserWorkoutPreferences
        fields = ['workoutPreferencesId']


class UserDietaryPreferencesSerializer(ModelSerializer):
    class Meta:
        model = UserDietaryPreferences
        fields = ['dietaryPreferencesId']


class UserDetailsSerializer(ModelSerializer):
    UserHobbyData = UserHobbiesSerializer(many=True, read_only=True)
    UserGoalData = UserGoalSettingsSerializer(many=True, read_only=True)
    UserWorkoutData = UserWorkoutPreferencesSerializer(many=True, read_only=True)
    UserDietaryData = UserDietaryPreferencesSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'fullName', 'password', 'email', 'mobileNo', 'profileImage',
                  'deviceType', 'gender', 'lat', 'lng', 'zipCode', 'dob', 'phoneNumberCountryCode', 'age',
                  'activityLevel', 'height', 'currentWeight', 'goalWeight', 'UserHobbyData', 'UserGoalData',
                  'UserWorkoutData', 'UserDietaryData'
                  ]


class UserSearchDetailsSerializer(ModelSerializer):
    UserHobbyData = UserHobbiesSerializer(many=True, read_only=True)
    UserGoalData = UserGoalSettingsSerializer(many=True, read_only=True)
    UserWorkoutData = UserWorkoutPreferencesSerializer(many=True, read_only=True)
    UserDietaryData = UserDietaryPreferencesSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'fullName', 'email', 'mobileNo', 'profileImage',
                  'deviceType', 'gender', 'lat', 'lng', 'zipCode', 'dob', 'phoneNumberCountryCode', 'age',
                  'activityLevel', 'height', 'currentWeight', 'goalWeight', 'UserHobbyData', 'UserGoalData',
                  'UserWorkoutData', 'UserDietaryData'
                  ]

