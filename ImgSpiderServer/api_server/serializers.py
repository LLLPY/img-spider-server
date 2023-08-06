from rest_framework import serializers
from common.serializers import DynamicFieldsSerializer


class ApiSerializers(DynamicFieldsSerializer):
    keyword = serializers.CharField(required=True, error_messages={'required': '关键字不能为空'})
    url = serializers.CharField(required=True, error_messages={'required': 'url不能为空'})
    uid = serializers.CharField(required=True, error_messages={'required': 'uid不能为空'})
    source = serializers.CharField(required=True, error_messages={'required': 'source不能为空'})
    crawl_time = serializers.CharField(required=True, error_messages={'required': '爬取时间不能为空'})
    desc = serializers.CharField()
    md5 = serializers.CharField(required=True, error_messages={'required': 'md5不能为空'})
    err_msg = serializers.CharField()