from django.apps import AppConfig


class ApiServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_server'
    verbose_name = 'API管理'
    verbose_name_plural = verbose_name
