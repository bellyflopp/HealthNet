from django.conf.urls import url
from medicalInfo import views

urlpatterns = [
        url(r'^$', views.medical, name='info')
]