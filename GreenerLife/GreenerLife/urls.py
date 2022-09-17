
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import serve,static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    # 新增行
    # url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]