from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from img_server.models import Img
import json

# Create your views here.
from page_server.models import Keyword, Page

RESPONSE_CODE_SUCCESS='200'
RESPONSE_CODE_FAIL='400'

DEFAULT_RETURN_CONTENT={
    'code':RESPONSE_CODE_SUCCESS,
    'msg':'响应成功!',
    'data':None
}


class ImgView(View):

    def get(self, request):
        return render(request, 'admin_index.html')


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
        
        return JsonResponse({'status': 'success', 'msg': '图片上传成功!'})

#检测重复的uid
def check_dup_uid(request):
    
    if request.method == 'POST':
        uid_list=json.loads(request.POST.get('uid_list','[]'))
        res_uid_list=[]
        for uid in uid_list:
            exist=cache.get(uid)
            if not exist:
                res_uid_list.append(uid)
        
            