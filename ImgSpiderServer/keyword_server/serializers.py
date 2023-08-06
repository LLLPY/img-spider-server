from rest_framework import serializers
from common.serializers import DynamicFieldsSerializer


class KeywordSerializers(DynamicFieldsSerializer):
    id = serializers.IntegerField(required=True, error_messages={'required': '关键字id不能为空'})
    name = serializers.CharField(required=True, error_messages={'required': '关键字不能为空'})
