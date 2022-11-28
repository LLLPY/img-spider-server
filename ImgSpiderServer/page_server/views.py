from django.core.cache import cache
from django.shortcuts import render
from page_server.models import Keyword, Page
from django.http import JsonResponse
import json


def keyword_list(request):
    if request.method == 'GET':
        keyword_list = Keyword.get_keyword_list()
        print(keyword_list)
        return JsonResponse({'keyword_list': keyword_list})


# 上传页面
def upload_page(request):
    if request.method == 'POST':
        img_list = json.loads(request.POST.get('page_list', '[]'))
        for item in img_list:
            k = item['uid']
            page_str = cache.get(k)
            if page_str == None:
                new_page_obj = Page()
                for attr in item:
                    if attr == 'keyword':
                        new_page_obj.keyword = Keyword.get_or_create(item['keyword'])
                    else:
                        setattr(new_page_obj, attr, item[attr])
                new_page_obj.save()
                cache.set(k, item['url'], 24 * 60 * 60)

        return JsonResponse({'status': 'success', 'msg': '图片上传成功!'})
