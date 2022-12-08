from django.db import models
import datetime

from django.db.models import Q


class Keyword(models.Model):
    # 关键字
    name = models.CharField(default='', max_length=50, unique=True, db_index=True, db_column='关键字', verbose_name='关键字',
                            help_text='关键字')

    # 创建时间
    create_time = models.DateTimeField(default=datetime.datetime.now, db_column='创建时间', verbose_name='创建时间',
                                       help_text='创建时间')

    class Meta:
        db_table = '关键字'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示
        ordering = ['create_time']

    @classmethod
    def get_keyword_list(cls):
        return [k[0] for k in cls.objects.values_list('name')]

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_or_create(cls, keyword):
        obj = cls.objects.filter(name=keyword).first()
        if not obj:
            obj = cls(name=keyword)
            obj.save()
        return obj


# Create your models here.
class Page(models.Model):
    # 待爬取
    STATUS_UNCRAWL = 0
    # 爬取中
    STATUS_CRAWLIMG = 1
    # 已爬取
    STATUS_CRAWLED = 2
    # 爬取错误
    STATUS_ERROR = 3
    # 状态(是否用于图片搜索了)
    STATUS_MAPPING = (
        (STATUS_UNCRAWL, '待爬取'),
        (STATUS_CRAWLIMG, '爬取中'),
        (STATUS_CRAWLED, '已爬取'),
        (STATUS_ERROR, '爬取错误'),
    )

    DEEP_MAPPING = (
        (1, '第一层'),
        (2, '第二层'),
        (3, '第三层'),
    )

    # 所属分类，根据哪个关键字爬取的就是哪个分类
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, db_column='关键字', verbose_name='关键字', help_text='关键字')

    url = models.URLField(db_index=True, db_column='页面地址', verbose_name='页面地址', help_text='页面地址',max_length=500)
    # 唯一标识
    uid = models.CharField(max_length=100, db_index=True, db_column='唯一标识', verbose_name='唯一标识', help_text='唯一标识')
    # 爬取状态 
    status = models.IntegerField(default=STATUS_UNCRAWL, choices=STATUS_MAPPING, db_column='状态', verbose_name='状态',
                                 help_text='状态')
    # 爬取的时间
    crawl_time = models.DateTimeField(db_column='爬取时间', verbose_name='爬取时间', help_text='爬取时间')

    source = models.CharField(max_length=20, db_column='爬取源', verbose_name='爬取源', help_text='爬取源')

    # 爬取深度，最大爬取深度为3
    deep = models.IntegerField(default=1, choices=DEEP_MAPPING, db_column='爬取深度', verbose_name='爬取深度', help_text='爬取深度')

    class Meta:
        db_table = '页面'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示
        ordering = ['-crawl_time']

    # 根据keyword获取一个未爬取的页面对象

    def __str__(self) -> str:
        return self.url

    @classmethod
    def get_ready_page_list(cls, keyword=None):
        objs = cls.objects.filter(Q(status=cls.STATUS_UNCRAWL) & Q(deep__lte=3))
        if keyword:
            objs = objs.filter(keyword__name=keyword)
        page_list = [obj.to_dict() for obj in objs[:50]]
        return page_list

    def to_dict(self):
        dict_con = {
            'url': self.url,
            'keyword': self.keyword.name,
            'uid': self.uid,
            'status': self.status,
            'source': self.source,
            'crawl_time': self.crawl_time.timestamp(),
            'deep': self.deep
        }
        return dict_con


