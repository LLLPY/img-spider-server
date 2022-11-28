from django.urls import  re_path
from img_server.views import *
urlpatterns=[
    
    re_path(r'get_img/', get_img,name='get_img'),
    re_path(r'upload_img/', upload_img,name='upload_img'),
    re_path(r'',ImgView.as_view(),name='img'),

]