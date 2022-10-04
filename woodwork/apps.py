from django.apps import AppConfig

class WoodworkConfig(AppConfig):
    name = 'woodwork'

    def ready(self):
        from .signals import create_profile, save_profile
