from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.display, name='display'),
        url(r'^get_csv/$', views.get_csv , name='get_csv'),
]
