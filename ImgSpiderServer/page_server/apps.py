from django.apps import AppConfig


class PageServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'page_server'
    verbose_name='页面管理'
    verbose_name_plural = verbose_name