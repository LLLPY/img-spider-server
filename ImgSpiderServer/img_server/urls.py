from django.urls import  re_path,include
from img_server.views import *
from rest_framework.routers import DefaultRouter
from img_server.apis import ImgViewSet


router=DefaultRouter()
router.register(r'img',ImgViewSet,basename='api-img')


urlpatterns=[
    re_path(r'api/',include((router.urls,'api'),'api')),
    re_path(r'get_img/', get_img,name='get_img'),
    re_path(r'upload_img/', upload_img,name='upload_img'),
    re_path(r'check_dup_uid/', check_dup_uid,name='check_dup_uid'),
    re_path(r'',ImgView.as_view(),name='img'),

]