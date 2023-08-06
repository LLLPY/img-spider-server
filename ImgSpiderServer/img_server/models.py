import datetime
from django.db import models
from common.models import BaseModel
from page_server.models import Page, Keyword, API
from django.db.models import JSONField


class Img(BaseModel):
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

    # 缩略图
    thumb_url = models.URLField(verbose_name='缩略图地址', help_text='缩略图地址', max_length=1000)

    status_config = JSONField(verbose_name='爬取状态配置')

    # 图片所在的页面
    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.CASCADE, verbose_name='页面链接',
                             help_text='页面链接')

    is_qualify = models.IntegerField(default=UNQUALIFY, choices=QUALIFY_MAPPING, verbose_name='是否合格',
                                     help_text='是否合格')

    # 文件类型
    file_type = models.IntegerField(default=0, choices=FILE_TYPE_MAPPING, verbose_name='文件类型',
                                    help_text='文件类型')

    # api
    api = models.ForeignKey(API, on_delete=models.CASCADE, verbose_name='api', help_text='api', null=True)

    # 是否已下载
    is_download = models.IntegerField(default=UNDOWNLOAD, choices=DOWNLOAD_MAPPING, verbose_name='下载状态',
                                      help_text='下载状态')

    class Meta:
        db_table = '图片'
        verbose_name_plural = verbose_name = db_table  # admin 后台显示
        ordering = []

    # 根据keyword获取一个状态是未爬取且是合格的图片对象
    @classmethod
    def get_uncrawl_img(cls, keyword, source):
        img_obj = cls.objects.filter(keyword__name=keyword, is_qualify=cls.QUALIFY).exclude(
            status_config__has_key=source).first()
        if img_obj:
            img_obj.status = cls.STATUS_CRAWLING
            img_obj.save()
        return img_obj

    @classmethod
    def get_undownload_img_list(cls, keyword):
        img_obj_list = cls.objects.filter(keyword__name=keyword, is_download=cls.UNDOWNLOAD)[:50]
        img_dict_list = []
        for img_obj in img_obj_list:
            img_obj.is_download = cls.DOWNLOADING
            img_obj.save()
            img_dict_list.append(img_obj.to_dict())
        return img_dict_list

    @classmethod
    def create(cls, keyword, url, thumb_url, uid, page_uid, update_time, desc, source, err_msg, file_type, api_uid,
               status_config):
        keyword = Keyword.get_or_create(keyword)
        print(11111, update_time, type(update_time))
        update_time = datetime.datetime.fromtimestamp(int(float(update_time)))
        page = Page.get_by_uid(page_uid)
        api = API.get_by_uid(api_uid)
        _self = cls(keyword=keyword, url=url, thumb_url=thumb_url, uid=uid, page=page, update_time=update_time,
                    desc=desc, source=source, err_msg=err_msg, file_type=file_type, api=api,
                    status_config=status_config)
        return _self.save()
