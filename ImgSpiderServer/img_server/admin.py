from django.contrib import admin
from django.utils.html import format_html

from img_server.models import Img


# Register your models here.


@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    save_on_top = True
    save_on_bottom = True
    list_select_related = True
    save_as = True
    search_fields = ['keyword__name','uid']
    list_filter = [
        'keyword__name',
        'status',
        'source',
        'qualify',
        'uid',
        'crawl_time',

    ]
    list_display = [
        'id',
        'keyword',
        'status',
        'crawl_time',
        'source',
        'qualify',
        'uid',
        'desc',
        'url_operator',
        'thumb_url_operator',
        'page_url_operator',
    ]

    def url_operator(self, obj):
        return format_html(f'<a href="{obj.url}" target="block">点击查看</a>')

    url_operator.short_description = 'url'

    def thumb_url_operator(self, obj):
        return format_html(f'<a href="{obj.thumb_url}" target="block">点击查看</a>')

    thumb_url_operator.short_description = 'thumb_url'

    def page_url_operator(self, obj):
        return format_html(f'<a href="{obj.page}" target="block">点击查看</a>')

    page_url_operator.short_description = 'page_url'
