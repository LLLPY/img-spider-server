import datetime
from django.core.cache import cache
from rest_framework.decorators import action
from common.models import Keyword
from common.response import ErrResponse, SucResponse
from img_server.models import Img
from img_server.serializers import ImgSerializers
from rest_framework import viewsets
from page_server.models import API, Page


class ImgViewSet(viewsets.ModelViewSet):
    serializer_class = ImgSerializers
    queryset = Img.objects.all()

    @action(methods=['post'], detail=False)
    def get_uncrawl_img(self, request, *args, **kwargs):
        # 根据keyword，返回该keyword下未爬取的图片
        serializer = self.get_serializer(data=self.request.data, include_fields=['keyword', 'source'])
        serializer.is_valid(raise_exception=True)
        keyword = serializer.data.get('keyword')
        source = serializer.data.get('source')

        img_obj = Img.get_uncrawl_img(keyword=keyword, source=source)
        if not img_obj:
            return ErrResponse(message='无可用img')

        return SucResponse(data=img_obj.to_dict())

    @action(methods=['post', 'get'], detail=False)
    def upload_img(self, request, *args, **kwargs):
        '''上传图片'''
        serializer = self.get_serializer(data=self.request.data, include_fields=['img_list'])
        serializer.is_valid(raise_exception=True)
        res = ''
        done = True
        print(serializer.data)
        for img_dict in serializer.data.get('img_list', []):
            if not cache.get(img_dict.get('uid')):
                done = False  # 不是所有的图片都存在
                img_serializer = self.get_serializer(data=img_dict, exclude_fields=['img_list', 'uid_list'])
                img_serializer.is_valid(raise_exception=True)
                res = Img.create(**img_serializer.data)
                cache.set(img_dict['uid'], img_dict['url'], 60 * 60 * 24 * 365 * 10000)

        return SucResponse(data=res)

    @action(methods=['post'], detail=False)
    def check_dup_uid(self, request, *args, **kwargs):
        '''检查重复的uid'''
        serializer = self.get_serializer(data=self.request.data, include_fields=['uid_list'])
        serializer.is_valid(raise_exception=True)
        uid_list = serializer.data.get('uid_list', [])
        res = []
        for uid in uid_list:
            if not cache.has_key(uid):
                res.append(uid)
            else:
                print(f'{uid}存在...')

        return SucResponse(data=res)

    @action(methods=['post'], detail=False)
    def get_undownload_img_list(self, request, *args, **kwargs):
        '''未下载的图片'''
        serializer = self.get_serializer(data=self.request.data, include_fields=['keyword'])
        serializer.is_valid(raise_exception=True)
        data = Img.get_undownload_img_list(keyword=serializer.data.get('keyword'))
        return SucResponse(data=data)

    @action(methods=['post'], detail=False)
    def update_img(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, include_fields=['img_list'])
        serializer.is_valid(raise_exception=True)
        for img_dict in serializer.data.get('img_list'):
            img_obj = Img.get_by_uid(img_dict.get('uid'))
            if img_obj:
                for k in img_dict:
                    if hasattr(img_obj, k):
                        if k == 'keyword':
                            img_obj.keyword = Keyword.get_or_create(k)
                        elif k == 'api':
                            img_obj.api = API.get_by_uid(k)
                        elif k == 'page':
                            img_obj.page = Page.get_by_uid(k)
                        elif isinstance(getattr(img_obj, k), type(datetime)):
                            setattr(img_obj, k, datetime.datetime.fromtimestamp(img_dict[k]))
                img_obj.save()

        return SucResponse()
