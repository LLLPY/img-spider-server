from django.db import models
from page_server.models import Page, Keyword
from django.db.models import Q


# Create your models here.

class Img(models.Model):
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
    # 合格的图片
    QUALIFY = 0
    # 不合格的图片
    UNQUALIFY = 1
    QUALIFY_MAPPING = (
        (QUALIFY, '合格'),
        (UNQUALIFY, '不合格')
    )
    # 所属分类，根据哪个关键字爬取的就是哪个分类
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, db_column='关键字', verbose_name='关键字',help_text='关键字')
    # 原图
    url = models.URLField(db_column='图片地址', verbose_name='图片地址',help_text='图片地址')
    # 缩略图
    thumb_url = models.URLField(db_column='缩略图地址', verbose_name='缩略图地址',help_text='缩略图地址')

    # 唯一标识 建立索引
    uid = models.CharField(unique=True, db_index=True, max_length=100, db_column='唯一标识', verbose_name='唯一标识',help_text='唯一标识')

    # 爬取状态
    status = models.IntegerField(default=STATUS_UNCRAWL, choices=STATUS_MAPPING, db_column='状态', verbose_name='状态',help_text='状态')

    # 图片所在的页面
    page = models.ForeignKey(Page, on_delete=models.CASCADE, db_column='页面链接', verbose_name='页面链接',help_text='页面链接')

    # 爬取的时间
    crawl_time = models.DateTimeField(db_column='爬取时间', verbose_name='爬取时间',help_text='爬取时间')

    # 图片相关描述
    desc = models.CharField(max_length=1000, db_column='图片描述', verbose_name='图片描述',help_text='图片描述')

    qualify = models.IntegerField(default=1, choices=QUALIFY_MAPPING, db_column='是否合格', verbose_name='是否合格',help_text='是否合格')

    source = models.CharField(max_length=20, db_column='爬取源', verbose_name='爬取源',help_text='爬取源')

    class Meta:
        db_table = '图片'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示
        ordering = []

    # 根据keyword获取一个状态是未爬取的图片对象
    @classmethod
    def get_uncrawl_img_by_keyword(cls, keyword):
        img_obj = cls.objects.filter(keyword=keyword).first()
        # img_obj=cls.objects.filter(Q(keyword=keyword) & Q(status=cls.STATUS_UNCRAWL)).first()
        return img_obj, img_obj == None

    # to dict
    def to_dict(self):
        tmp_dict = {}
        tmp_dict['id'] = self.id
        tmp_dict['keyword'] = self.keyword
        tmp_dict['url'] = self.url
        tmp_dict['thumb_url'] = self.thumb_url
        tmp_dict['uid'] = self.uid
        tmp_dict['status'] = self.status
        tmp_dict['page_url'] = self.page.url
        tmp_dict['crawl_time'] = self.crawl_time
        tmp_dict['desc'] = self.desc
