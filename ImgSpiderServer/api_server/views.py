from rest_framework import viewsets
from rest_framework.decorators import action

from api_server.models import API
from api_server.serializers import ApiSerializers
from common.response import SucResponse


# Create your views here.
class ApiViewSet(viewsets.ModelViewSet):
    queryset = API.objects.all()
    serializer_class = ApiSerializers

    def create(self, request, *args, **kwargs):
        # upload_api
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        res = API.create(**serializer.data)
        return SucResponse(data=res)

    @action(methods=['post'], detail=False)
    def status(self, request, *args, **kwargs):
        # 查询一个api的状态 is_crawled_api
        serializer = self.get_serializer(data=self.request.data, include_fields=['md5'])
        serializer.is_valid(raise_exception=True)
        res = API.objects.filter(md5=serializer.data.get('md5')).exists()
        return SucResponse(data=res)
