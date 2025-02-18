from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, DashboardView, FeatureListCreateView, 
    UserInfoView, check_role
)

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Authentication API
    path("api/register/", RegisterView.as_view(), name="register"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Dashboard API
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),

    # Features API
    path('api/features/', FeatureListCreateView.as_view(), name='features'),

    # User Info API
    path('api/user-info/', UserInfoView.as_view(), name='user-info'),
    path('api/user-info/<int:pk>/', UserInfoView.as_view(), name='update-user-info'),

    # Role Checking API
    path('api/user-role/<int:pk>/', check_role, name='check-user-role'),
    path('api/check-role/', check_role, name='check-role'),
]