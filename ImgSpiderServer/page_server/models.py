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


class API(models.Model):
    # 关键词
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, db_column='关键字', verbose_name='关键字', help_text='关键字')

    url = models.URLField(db_column='接口地址', verbose_name='接口地址', help_text='接口地址', max_length=1000)

    uid = models.CharField(unique=True, max_length=100, db_index=True, db_column='唯一标识', verbose_name='唯一标识',
                           help_text='唯一标识')

    # 爬取的时间
    source = models.CharField(max_length=20, db_column='爬取源', verbose_name='爬取源', help_text='爬取源')

    crawl_time = models.DateTimeField(db_column='爬取时间', verbose_name='爬取时间', help_text='爬取时间')

    desc = models.CharField(max_length=500, default='', blank=True, db_column='描述', verbose_name='描述', help_text='描述')

    # md5
    md5 = models.CharField(max_length=200, db_column='内容摘要', verbose_name='内容摘要', help_text='内容摘要')

    # 错误信息
    err_msg = models.CharField(max_length=500, default='', blank=True, db_column='错误信息', verbose_name='错误信息',
                               help_text='错误信息')

    class Meta:
        db_table = 'API'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示

    def __str__(self):
        return self.uid

    @classmethod
    def get_by_uid(cls, uid):
        return cls.objects.filter(uid=uid).first()


class Page(models.Model):
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

    DEEP_MAPPING = (
        (1, '第一层'),
        (2, '第二层'),
        (3, '第三层'),
    )

    # 所属分类，根据哪个关键字爬取的就是哪个分类
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, db_column='关键字', verbose_name='关键字', help_text='关键字')

    url = models.URLField(db_column='页面地址', verbose_name='页面地址', help_text='页面地址', max_length=1000)
    # 唯一标识
    uid = models.CharField(unique=True, max_length=100, db_index=True, db_column='唯一标识', verbose_name='唯一标识',
                           help_text='唯一标识')
    # 爬取状态 
    status = models.IntegerField(default=STATUS_UNCRAWL, choices=STATUS_MAPPING, db_column='状态', verbose_name='状态',
                                 help_text='状态')
    # 爬取的时间
    crawl_time = models.DateTimeField(db_column='爬取时间', verbose_name='爬取时间', help_text='爬取时间')

    source = models.CharField(max_length=20, db_column='爬取源', verbose_name='爬取源', help_text='爬取源')

    # 爬取深度，最大爬取深度为3
    deep = models.IntegerField(default=1, choices=DEEP_MAPPING, db_column='爬取深度', verbose_name='爬取深度', help_text='爬取深度')

    # desc
    desc = models.CharField(max_length=500, null=True, default='', blank=True, db_column='描述', verbose_name='描述',
                            help_text='描述')

    # 错误信息
    err_msg = models.CharField(max_length=500, null=True, default='', blank=True, db_column='错误信息', verbose_name='错误信息',
                               help_text='错误信息')

    api = models.ForeignKey(API, on_delete=models.CASCADE, db_column='api', blank=True, verbose_name='api',
                            help_text='api',
                            null=True)

    class Meta:
        db_table = '页面'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示
        ordering = ['-crawl_time']

    # 根据keyword获取一个未爬取的页面对象

    def __str__(self) -> str:
        return self.url

    @classmethod
    def get_ready_page(cls, keyword):
        obj = cls.objects.filter(Q(status=cls.STATUS_UNCRAWL) & Q(deep__lte=3) & Q(keyword__name=keyword)).first()
        if obj:
            obj.status = cls.STATUS_CRAWLING
            obj.save()
        return obj

    def to_dict(self):
        dict_con = {
            'url': self.url,
            'keyword': self.keyword.name,
            'uid': self.uid,
            'status': self.status,
            'source': self.source,
            'crawl_time': self.crawl_time.timestamp(),
            'deep': self.deep,
            'desc': self.desc,
            'err_msg': self.err_msg,
        }
        if self.api:
            dict_con['api'] = self.api.url
        else:
            dict_con['api'] = ''

        return dict_con
