from django.apps import AppConfig


class EventmgtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventmgt'

    def ready(self):
        import eventmgt.signals
