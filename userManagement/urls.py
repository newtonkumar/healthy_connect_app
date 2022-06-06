from django.urls import path
from .views import (adminLogin, adminDashboard, logoutAdmin)

urlpatterns = [
    path('', adminLogin, name='admin-login'),
    path('admin-dashboard/', adminDashboard, name="admin-dashboard"),
    path('logout', logoutAdmin, name="logout-admin")
]
