import datetime

from django.db import models


class Keyword(models.Model):
    # 关键字
    name = models.CharField(default='', max_length=50, unique=True, db_index=True, verbose_name='关键字',
                            help_text='关键字')

    # 创建时间
    create_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间', help_text='创建时间')

    class Meta:
        db_table = '关键字'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示
        ordering = ['create_time']

    @classmethod
    def get_keyword_list(cls):
        return cls.objects.values_list('name', flat=True)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_or_create(cls, keyword):
        obj = cls.objects.filter(name=keyword).first()
        if not obj:
            obj = cls(name=keyword)
            obj.save()
        return obj

    def to_dict(self, *args, **kwargs):
        return {'id': self.id, 'name': self.name, 'create_time': str(self.create_time)}
