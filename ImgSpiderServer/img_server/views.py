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
def get_img(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')

        img_obj, success = Img.get_uncrawl_img_by_keyword(keyword)
        print(img_obj, success)
        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': None
        }
        return JsonResponse(response_data)


# 上传图片
@catch_error
def upload_img(request):
    if request.method == 'POST':
        img_list = json.loads(request.POST.get('img_list', '[]'))
        for item in img_list:
            k = item['uid']
            img_str = cache.get(k)
            if not img_str:
                new_img_obj = Img()
                for attr in item:
                    if attr == 'keyword':
                        new_img_obj.keyword = Keyword.get_or_create(item['keyword'])
                    elif attr == 'page_url':
                        page = Page.objects.filter(url=item['page_url']).first()
                        new_img_obj.page = page
                    else:
                        setattr(new_img_obj, attr, item[attr])
                new_img_obj.save()
                cache.set(k, item['url'], 24 * 60 * 60)
            else:
                print('图片已经存在...', img_str)
        response_data = {
            'code': '200',
            'msg': '图片上传成功!',
            'data': None
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
