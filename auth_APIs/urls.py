import django
from django.urls import path
from .views import UserRegistrationView, UserLoginView, ForgetPasswordUpdate, UserDetailsView, UserSearchDetailsView, \
    HobbyListView, GoalSettingsListView, WorkoutPreferencesListView, DietaryPreferencesListView
urlpatterns = [
    path('user/registration', UserRegistrationView.as_view()),
    path('user/login', UserLoginView.as_view()),
    path('user/<int:pk>', UserDetailsView.as_view()),
    path('user/search', UserSearchDetailsView.as_view()),
    path('forget/password/update', ForgetPasswordUpdate.as_view()),
    path('hobbies', HobbyListView.as_view()),
    path('goal-settings', GoalSettingsListView.as_view()),
    path('workout-preferences', WorkoutPreferencesListView.as_view()),
    path('dietary-preferences', DietaryPreferencesListView.as_view())
]
