"""preeclampsia_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

# import articles
"""
this is file with urls you can see line with admin/
 that describes all url for admin
"""


""" Default urlconf for config """

from django.conf.urls import include, url
from django.contrib import admin


from django.conf import settings
from django.contrib.auth.views import logout
from django.views.static import serve

from grappelli import urls as grappelli_urls

admin.autodiscover()


urlpatterns = [
    # Examples:
    # url(r'^$', 'config.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.STATIC_ROOT}),
    url(r'', include('articles.urls')), # means include urls that are in urls.py file in atricles app


    url(r'^admin/', admin.site.urls)
    
]