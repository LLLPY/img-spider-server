from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from img_server.models import Img
import json


# Create your views here.


class ImgView(View):

    def get(self, request):
        return render(request,'admin_index.html')


# 根据keyword，返回该keyword下未爬取的图片
def get_img(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')

        img_obj, success = Img.get_uncrawl_img_by_keyword(keyword)
        print(img_obj, success)

        return JsonResponse({'msg': ''})


# 上传图片
def upload_img(request):
    if request.method == 'POST':
        img_list = json.loads(request.POST.get('img_list', '[]'))
        for item in img_list:
            k = item['uid']
            cache.set(k, json.dumps(item), 24 * 60 * 60)
        return JsonResponse({'status': 'success', 'msg': '图片上传成功!'})

