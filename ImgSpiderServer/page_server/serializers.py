from rest_framework import serializers
from page_server.models import *



class KeywordSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Keyword
        fields='__all__'



class PageSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Page
        fields='__all__'