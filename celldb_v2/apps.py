from django.apps import AppConfig


class CelldbV2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celldb_v2'
    def ready(self) -> None:
        import celldb_v2.signals