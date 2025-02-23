from rest_framework import serializers
from common.serializers import DynamicFieldsSerializer


class ImgSerializers(DynamicFieldsSerializer):
    keyword = serializers.CharField(error_messages={'required': '关键字不能为空'})
    url = serializers.CharField(error_messages={'required': 'url不能为空'})
    thumb_url = serializers.CharField(error_messages={'required': 'thumb_url不能为空'})
    uid = serializers.CharField(error_messages={'required': 'uid不能为空'})
    page_uid = serializers.CharField(error_messages={'required': 'page_uid不能为空'})
    desc = serializers.CharField(allow_null=True, allow_blank=True)
    source = serializers.CharField(error_messages={'required': 'source不能为空'})
    err_msg = serializers.CharField(allow_null=True, allow_blank=True)
    file_type = serializers.CharField(error_messages={'required': 'file_type不能为空'})
    api_url = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    api_uid = serializers.CharField(error_messages={'required': 'api_uid不能为空'})
    status_config = serializers.JSONField(error_messages={'required': 'status_config不能为空'})
    is_qualify = serializers.IntegerField()
    is_download = serializers.IntegerField()
    img_list = serializers.JSONField(error_messages={'required': 'img_list不能为空'})
    uid_list = serializers.JSONField(error_messages={'required': 'uid_list不能为空'})
