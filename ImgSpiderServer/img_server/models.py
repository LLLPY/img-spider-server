import datetime

from django.db import models
from page_server.models import Page, Keyword, API
from django.db.models import Q


# Create your models here.

class Img(models.Model):
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
    # 合格的图片
    QUALIFY = 0
    # 不合格的图片
    UNQUALIFY = 1
    QUALIFY_MAPPING = (
        (QUALIFY, '合格'),
        (UNQUALIFY, '不合格')
    )

    # 文件类型
    FILE_IMAGE = 0
    FILE_VIDEO = 1
    FILE_TYPE_MAPPING = (
        (FILE_IMAGE, '图片'),
        (FILE_VIDEO, '视频')
    )

    # 是否已下载到本地
    UNDOWNLOAD = 0  # 未下载
    DOWNLOADED = 1  # 已下载
    DOWNLOADING = 2  # 下载中
    DOWNLOADERROR = 3  # 下载失败
    DOWNLOAD_MAPPING = (
        (UNDOWNLOAD, '未下载'),
        (DOWNLOADED, '已下载'),
        (DOWNLOADING, '下载中'),
        (DOWNLOADERROR, '下载失败'),

    )

    # 所属分类，根据哪个关键字爬取的就是哪个分类
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, db_column='关键字', verbose_name='关键字', help_text='关键字')
    # 原图
    url = models.URLField(db_column='图片地址', verbose_name='图片地址', help_text='图片地址', max_length=1000)
    # 缩略图
    thumb_url = models.URLField(db_column='缩略图地址', verbose_name='缩略图地址', help_text='缩略图地址', max_length=1000)

    # 唯一标识 建立索引
    uid = models.CharField(unique=True, max_length=100, db_index=True, db_column='唯一标识', verbose_name='唯一标识',
                           help_text='唯一标识')

    # 爬取状态
    status = models.IntegerField(default=STATUS_UNCRAWL, choices=STATUS_MAPPING, db_column='状态', verbose_name='状态',
                                 help_text='状态')

    # 图片所在的页面
    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.CASCADE, db_column='页面链接',
                             verbose_name='页面链接',
                             help_text='页面链接')

    # 爬取的时间
    crawl_time = models.DateTimeField(default=datetime.datetime.now, db_column='爬取时间', verbose_name='爬取时间',
                                      help_text='爬取时间')

    # 图片相关描述
    desc = models.CharField(max_length=1000, null=True, default='', db_column='图片描述', verbose_name='图片描述',
                            help_text='图片描述', blank=True)

    qualify = models.IntegerField(default=1, choices=QUALIFY_MAPPING, db_column='是否合格', verbose_name='是否合格',
                                  help_text='是否合格')

    source = models.CharField(max_length=20, db_column='爬取源', verbose_name='爬取源', help_text='爬取源')
    # 错误信息
    err_msg = models.CharField(max_length=500, null=True, default='', db_column='错误信息', verbose_name='错误信息',
                               help_text='错误信息', blank=True)

    # 文件类型
    file_type = models.IntegerField(default=0, choices=FILE_TYPE_MAPPING, db_column='文件类型', verbose_name='文件类型',
                                    help_text='文件类型')

    # api
    api = models.ForeignKey(API, on_delete=models.CASCADE, db_column='api', verbose_name='api', help_text='api',
                            null=True, blank=True)

    # 是否已下载
    download = models.IntegerField(default=UNDOWNLOAD, choices=DOWNLOAD_MAPPING, db_column='是否已下载',
                                   verbose_name='是否已下载', help_text='是否已下载')

    class Meta:
        db_table = '图片'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示
        ordering = []

    # 根据keyword获取一个状态是未爬取且是合格的图片对象
    @classmethod
    def get_uncrawl_img_by_keyword(cls, keyword):
        img_obj = cls.objects.filter(
            Q(keyword__name=keyword) & Q(qualify=cls.QUALIFY) & Q(status=cls.STATUS_UNCRAWL)).first()
        if img_obj:
            img_obj.status = cls.STATUS_CRAWLING
            img_obj.save()
        return img_obj

    @classmethod
    def get_undownload_img_list(cls, keyword):
        img_obj_list = cls.objects.filter(Q(keyword__name=keyword) & Q(download=cls.UNDOWNLOAD))[:50]
        img_dict_list = []
        for img_obj in img_obj_list:
            img_obj.download = cls.DOWNLOADING
            img_obj.save()
            img_dict_list.append(img_obj.to_dict())
        return img_dict_list

    # to dict
    def to_dict(self):
        tmp_dict = {}
        tmp_dict['id'] = self.id
        tmp_dict['keyword'] = self.keyword.name
        tmp_dict['url'] = self.url
        tmp_dict['thumb_url'] = self.thumb_url
        tmp_dict['uid'] = self.uid
        tmp_dict['status'] = self.status
        if self.page:
            tmp_dict['page_url'] = self.page.url
        else:
            tmp_dict['page_url'] = ''
        tmp_dict['crawl_time'] = self.crawl_time.timestamp()
        tmp_dict['desc'] = self.desc
        tmp_dict['qualify'] = self.qualify
        tmp_dict['source'] = self.source
        tmp_dict['err_msg'] = self.err_msg
        tmp_dict['file_type'] = self.file_type
        tmp_dict['download'] = self.download
        if self.api:
            tmp_dict['api'] = self.api.url
        else:
            tmp_dict['api'] = ''
        return tmp_dict
