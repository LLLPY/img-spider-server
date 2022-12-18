import datetime
from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from img_server.models import Img
import json
from page_server.models import Keyword, Page, API


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
        for img_dict in img_list:
            if not cache.get(img_dict['uid']):
                done = False  # 不是所有的图片都存在
                new_img_obj = Img()
                new_img_obj.keyword = Keyword.get_or_create(img_dict['keyword'])
                new_img_obj.url = img_dict['url']
                new_img_obj.thumb_url = img_dict['thumb_url']
                new_img_obj.uid = img_dict['uid']
                new_img_obj.status = img_dict['status']
                new_img_obj.page = Page.objects.filter(url=img_dict['page_url']).first()
                new_img_obj.crawl_time = datetime.datetime.fromtimestamp(img_dict['crawl_time'])
                new_img_obj.desc = img_dict['desc']
                new_img_obj.qualify = img_dict['qualify']
                new_img_obj.source = img_dict['source']
                new_img_obj.err_msg = img_dict['err_msg'][:500]
                new_img_obj.file_type = img_dict['file_type']
                new_img_obj.api = API.objects.filter(uid=img_dict['api']).first()
                new_img_obj.download = img_dict['download']
                try:
                    new_img_obj.save()
                except Exception as e:
                    print(e)
                cache.set(img_dict['uid'], img_dict['url'], 60 * 60 * 24 * 365 * 10)

        response_data = {
            'code': '200',
            'msg': '图片上传成功!',
            'data': {'done': done}
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


# @catch_error
def get_undownload_img_list(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        img_dict_list = Img.get_undownload_img_list(keyword)
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
            for k in img_dict:
                if k in ['api', 'page', 'keyword']:
                    pass
                elif k == 'crawl_time':
                    img_obj.crawl_time = datetime.datetime.fromtimestamp(img_dict['crawl_time'])
                else:
                    setattr(img_obj, k, img_dict[k])
            img_obj.save()

        response_data = {
            'code': '200',
            'msg': '响应成功!',
            'data': None
        }
        return JsonResponse(response_data)
