from django.db import models
import datetime
from api_server.models import API
from common.models import BaseModel
from keyword_server.models import Keyword


class Page(BaseModel):
    DEEP_MAPPING = (
        (1, '第一层'),
        (2, '第二层'),
        (3, '第三层'),
    )

    # 爬取状态
    status = models.IntegerField(default=BaseModel.STATUS_UNCRAWL, choices=BaseModel.STATUS_MAPPING,
                                 verbose_name='状态', help_text='状态')

    # 爬取深度，最大爬取深度为3
    deep = models.IntegerField(default=1, choices=DEEP_MAPPING, verbose_name='爬取深度',
                               help_text='爬取深度')

    api = models.ForeignKey(API, on_delete=models.CASCADE, blank=True, verbose_name='api',
                            help_text='api',
                            null=True)

    class Meta:
        db_table = '页面'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示
        ordering = ['-update_time']

    def __str__(self) -> str:
        return self.url

    @classmethod
    def get_ready_page(cls, keyword):
        obj = cls.objects.filter(status=cls.STATUS_UNCRAWL, deep__lte=3, keyword__name=keyword).first()
        if obj:
            obj.status = cls.STATUS_CRAWLING
            obj.save()
        return obj

    @classmethod
    def create(cls, **kwargs):
        keyword = Keyword.get_or_create(kwargs.get('keyword'))
        api = API.get_by_uid(kwargs.get('api_uid'))
        kwargs.update({
            'keyword': keyword,
            'api': api
        })
        _self = cls()
        for field in cls._meta.get_fields():
            setattr(_self, field.name, kwargs.get(field.name))
        return _self.save()
