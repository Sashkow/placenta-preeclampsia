"""preeclampsia_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from grappelli import urls as grappelli_urls

# Admin autodiscovery is automatic in modern Django; explicit call no longer needed

urlpatterns = [
    # Grappelli administration interface
    path('grappelli/', include(grappelli_urls)),

    # Static files served in development
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    # Application URLs
    path('', include('articles.urls')),

    # Default admin site
    path('admin/', admin.site.urls),
]
