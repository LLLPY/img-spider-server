"""ImgSpiderServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from api_server.views import ApiViewSet
from img_server.views import ImgViewSet
from keyword_server.views import KeywordViewSet
from page_server.views import PageViewSet

router = DefaultRouter(trailing_slash=False)
router.register('keyword_server', KeywordViewSet, basename='keyword_server')
router.register('api_server', ApiViewSet, basename='api_server')
router.register('page_server', PageViewSet, basename='page_server')
router.register('img_server', ImgViewSet, basename='img_server')

admin.site.site_header = 'Img-Spider管理后台'
admin.site.site_title = 'Img-Spider管理后台'
admin.site.index_title = 'Img-Spider管理后台'

urlpatterns = [
    path('img-spider-server/admin/', admin.site.urls),
    path(r'img-spider-server/', include(router.urls)),
    # path('img-spider-server/img_server/', include(('img_server.urls', 'img_server'), namespace='img_server')),
    # path('img-spider-server/page_server/', include(('page_server.urls', 'page_server'), namespace='page_server')),
    # path('img-spider-server/api/docs/', include_docs_urls(title='Img-Spider api docs')),
    path('', lambda request: render(request, 'admin_index.html'), name='admin_index'),

]
