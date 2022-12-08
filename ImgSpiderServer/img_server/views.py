import datetime

from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from img_server.models import Img
import json

# Create your views here.
from page_server.models import Keyword, Page


class ImgView(View):

    def get(self, request):
        return render(request, 'admin_index.html')


# 捕获异常并返回
def catch_error(func):
    def inner(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            response_data = {
                'code': '400',
                'msg': e.__repr__(),
                'data': None
            }
            print(e)
            return JsonResponse(response_data)
        return res

    return inner


# 根据keyword，返回该keyword下未爬取的图片
@catch_error
def get_uncrawl_img_by_keyword(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')

        img_obj = Img.get_uncrawl_img_by_keyword(keyword)
        img_dict = img_obj.to_dict() if img_obj else {}
        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': img_dict
        }
        return JsonResponse(response_data)


# 上传图片
@catch_error
def upload_img(request):
    if request.method == 'POST':
        img_list = json.loads(request.POST.get('img_list', '[]'))
        done = True
        for item in img_list:
            k = item['uid']
            img_str = cache.get(k)
            if not img_str:
                done = False  # 不是所有的图片都存在
                new_img_obj = Img()
                for attr in item:
                    if attr == 'keyword':
                        new_img_obj.keyword = Keyword.get_or_create(item['keyword'])
                    elif attr == 'page_url':
                        page = Page.objects.filter(url=item['page_url']).first()
                        new_img_obj.page = page
                    elif attr == 'crawl_time':
                        new_img_obj.crawl_time = datetime.datetime.fromtimestamp(item[attr])
                    else:
                        setattr(new_img_obj, attr, item[attr])
                if page:
                    new_img_obj.save()
                cache.set(k, item['url'])

        response_data = {
            'code': '200',
            'msg': '图片上传成功!',
            'data': {'done':done}
        }
        return JsonResponse(response_data)


# 检测重复的uid
@catch_error
def check_dup_uid(request):
    if request.method == 'POST':
        uid_list = json.loads(request.POST.get('uid_list', '[]'))
        res_uid_list = []
        for uid in uid_list:
            exist = cache.get(uid)
            if not exist:
                res_uid_list.append(uid)
            else:
                print('存在...')
        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': res_uid_list
        }
        return JsonResponse(response_data)


@catch_error
def get_ready_img_list(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        img_dict_list = Img.get_ready_img_list(keyword)
        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': img_dict_list
        }
        return JsonResponse(response_data)


@catch_error
def update_img(request):
    if request.method == 'POST':

        img_dict_list = json.loads(request.POST.get('img_list'))
        for img_dict in img_dict_list:
            img_obj = Img.objects.filter(uid=img_dict['uid']).first()
            img_obj.status = img_dict['status']
            img_obj.save()

        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': None
        }
        return JsonResponse(response_data)
