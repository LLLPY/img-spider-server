from django.contrib import admin
from django.db.models import Q
from img_server.models import Img
from page_server.models import Keyword, Page, API
from django.utils.html import format_html





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
        'status',
        'source',
        'deep',
        'update_time',

    ]
    list_display = [
        'id',
        'keyword',
        'uid',
        'status',
        'update_time',
        'source',
        'deep',
        'desc',
        'err_msg',
        'img_count',
        'img_crawled_count',
        'img_uncrawl_count',
        'img_crawling_count',
        'img_error_count',
        'page_operator',
        'api_operator'
    ]

    def api_operator(self, obj):
        if obj.api:
            res = format_html(f'<a href="{obj.api.url}" target="block">点击查看</a>')
        else:
            res = format_html(f'非api获取')
        return res

    api_operator.short_description = 'api地址'

    def img_count(self, obj):
        count = Img.objects.filter(page=obj).count()
        return count

    img_count.short_description = '页面上的图片'

    def img_crawled_count(self, obj):
        count = Img.objects.filter(Q(page=obj) & Q(status=Img.STATUS_CRAWLED)).count()
        return count

    img_crawled_count.short_description = '已爬取的图片'

    def img_uncrawl_count(self, obj):
        count = Img.objects.filter(Q(page=obj) & Q(status=Img.STATUS_UNCRAWL)).count()
        return count

    img_uncrawl_count.short_description = '待爬取的图片'

    def img_crawling_count(self, obj):
        count = Img.objects.filter(Q(page=obj) & Q(status=Img.STATUS_CRAWLING)).count()
        return count

    img_crawling_count.short_description = '正在爬取的图片'

    def img_error_count(self, obj):
        count = Img.objects.filter(Q(page=obj) & Q(status=Img.STATUS_ERROR)).count()
        return count

    img_error_count.short_description = '爬取错误的图片'

    def page_operator(self, obj):
        try:
            res = format_html(f'<a href="{obj.url}" target="block">点击查看</a>')
        except:
            res = '地址非法'
        return res

    page_operator.short_description = '页面地址'
