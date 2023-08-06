from django.contrib import admin

from img_server.models import Img
from keyword_server.models import Keyword
from page_server.models import Page


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
        count = Img.objects.filter(keyword=obj).count()
        return count

    img_crawled_count.short_description = '已爬取的图片'

    def img_uncrawl_count(self, obj):
        count = Img.objects.filter(keyword=obj).count()
        return count

    img_uncrawl_count.short_description = '待爬取的图片'

    def img_crawling_count(self, obj):
        count = Img.objects.filter(keyword=obj).count()
        return count

    img_crawling_count.short_description = '正在爬取的图片'

    def img_error_count(self, obj):
        count = Img.objects.filter(keyword=obj).count()
        return count

    img_error_count.short_description = '爬取错误的图片'

    def page_count(self, obj):
        count = Page.objects.filter(keyword=obj).count()
        return count

    page_count.short_description = '页面总量'

    def page_crawled_count(self, obj):
        count = Page.objects.filter(keyword=obj, status=Page.STATUS_CRAWLED).count()
        return count

    page_crawled_count.short_description = '已爬取的页面'

    def page_uncrawl_count(self, obj):
        count = Page.objects.filter(keyword=obj, status=Page.STATUS_UNCRAWL).count()
        return count

    page_uncrawl_count.short_description = '待爬取的页面'

    def page_crawling_count(self, obj):
        count = Page.objects.filter(keyword=obj, status=Page.STATUS_CRAWLING).count()
        return count

    page_crawling_count.short_description = '正在爬取的页面'

    def page_error_count(self, obj):
        count = Page.objects.filter(keyword=obj, status=Page.STATUS_ERROR).count()
        return count

    page_error_count.short_description = '爬取错误的页面'
