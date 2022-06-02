import django
from django.urls import path
from .views import UserRegistrationView,GetAllLicenseType,UserLoginView,ForgetPasswordUpdate
urlpatterns = [
    path('user/registration', UserRegistrationView.as_view()),
    path('license/type/list', GetAllLicenseType.as_view()),
    path('user/login', UserLoginView.as_view()),
    path('forget/password/update', ForgetPasswordUpdate.as_view())
]
