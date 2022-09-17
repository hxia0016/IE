
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import serve,static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]