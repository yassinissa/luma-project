from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Report  

@receiver(post_migrate)
def create_manager_group(sender, **kwargs):
    group, created = Group.objects.get_or_create(name="Manager")
    if created:
        content_type = ContentType.objects.get_for_model(Report)
        permissions = Permission.objects.filter(content_type=content_type, codename__in=["add_reports", "edit_reports"])
        group.permissions.set(permissions)
        print("Manager group created with permissions.")
