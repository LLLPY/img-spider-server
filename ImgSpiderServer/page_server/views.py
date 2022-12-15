import datetime
from django.core.cache import cache
from img_server.views import catch_error
from page_server.models import Keyword, Page, API
from django.http import JsonResponse
import json


@catch_error
def keyword_list(request):
    if request.method == 'GET':
        keyword_list = Keyword.get_keyword_list()
        print(keyword_list)
        return JsonResponse({'keyword_list': keyword_list})


# 上传api
@catch_error
def upload_api(request):
    if request.method == 'POST':
        api_dict = json.loads(request.POST.get('api_dict', '{}'))
        api_uid = api_dict.get('uid')
        api_obj = API.get_by_uid(api_uid)
        if not api_obj:
            api_obj = API()
            for attr in api_dict:
                if attr == 'keyword':
                    api_obj.keyword = Keyword.get_or_create(api_dict['keyword'])
                elif attr == 'crawl_time':
                    api_obj.crawl_time = datetime.datetime.fromtimestamp(api_dict[attr])
                else:
                    setattr(api_obj, attr, api_dict[attr])
            api_obj.save()

        response_data = {
            'code': '200',
            'msg': 'api上传成功!',
            'data': None
        }
        return JsonResponse(response_data)


# @catch_error
def is_crawled_api(request):
    if request.method == 'POST':
        api_md5 = request.POST.get('api_md5')
        crawled = API.objects.filter(md5=api_md5).exists()

        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': {'crawled': crawled}
        }
        return JsonResponse(response_data)


# 上传页面
# @catch_error
def upload_page(request):
    if request.method == 'POST':
        page_list = json.loads(request.POST.get('page_list', '[]'))
        for item in page_list:
            k = item['uid']
            page_str = cache.get(k)
            if not page_str:
                new_page_obj = Page()
                for attr in item:
                    if attr == 'keyword':
                        new_page_obj.keyword = Keyword.get_or_create(item['keyword'])
                    elif attr == 'crawl_time':
                        new_page_obj.crawl_time = datetime.datetime.fromtimestamp(item[attr])
                    elif attr == 'api':
                        api_obj = API.objects.filter(uid=item['api']).first()
                        new_page_obj.api = api_obj
                    else:
                        setattr(new_page_obj, attr, item[attr])
                new_page_obj.save()


                cache.set(k, item['uid'], 60 * 60 * 24 * 365 * 10)
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
        keyword = request.POST.get('keyword')
        page_obj = Page.get_ready_page(keyword)
        page_dict = page_obj.to_dict() if page_obj else {}
        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': page_dict
        }
        return JsonResponse(response_data)


@catch_error
def update_page(request):
    if request.method == 'POST':
        page_dict = json.loads(request.POST.get('page'))
        uid = page_dict.get('uid', '')
        page_obj = Page.objects.filter(uid=uid).first()
        if page_obj:
            for attr in page_dict:
                if attr in {'crawl_time', 'keyword', 'api'}:
                    pass
                else:
                    setattr(page_obj, attr, page_dict[attr])
        page_obj.save()
        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': ''
        }
        return JsonResponse(response_data)
