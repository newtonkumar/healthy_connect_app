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

#############provider#################
class ProviderUserRequest(ListView, LoginRequiredMixin):
    model = User
    paginate_by = 20
    template_name = 'userManagement/providerUserRequests.html'
    queryset = User.objects.filter(Q(isDeleted=False) & Q(isApproved__in=[1, 3])).order_by('-id')
    context_object_name = 'providerUsers'
    login_url = 'admin-login'


def changeRequestStatus(request, status, userId):
    user = User.objects.filter(id=userId).first()
    if not user:
        messages.warning(request, 'Incorrect userId')
        return redirect('provider-usr-requests')
    user.isApproved = status
    user.save()
    return redirect('provider-usr-requests')


def searchUserRequest(request):
    try:
        search_key = request.POST.get('q')
        query1 = Q(fullName__icontains=search_key) | Q(
            email__icontains=search_key) | Q(
            mobileNo__icontains=search_key)
        users = User.objects.filter((Q(query1) & Q(isDeleted=False) & Q(isApproved__in=[1, 3]))).all()
        paginator = Paginator(users, 20)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        context = {
            'providerUsers': users,
            'page_obj': page_obj,
            'InputText': search_key
        }
        return render(request, 'userManagement/providerUserRequests.html', context)
    except Exception as e:
        return redirect('provider-usr-requests')
    
def filterByStatus(request):
    status = request.POST.get('filter_status_id')
    users = User.objects.filter(Q(isDeleted=False) & Q(isApproved = status)).all()
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
        'providerUsers': users,
        'page_obj': page_obj,
        'SelectedType': status
    }
    return render(request, 'userManagement/providerUserRequests.html', context)

class ProviderApprovedUsers(ListView, LoginRequiredMixin):
    model = User
    paginate_by = 20
    template_name = 'userManagement/providerApprovedUsers.html'
    queryset = User.objects.filter(Q(isDeleted=False) & Q(isApproved =2)).order_by('-id')
    context_object_name = 'approvedUsers'
    login_url = 'admin-login'
