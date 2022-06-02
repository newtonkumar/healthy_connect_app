from django.urls import path
from .views import (adminLogin, adminDashboard, logoutAdmin, ProviderUserRequest, changeRequestStatus,
                    searchUserRequest,
                    filterByStatus,
                    ProviderApprovedUsers
                    )

urlpatterns = [
    path('', adminLogin, name='admin-login'),
    path('admin-dashboard/', adminDashboard, name="admin-dashboard"),
    path('logout', logoutAdmin, name="logout-admin"),
    path('provider-user-requests/', ProviderUserRequest.as_view(), name='provider-usr-requests'),
    path('request-status-change/<int:status>/<int:userId>/', changeRequestStatus, name='change-status-user'),
    path('search-provider/', searchUserRequest, name='provider-search'),
    path('filter-by-status/', filterByStatus, name='filter-by-status'),
    path('approved-providers/', ProviderApprovedUsers.as_view(), name='approved-users-provider')
]
