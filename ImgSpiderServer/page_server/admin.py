from django.contrib import admin
from django.db.models import Q

from img_server.models import Img
from page_server.models import Keyword, Page
from django.utils.html import format_html


# Register your models here.

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    save_on_top = True
    save_on_bottom = True
    list_select_related = True
    save_as = True
    search_fields = ['name']
    list_filter = ['create_time']
    list_display = [
        'id',
        'name',
        'create_time',
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
    ]

    def img_count(self, obj):
        count = Img.objects.filter(keyword=obj).count()
        return count

    img_count.short_description = '图片总量'

    def img_crawled_count(self, obj):
        count = Img.objects.filter(Q(keyword=obj) & Q(status=Img.STATUS_CRAWLED)).count()
        return count

    img_crawled_count.short_description = '已爬取的图片'

    def img_uncrawl_count(self, obj):
        count = Img.objects.filter(Q(keyword=obj) & Q(status=Img.STATUS_UNCRAWL)).count()
        return count

    img_uncrawl_count.short_description = '待爬取的图片'

    def img_crawling_count(self, obj):
        count = Img.objects.filter(Q(keyword=obj) & Q(status=Img.STATUS_CRAWLIMG)).count()
        return count

    img_crawling_count.short_description = '正在爬取的图片'

    def img_error_count(self, obj):
        count = Img.objects.filter(Q(keyword=obj) & Q(status=Img.STATUS_ERROR)).count()
        return count

    img_error_count.short_description = '爬取错误的图片'

    def page_count(self, obj):
        count = Page.objects.filter(keyword=obj).count()
        return count

    page_count.short_description = '页面总量'

    def page_crawled_count(self, obj):
        count = Page.objects.filter(Q(keyword=obj) & Q(status=Page.STATUS_CRAWLED)).count()
        return count

    page_crawled_count.short_description = '已爬取的页面'

    def page_uncrawl_count(self, obj):
        count = Page.objects.filter(Q(keyword=obj) & Q(status=Page.STATUS_UNCRAWL)).count()
        return count

    page_uncrawl_count.short_description = '待爬取的页面'

    def page_crawling_count(self, obj):
        count = Page.objects.filter(Q(keyword=obj) & Q(status=Page.STATUS_CRAWLIMG)).count()
        return count

    page_crawling_count.short_description = '正在爬取的页面'

    def page_error_count(self, obj):
        count = Page.objects.filter(Q(keyword=obj) & Q(status=Page.STATUS_ERROR)).count()
        return count

    page_error_count.short_description = '爬取错误的页面'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    save_on_top = True
    save_on_bottom = True
    list_select_related = True
    save_as = True
    search_fields = [
        'keyword__name',
        'uid',

    ]
    list_filter = [
        'keyword__name',
        'uid',
        'status',
        'source',
        'deep',
        'crawl_time',

    ]
    list_display = [
        'id',
        'keyword',
        'uid',
        'status',
        'crawl_time',
        'source',
        'deep',
        'img_count',
        'img_crawled_count',
        'img_uncrawl_count',
        'img_crawling_count',
        'img_error_count',
        'page_url'
    ]

    def img_crawled_count(self, obj):
        count = Img.objects.filter(Q(page=obj) & Q(status=Img.STATUS_CRAWLED)).count()
        return count

    img_crawled_count.short_description = '已爬取的图片'

    def img_uncrawl_count(self, obj):
        count = Img.objects.filter(Q(page=obj) & Q(status=Img.STATUS_UNCRAWL)).count()
        return count

    img_uncrawl_count.short_description = '待爬取的图片'

    def img_crawling_count(self, obj):
        count = Img.objects.filter(Q(page=obj) & Q(status=Img.STATUS_CRAWLIMG)).count()
        return count

    img_crawling_count.short_description = '正在爬取的图片'

    def img_error_count(self, obj):
        count = Img.objects.filter(Q(page=obj) & Q(status=Img.STATUS_ERROR)).count()
        return count

    img_error_count.short_description = '爬取错误的图片'

    def page_url(self, obj):
        return format_html(f'<a href="{obj.url}" target="block">点击查看</a>')

    page_url.short_description = '页面地址'
