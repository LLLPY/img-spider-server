from django.apps import AppConfig


class ImgServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'img_server'
    verbose_name='图片管理'
    verbose_name_plural = verbose_name

