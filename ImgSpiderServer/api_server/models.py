import datetime
from django.db import models
from common.models import BaseModel
from keyword_server.models import Keyword


# Create your models here.
class API(BaseModel):
    # md5
    md5 = models.CharField(max_length=200, db_column='内容摘要', verbose_name='内容摘要', help_text='内容摘要')

    class Meta:
        db_table = 'API'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示

    def __str__(self):
        return self.uid

    @classmethod
    def create(cls, keyword, url, uid, source, update_time, desc, md5, err_msg):
        keyword = Keyword.get_or_create(keyword)
        update_time = datetime.datetime.fromtimestamp(update_time)
        _self = cls(keyword=keyword, url=url, uid=uid, source=source, update_time=update_time, desc=desc, md5=md5,
                    err_msg=err_msg)
        return _self.save()
