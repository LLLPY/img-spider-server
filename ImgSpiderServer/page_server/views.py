import json

from rest_framework import viewsets
from rest_framework.decorators import action
from common.response import SucResponse, ErrResponse
from page_server.models import Page
from page_server.serializers import PageSerializers


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializers

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        data = serializer.data
        return SucResponse(data=data)

    def create(self, request, *args, **kwargs):
        # upload_page
        page_list = json.loads(self.request.data.get('page_list', '[]'))
        for page in page_list:
            uid = page.get('uid')
            if not Page.get_by_uid(uid):
                serializer = self.get_serializer(data=page, exclude_fields=['desc', 'err_msg', 'api_url'])
                serializer.is_valid(raise_exception=True)
                try:
                    Page.create(**serializer.data)
                except Exception as e:
                    print(f'页面创建失败，该页面已存在,uid:{uid}')
            else:
                print('该页面对象已上传...')

        return SucResponse()

    @action(methods=['post'], detail=False)
    def get_ready_page(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, include_fields=['keyword'])
        serializer.is_valid(raise_exception=True)
        ready_page = Page.get_ready_page(serializer.data.get('keyword'))
        page_dict = ready_page.to_dict() if ready_page else {}
        return SucResponse(data=page_dict)

    @action(methods=['post'], detail=False)
    def update_page(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, include_fields=['page'])
        serializer.is_valid(raise_exception=True)
        page_dict = json.loads(self.request.data.get('page', '{}'))  # #TODO 不知道为什么这里serializer.data拿不到数据
        uid = page_dict.get('uid')
        page_obj = Page.get_by_uid(uid)
        if not page_obj:
            return ErrResponse(message='通过uid找不到page对象')

        for attr in ['status', 'desc', 'err_msg']:
            if hasattr(page_obj, attr):
                setattr(page_obj, attr, page_dict.get(attr))
        page_obj.save()
        return SucResponse()
