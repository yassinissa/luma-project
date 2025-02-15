from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Feature, UserInfo
from .serializers import FeatureSerializer, UserInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required




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

@api_view(['GET'])
def check_role(request, pk):
    try:
        user_info = UserInfo.objects.get(pk=pk)
        role = user_info.group.name if user_info.group else None
        return Response({"role": role})
    except UserInfo.DoesNotExist:
        return Response({"error": "UserInfo not found"}, status=404)



@api_view(['GET'])
def api_overview(request):
    routes = {
        '/api/features/': 'List all features',
        '/api/userinfo/': 'List all user info',
    }
    return Response(routes)

class AssignRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRoleSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SomeOtherView(APIView):
    def get(self, request):
        return Response({"message": "This is the response from some_other_view."})
    
class UserInfoListCreateView(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    class CreateUserView(APIView):
     def post(self, request):
        """
        Admin creates a user and assigns them to a group.
        """
        data = request.data

        # Validate and create the user
        serializer = UserInfoSerializer(data=data)
        if serializer.is_valid():
            # Create user
            user = serializer.save()

            # Assign group to the user
            role = data.get("role", None)
            if role:
                # Check if the group exists; if not, create it
                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)  # Assign the user to the group

            return Response({"message": "User created and assigned to the role."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ReportView(APIView):
    # Decorate the POST method to require 'add_reports' permission
    @method_decorator(permission_required("core.add_reports", raise_exception=True))
    def post(self, request):
        # Add a new report
        data = request.data
        report = Report.objects.create(title=data["title"], content=data["content"])
        return Response({"message": "Report added successfully."}, status=status.HTTP_201_CREATED)

    # Decorate the PUT method to require 'edit_reports' permission
    @method_decorator(permission_required("core.edit_reports", raise_exception=True))
    def put(self, request, pk):
        
        # Edit an existing report
        try:
            report = Report.objects.get(pk=pk)
            data = request.data
            report.title = data.get("title", report.title)
            report.content = data.get("content", report.content)
            report.save()
            return Response({"message": "Report updated successfully."}, status=status.HTTP_200_OK)
        except Report.DoesNotExist:
            return Response({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)