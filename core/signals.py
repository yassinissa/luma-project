from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Report

@receiver(post_migrate)
def create_manager_group(sender, **kwargs):
    """
    Ensures the 'Manager' group is created and has the correct permissions after migrations.
    """
    if sender.name == "core":  # ✅ Run only for 'core' app
        manager_group, created = Group.objects.get_or_create(name="Manager")

        # Get the permissions for Report model
        report_content_type = ContentType.objects.get_for_model(Report)
        add_report_permission, _ = Permission.objects.get_or_create(
            codename="add_reports", content_type=report_content_type, name="Can add reports"
        )
        edit_report_permission, _ = Permission.objects.get_or_create(
            codename="edit_reports", content_type=report_content_type, name="Can edit reports"
        )

        # Assign permissions to the Manager group
        manager_group.permissions.add(add_report_permission, edit_report_permission)
