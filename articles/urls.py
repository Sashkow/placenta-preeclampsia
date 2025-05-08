from django.urls import path
from . import views  # import views from current app

# URL patterns for the articles app
urlpatterns = [
    path('experiments/', views.experiments, name='experiments'),
    path('microarrays/', views.microarrays, name='microarrays'),
    path('samples/', views.samples, name='samples'),
    path('', views.home, name='home'),
]