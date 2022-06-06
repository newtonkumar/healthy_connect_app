from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from auth_APIs.models import User
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


def adminLogin(request):
    if request.method == "GET":
        return render(request, 'userManagement/adminLogin.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            messages.warning(request, 'Incorrect username/password')
            return redirect('admin-login')
        else:
            if user.is_superuser == 1:
                login(request, user)
                return redirect('admin-dashboard')
            else:
                messages.warning(request, 'Not authenticate user')
            return redirect('admin-login')

@login_required(login_url='admin-login')
def adminDashboard(request):
    paitentUsers = User.objects.filter(
        Q(isDeleted=False))[:2]
    providersUsers = User.objects.filter(
        Q(isDeleted=False))[:2]
    context = {
        "patientUsers": paitentUsers,
        "providersUsers": providersUsers
    }
    return render(request, 'userManagement/adminDashboard.html', context)


def logoutAdmin(request):
    logout(request)
    return redirect('admin-login')