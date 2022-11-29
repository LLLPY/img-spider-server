from rest_framework import serializers
from img_server.models import *
class ImgSerializers(serializers.ModelSerializer):
    
    # url=serializers.CharField(help_text='原图链接')
    
    class Meta:
        model=Img
        fields='__all__'