from rest_framework import viewsets

from common.response import SucResponse
from keyword_server.models import Keyword
from keyword_server.serializers import KeywordSerializers


class KeywordViewSet(viewsets.ModelViewSet):
    serializer_class = KeywordSerializers
    queryset = Keyword.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True, include_fields=['id', 'name'])
        data = serializer.data
        return SucResponse(data=data)