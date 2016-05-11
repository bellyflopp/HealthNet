from django.conf.urls import url
from modprofile import views

urlpatterns = [
        #url(r'^(?P<pk>[0-9]+)/$', views.modprofile, name='profile')
        url(r'^$', views.modprofile, name='profile')
]