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
            api_obj.keyword = Keyword.get_or_create(api_dict['keyword'])
            api_obj.url = api_dict['url']
            api_obj.uid = api_dict['uid']
            api_obj.source = api_dict['source']
            api_obj.crawl_time = datetime.datetime.fromtimestamp(api_dict['crawl_time'])
            api_obj.desc = api_dict['desc']
            api_obj.md5 = api_dict['md5']
            api_obj.err_msg = api_dict['err_msg'][:500]
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
        # print(1111, page_list)
        for page_dict in page_list:
            # page_str = cache.get(page_dict['uid'])
            # print(66666, page_str)
            # 改为直接在数据库中查找
            if not Page.objects.filter(uid=page_dict['uid']).exists():
                new_page_obj = Page()
                new_page_obj.keyword = Keyword.get_or_create(page_dict['keyword'])
                new_page_obj.url = page_dict['url']
                new_page_obj.uid = page_dict['uid']
                new_page_obj.status = page_dict['status']
                new_page_obj.crawl_time = datetime.datetime.fromtimestamp(page_dict['crawl_time'])
                new_page_obj.source = page_dict['source']
                new_page_obj.deep = page_dict['deep']
                new_page_obj.desc = page_dict['desc']
                new_page_obj.err_msg = page_dict['err_msg'][:490]
                new_page_obj.api = API.objects.filter(uid=page_dict['api']).first()
                new_page_obj.save()
            cache.set(page_dict['uid'], page_dict['url'], 60 * 60 * 24 * 365 * 10)
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
        page_obj = Page.objects.filter(uid=uid).first() or Page()
        page_obj.keyword = Keyword.get_or_create(page_dict['keyword'])
        page_obj.url = page_dict['url']
        page_obj.uid = page_dict['uid']
        page_obj.status = page_dict['status']
        page_obj.crawl_time = datetime.datetime.fromtimestamp(page_dict['crawl_time'])
        page_obj.source = page_dict['source']
        page_obj.deep = page_dict['deep']
        page_obj.desc = page_dict['desc']
        page_obj.err_msg = page_dict['err_msg'][:500]
        page_obj.api = API.objects.filter(uid=page_dict['api']).first()
        page_obj.save()
        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': ''
        }
        return JsonResponse(response_data)
