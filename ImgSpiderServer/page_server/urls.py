from django.urls import re_path,include
from page_server.views import *
from rest_framework.routers import DefaultRouter
from page_server.apis import *


router=DefaultRouter()
router.register(r'page',PageViewSet,basename='api-page')
router.register(r'keyword',KeywordViewSet,basename='api-keyword')

urlpatterns = [
    re_path(r'api/',include((router.urls,'api'),'api')),
    re_path(r'keyword_list/', keyword_list, name='keyword_list'),
    re_path(r'upload_page/', upload_page, name='upload_page'),
    re_path(r'get_ready_page/', get_ready_page, name='get_ready_page'),
    re_path(r'update_page/', update_page, name='update_page'),

]
