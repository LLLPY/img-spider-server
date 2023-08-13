import json

from rest_framework import viewsets
from rest_framework.decorators import action
from api_server.models import API
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
            if not Page.get_by_uid(page.get('uid')):
                serializer = self.get_serializer(data=page, exclude_fields=['desc', 'err_msg'])
                serializer.is_valid(raise_exception=True)
                Page.create(**serializer.data)
            else:
                print('该页面对象已上传...')

        return SucResponse()

    @action(methods=['post'], detail=False)
    def get_ready_page(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, include_fields=['keyword'])
        serializer.is_valid(raise_exception=True)
        ready_page = Page.get_ready_page(serializer.data.get('keyword'))
        page_dict = ready_page.to_dict() if ready_page else {}
        print(333333, page_dict)
        return SucResponse(data=page_dict)

    @action(methods=['post'], detail=False)
    def update_page(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, include_fields=['page'])
        serializer.is_valid(raise_exception=True)
        page_dict = serializer.data.get('page', {})
        uid = page_dict.get('uid')
        page_obj = Page.get_by_uid(uid)
        print(page_obj)
        if not page_obj:
            return ErrResponse(message='通过uid找不到page对象')
        for attr in page_dict:
            if hasattr(page_obj, attr):
                setattr(page_obj, attr, page_dict.get(attr))
        page_obj.save()
        return SucResponse()
