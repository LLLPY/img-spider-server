from django.core.cache import cache
from django.shortcuts import render

from img_server.views import catch_error
from page_server.models import Keyword, Page
from django.http import JsonResponse
import json


@catch_error
def keyword_list(request):
    if request.method == 'GET':
        keyword_list = Keyword.get_keyword_list()
        print(keyword_list)
        return JsonResponse({'keyword_list': keyword_list})


# 上传页面
@catch_error
def upload_page(request):
    if request.method == 'POST':
        img_list = json.loads(request.POST.get('page_list', '[]'))
        for item in img_list:
            k = item['uid']
            page_str = cache.get(k)
            if not page_str:
                new_page_obj = Page()
                for attr in item:
                    if attr == 'keyword':
                        new_page_obj.keyword = Keyword.get_or_create(item['keyword'])
                    else:
                        setattr(new_page_obj, attr, item[attr])
                new_page_obj.save()
                cache.set(k, item['url'], 24 * 60 * 60)
            # else:
            #     print('页面已经存在...', page_str)
        response_data = {
            'code': '200',
            'msg': '页面上传成功!',
            'data': None
        }
        return JsonResponse(response_data)


# 获取待消费的page
@catch_error
def get_ready_page(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', None)
        page_list = Page.get_ready_page_list(keyword)
        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': page_list
        }
        return JsonResponse(response_data)


@catch_error
def update_page(request):
    if request.method == 'POST':
        page_dict = json.loads(request.POST.get('page'))
        uid = page_dict.get('uid', '')
        page_obj = Page.objects.filter(uid=uid).first()
        if page_obj:
            page_obj.status = page_dict['status']
            page_obj.deep = page_dict['deep']

        page_obj.save()
        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': ''
        }
        return JsonResponse(response_data)
