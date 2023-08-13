from rest_framework import serializers

from common.serializers import DynamicFieldsSerializer


class PageSerializers(DynamicFieldsSerializer):
    keyword = serializers.CharField(required=True, error_messages={'required': '关键字不能为空'})
    url = serializers.CharField(required=True, error_messages={'required': 'url不能为空'})
    uid = serializers.CharField(required=True, error_messages={'required': 'uid不能为空'})
    status = serializers.CharField(required=True, error_messages={'required': 'status不能为空'})
    update_time = serializers.CharField(required=False)
    source = serializers.CharField(required=True, error_messages={'required': 'source不能为空'})
    deep = serializers.CharField(required=True, error_messages={'required': 'deep不能为空'})
    desc = serializers.CharField(required=False, allow_null=True, error_messages={'required': 'desc不能为空'})
    err_msg = serializers.CharField(required=False, allow_null=True)
    api_url = serializers.CharField(required=True, error_messages={'required': 'api_url不能为空'})
    api_uid = serializers.CharField(required=True, error_messages={'required': 'api_uid不能为空'})
    # page = serializers.JSONField(required=True, error_messages={'required', 'page对象不能为空'})
    # page = serializers.JSONField()
