from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User, Group

from .models import Feature, UserInfo, Report
from .serializers import FeatureSerializer, UserInfoSerializer, ReportSerializer

# ---------------------- Feature API ----------------------
class FeatureListCreateView(APIView):
    def get(self, request):
        features = Feature.objects.all()
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------- User Info API ----------------------
class UserInfoView(APIView):
    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user_info = UserInfo.objects.get(pk=pk)
        except UserInfo.DoesNotExist:
            return Response({"error": "UserInfo not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserInfoSerializer(user_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------- Role Checking API ----------------------
@api_view(['GET'])
def check_role(request, pk):
    try:
        user_info = UserInfo.objects.get(pk=pk)
        role = user_info.group.name if user_info.group else None
        return Response({"role": role})
    except UserInfo.DoesNotExist:
        return Response({"error": "UserInfo not found"}, status=404)

# ---------------------- API Overview ----------------------
@api_view(['GET'])
def api_overview(request):
    routes = {
        'api/features/': 'List all features',
        'api/userinfo/': 'List all user info',
    }
    return Response(routes)

# ---------------------- User Registration ----------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "Manager")  # Default role is Manager

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        # Assign user to a group
        group, created = Group.objects.get_or_create(name=role)
        user.groups.add(group)  

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User registered successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role
        }, status=status.HTTP_201_CREATED)

# ---------------------- Report Management ----------------------
class ReportView(APIView):
    permission_classes = [DjangoModelPermissions]

    @method_decorator(permission_required("core.add_reports", raise_exception=True))
    def post(self, request):
        data = request.data
        report = Report.objects.create(title=data["title"], content=data["content"])
        return Response({"message": "Report added successfully."}, status=status.HTTP_201_CREATED)

    @method_decorator(permission_required("core.edit_reports", raise_exception=True))
    def put(self, request, pk):
        try:
            report = Report.objects.get(pk=pk)
            data = request.data
            report.title = data.get("title", report.title)
            report.content = data.get("content", report.content)
            report.save()
            return Response({"message": "Report updated successfully."}, status=status.HTTP_200_OK)
        except Report.DoesNotExist:
            return Response({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

# ---------------------- Dashboard API ----------------------
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "message": "Welcome to the dashboard!",
            "username": user.username,
            "email": user.email,
            "role": user.groups.first().name if user.groups.exists() else "No Role"
        }, status=status.HTTP_200_OK)
