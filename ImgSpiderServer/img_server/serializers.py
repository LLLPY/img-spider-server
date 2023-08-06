from rest_framework import serializers
from common.serializers import DynamicFieldsSerializer


class ImgSerializers(DynamicFieldsSerializer):
    keyword = serializers.CharField(required=True, error_messages={'required': '关键字不能为空'})
    url = serializers.CharField(required=True, error_messages={'required': 'url不能为空'})
    thumb_url = serializers.CharField(required=True, error_messages={'required': 'thumb_url不能为空'})
    uid = serializers.CharField(required=True, error_messages={'required': 'uid不能为空'})
    page_uid = serializers.CharField(required=True, error_messages={'required': 'page_uid不能为空'})
    update_time = serializers.CharField()
    desc = serializers.CharField(required=True, error_messages={'required': 'desc不能为空'})
    source = serializers.CharField(required=True, error_messages={'required': 'source不能为空'})
    err_msg = serializers.CharField(required=True, error_messages={'required': 'err_msg不能为空'})
    file_type = serializers.CharField(required=True, error_messages={'required': 'file_type不能为空'})
    api_uid = serializers.CharField(required=True, error_messages={'required': 'api_uid不能为空'})

    img_list = serializers.ListField(required=True, error_messages={'required': 'img_list不能为空'})
    uid_list = serializers.ListField(required=True, error_messages={'required': 'uid_list不能为空'})
