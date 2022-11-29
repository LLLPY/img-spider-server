from rest_framework.viewsets import ModelViewSet
from page_server.models import  *
from page_server.serializers import *

class KeywordViewSet(ModelViewSet):
    queryset=Keyword.objects.all()
    serializer_class=KeywordSerializers


class PageViewSet(ModelViewSet):
    queryset=Page.objects.all()
    serializer_class=PageSerializers