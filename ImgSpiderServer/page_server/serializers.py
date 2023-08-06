from rest_framework import serializers

from common.serializers import DynamicFieldsSerializer

class PageSerializers(DynamicFieldsSerializer):
    keyword = serializers.CharField(required=True, error_messages={'required': '关键字不能为空'})
    url = serializers.CharField(required=True, error_messages={'required': 'url不能为空'})
    uid = serializers.CharField(required=True, error_messages={'required': 'uid不能为空'})
    status = serializers.CharField(required=True, error_messages={'required': 'status不能为空'})
    update_time = serializers.CharField(required=True, error_messages={'required': '爬取时间不能为空'})
    source = serializers.CharField(required=True, error_messages={'required': 'source不能为空'})
    deep = serializers.CharField(required=True, error_messages={'required': 'deep不能为空'})
    desc = serializers.CharField()
    err_msg = serializers.CharField()
    api = serializers.CharField(required=True, error_messages={'required': 'api不能为空'})
    # page = serializers.JSONField(required=True, error_messages={'required', 'page对象不能为空'})
    page = serializers.JSONField()



