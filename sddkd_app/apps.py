from django.apps import AppConfig


class SddkdAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sddkd_app'

    def ready(self):
        import sddkd_app.signals
