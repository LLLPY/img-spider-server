from django.contrib import admin
from django.utils.html import format_html

from api_server.models import API
from img_server.models import Img
from page_server.models import Page


# Register your models here.
@admin.register(API)
class APIAdmin(admin.ModelAdmin):
    save_on_top = True
    save_on_bottom = True
    list_select_related = True
    save_as = True
    search_fields = ['uid', 'md5']
    list_filter = [
        'keyword__name',
        'source',
        'update_time',
    ]
    list_display = [
        'id',
        'keyword',
        'uid',
        'md5',
        'update_time',
        'source',
        'desc',
        'err_msg',
        'img_count',
        'img_crawled_count',
        'img_uncrawl_count',
        'img_crawling_count',
        'img_error_count',
        'page_count',
        'page_crawled_count',
        'page_uncrawl_count',
        'page_crawling_count',
        'page_error_count',
        'api_operator',

    ]

    def img_count(self, obj):
        count = Img.objects.filter(api=obj).count()
        return count

    img_count.short_description = '图片总量'

    def img_crawled_count(self, obj):
        count = Img.objects.filter(api=obj,status=Img.STATUS_CRAWLED).count()
        return count

    img_crawled_count.short_description = '已爬取的图片'

    def img_uncrawl_count(self, obj):
        count = Img.objects.filter(api=obj,status=Img.STATUS_UNCRAWL).count()
        return count

    img_uncrawl_count.short_description = '待爬取的图片'

    def img_crawling_count(self, obj):
        count = Img.objects.filter(api=obj,status=Img.STATUS_CRAWLING).count()
        return count

    img_crawling_count.short_description = '正在爬取的图片'

    def img_error_count(self, obj):
        count = Img.objects.filter(api=obj,status=Img.STATUS_ERROR).count()
        return count

    img_error_count.short_description = '爬取错误的图片'

    def page_count(self, obj):
        count = Page.objects.filter(api=obj).count()
        return count

    page_count.short_description = '页面总量'

    def page_crawled_count(self, obj):
        count = Page.objects.filter(api=obj,status=Page.STATUS_CRAWLED).count()
        return count

    page_crawled_count.short_description = '已爬取的页面'

    def page_uncrawl_count(self, obj):
        count = Page.objects.filter(api=obj,status=Page.STATUS_UNCRAWL).count()
        return count

    page_uncrawl_count.short_description = '待爬取的页面'

    def page_crawling_count(self, obj):
        count = Page.objects.filter(api=obj,status=Page.STATUS_CRAWLING).count()
        return count

    page_crawling_count.short_description = '正在爬取的页面'

    def page_error_count(self, obj):
        count = Page.objects.filter(api=obj,status=Page.STATUS_ERROR).count()
        return count

    page_error_count.short_description = '爬取错误的页面'

    def api_operator(self, obj):
        return format_html(f'<a href="{obj.url}" target="block">点击查看</a>')

    api_operator.short_description = 'api地址'
