from django.db import models
from django.contrib.auth.models import Group,User

class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name



class UserInfo(models.Model):
    branch_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.manager_name
    
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_info")
    branch_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255) 
    

class Report(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("add_reports", "Can add reports"),
            ("edit_reports", "Can edit reports"),
        ]
