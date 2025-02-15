from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Report
        import core.signals

        # Ensure the Manager group exists
        manager_group, created = Group.objects.get_or_create(name="Manager")

        # Get the permissions for Report
        report_content_type = ContentType.objects.get_for_model(Report)
        add_report_permission = Permission.objects.get(
            codename="add_reports", content_type=report_content_type
        )
        edit_report_permission = Permission.objects.get(
            codename="edit_reports", content_type=report_content_type
        )

        # Assign the permissions to the Manager group
        manager_group.permissions.add(add_report_permission, edit_report_permission)
