from rest_framework import viewsets
from rest_framework.decorators import action

from api_server.models import API
from api_server.serializers import ApiSerializers
from common.response import SucResponse


# Create your views here.
class ApiViewSet(viewsets.ModelViewSet):
    queryset = API.objects.all()
    serializer_class = ApiSerializers

    @action(methods=['post'], detail=False)
    def upload_api(self, request, *args, **kwargs):
        # upload_api
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.data.get('uid')
        is_exist = API.get_by_uid(uid)
        if not is_exist:
            API.create(**serializer.data)
            res = SucResponse('新增接口成功')
        else:
            msg = '该接口对象已上传...'
            print(msg)
            res = SucResponse(msg)
        return res

    @action(methods=['post'], detail=False)
    def status(self, request, *args, **kwargs):
        # 查询一个api的状态 is_crawled_api
        serializer = self.get_serializer(data=self.request.data, include_fields=['md5'])
        serializer.is_valid(raise_exception=True)
        md5 = serializer.data.get('md5')
        is_exist = API.objects.filter(md5=md5).exists()
        if is_exist:
            res = SucResponse('该接口已被爬取...', data={'status': True})
        else:
            res = SucResponse('该接口暂未爬取...', data={'status': False})
        return res
