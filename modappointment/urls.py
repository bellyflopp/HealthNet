from django.conf.urls import url
from modappointment import views

urlpatterns = [
        url(r'^$', views.modappointment, name='appointment'),
        url(r'^S', views.delappointment, name='delappointment')
]
