from django.conf.urls import url
from cal import views

urlpatterns = [
        url(r'^$', views.calendar, name='cal')
]
