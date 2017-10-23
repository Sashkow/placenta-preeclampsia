from django.conf.urls import url
from . import views # from the same folder as this file from


"""
this is urls file in articles app you can see address on top?
~/python/placen.../articles/urls.py
"""
# list of url patterns
urlpatterns = [ 
    url(r'^experiments', views.experiments, name='experiments'),
    url(r'^microarrays', views.microarrays, name='microarrays'),
    url(r'^samples', views.samples, name='samples'),
    url(r'^$',views.home, name='home')
]