from django.urls import  re_path,include
from img_server.views import *
from rest_framework.routers import DefaultRouter
from img_server.apis import ImgViewSet


router=DefaultRouter()
router.register(r'img',ImgViewSet,basename='api-img')


urlpatterns=[
    re_path(r'api/',include((router.urls,'api'),'api')),
    re_path(r'get_uncrawl_img_by_keyword/', get_uncrawl_img_by_keyword,name='get_uncrawl_img_by_keyword'),
    re_path(r'upload_img/', upload_img,name='upload_img'),
    re_path(r'check_dup_uid/', check_dup_uid,name='check_dup_uid'),
    re_path(r'get_undownload_img_list/', get_undownload_img_list,name='get_undownload_img_list'),
    re_path(r'update_img/', update_img,name='update_img'),
    re_path(r'',ImgView.as_view(),name='img'),

]