from django.apps import AppConfig


class KeywordServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keyword_server'
    verbose_name = '关键词管理'
    verbose_name_plural = verbose_name
