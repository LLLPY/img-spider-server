import datetime
from django.db import models
from keyword_server.models import Keyword


class BaseModel(models.Model):
    # 待爬取
    STATUS_UNCRAWL = 0
    # 爬取中
    STATUS_CRAWLING = 1
    # 已爬取
    STATUS_CRAWLED = 2
    # 爬取错误
    STATUS_ERROR = 3
    # 状态(是否用于图片搜索了)
    STATUS_MAPPING = (
        (STATUS_UNCRAWL, '待爬取'),
        (STATUS_CRAWLING, '爬取中'),
        (STATUS_CRAWLED, '已爬取'),
        (STATUS_ERROR, '爬取错误'),
    )
    # 所属分类，根据哪个关键字爬取的就是哪个分类
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, verbose_name='关键字', help_text='关键字')
    # 原图
    url = models.URLField(verbose_name='地址', help_text='地址', max_length=1000)
    create_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间', help_text='更新时间')
    desc = models.CharField(max_length=500, null=True, default='', verbose_name='描述', help_text='描述')
    # 错误信息
    err_msg = models.CharField(max_length=500, null=True, default='', verbose_name='错误信息', help_text='错误信息')
    source = models.CharField(max_length=20, verbose_name='爬取源', help_text='爬取源')
    # 唯一标识 建立索引
    uid = models.CharField(unique=True, max_length=100, db_index=True, verbose_name='唯一标识', help_text='唯一标识')

    class Meta:
        abstract = True
        # ordering = ['-update_time']

    def to_dict(self, fields, exclude_list=None, extra_map=None):
        '''
        fields:需要转换的字段列表
        exclude_list:不需要转换的字段列表
        extra_map:需要二次to_dict的对象的配置表
        例如：
            blog:(title,author)--->author需要再次to_dict
            对于author的fields和exclude_list配置，可以写在extra_map中
            extra_map={
                'author':{
                    'fields':[],
                    'exclude_list':[],
                    }
            }
        '''
        fields = fields or self._meta.concrete_fields
        exclude_list = exclude_list or []
        extra_map = extra_map or {}
        con = {}
        for k in fields:
            if k not in exclude_list and hasattr(self, k):

                obj_v = getattr(self, k)
                # 需要再次to_dict
                if isinstance(obj_v, models.Model):
                    k_extra_map = extra_map.get(k, {})
                    _fields = k_extra_map.get('fields', None)
                    _exclude_list = extra_map.get('exclude_list', exclude_list)

                    if _fields:
                        con[k] = obj_v.to_dict(fields=_fields, exclude_list=_exclude_list,
                                               extra_map=extra_map)
                    else:
                        con[k] = obj_v.to_dict(exclude_list=_exclude_list, extra_map=extra_map)

                # 时间
                if isinstance(obj_v, type(datetime)):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')

                # 多对多关系的
                elif k in ['tags', 'blog_list']:
                    con[k] = [str(tag.to_dict(exclude_list=exclude_list, extra_map=extra_map)) for tag in
                              obj_v.all()]

                # 一般字段
                else:
                    con[k] = obj_v

        return con

    @classmethod
    def create(cls, **kwargs):
        _self = cls(**kwargs)
        return _self.save()

    @classmethod
    def get_by_uid(cls, uid):
        return cls.objects.filter(uid=uid).first()
