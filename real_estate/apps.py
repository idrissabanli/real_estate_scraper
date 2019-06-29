from django.apps import AppConfig


class RealEstateConfig(AppConfig):
    name = 'real_estate'

    def ready(self):
        import real_estate.signals
        import real_estate.tasks
