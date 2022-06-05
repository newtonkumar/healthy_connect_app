
from django.contrib import admin
from django.urls import path, include # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/', include('auth_APIs.urls')),
    path('', include('userManagement.urls'))
]
