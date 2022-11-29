from rest_framework.viewsets import ModelViewSet
from img_server.models import *
from img_server.serializers import *
class ImgViewSet(ModelViewSet):
    queryset=Img.objects.all()
    serializer_class=ImgSerializers