from django.urls import path
from .views import api_overview
from .views import FeatureListCreateView, UserInfoView
from .views import check_role
from django.urls import path, include
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin




urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-info/', include('core.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('api/features/', FeatureListCreateView.as_view(), name='features'),
    path('api/user-info/', FeatureListCreateView.as_view(), name='user-info'),
]

urlpatterns = [
    path('user-info/', UserInfoView.as_view(), name='create-user-info'),
    path('user-info/<int:pk>/', UserInfoView.as_view(), name='update-user-info'),
]


urlpatterns += [
    path('user-role/<int:pk>/', check_role, name='check-user-role'),
    path('check-role/', check_role, name='check-role'),
]

urlpatterns = [
    path('create/', UserInfoView.as_view(), name='create-user-info'),
    path('update/<int:pk>/', UserInfoView.as_view(), name='update-user-info'),
    path('check-role/', check_role, name='check-role'),
]



