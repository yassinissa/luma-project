from rest_framework import serializers
from .models import Feature, UserInfo
from django.contrib.auth.models import Group,User

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['branch_name', 'manager_name', 'role', 'user']

    def create(self, validated_data):
        # Create the user
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)

        # Handle the role
        role = validated_data.pop("role", None)
        group = Group.objects.get_or_create(name=role)[0] if role else None
        validated_data["user"] = user

        # Save the UserInfo instance
        user_info = UserInfo.objects.create(**validated_data)

        # Assign the group to the user
        if group:
            user.groups.add(group)

        return user_info