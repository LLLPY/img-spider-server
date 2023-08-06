from django.contrib import admin
from django.utils.html import format_html
from img_server.models import Img


@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    save_on_top = True
    save_on_bottom = True
    list_select_related = True
    save_as = True
    search_fields = ['keyword__name', 'uid', 'page__url']
    list_filter = [
        'keyword__name',
        'is_download',
        'source',
        'is_qualify',
        'update_time',

    ]
    list_display = [
        'id',
        'keyword',
        'status_config',
        'is_download',
        'update_time',
        'file_type',
        'source',
        'is_qualify',
        'uid',
        'desc',
        'err_msg',
        'url_operator',
        'thumb_url_operator',
        'page_url_operator',
        'api_operator',

    ]

    def api_operator(self, obj):
        if obj.api:
            res = format_html(f'<a href="{obj.api.url}" target="block">点击查看</a>')
        else:
            res = format_html(f'非api获取')
        return res

    api_operator.short_description = 'api地址'

    def url_operator(self, obj):
        return format_html(f'<a href="{obj.url}" target="block">点击查看</a>')

    url_operator.short_description = '原图链接'

    def thumb_url_operator(self, obj):
        return format_html(f'<a href="{obj.thumb_url}" target="block">点击查看</a>')

    thumb_url_operator.short_description = '缩略图'

    def page_url_operator(self, obj):
        return format_html(f'<a href="{obj.page}" target="block">点击查看</a>')

    page_url_operator.short_description = '所在页面'
