"""Healthnet URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from login.views import *
from HealthNet.views import *
from makeappointment.views import *
from modappointment.urls import *
from modappointment.views import modappointment
from cal.views import calendar
from message.views import message
from django.conf import settings
from django.conf.urls.static import static
from medicalInfo.views import *
from testresult.views import testresult, testsHome, testsFiles, modTest, releasetest
from modprofile.views import *
from comment.views import *

from django.views.generic.base import RedirectView
'''
To download files, url is HealthNet/serve?userid=(user's id here)&filename=(name of file, including file type here)
Example: HealthNet/serve?userid=1&filename=test.txt
To upload files, log in as a user, then go to doctor/upload
Files will be saved under HealthNet/files/uploads/user_(user id # here)
'''
urlpatterns = [
    url(r'^HealthNet/serve', serveFile),
    url(r'^doctor/serve', serveFile),
    url(r'^doctor/upload', upload),
    url(r'^doctor/testshome', testsHome),
    url(r'^HealthNet/export', exportData),
    url(r'^doctor/edittest', modTest),
    # url(r'^doctor/testresult', testresult),
    url(r'^doctor/testfiles', testsFiles),
    url(r'^doctor/releasetest', releasetest),
    url(r'^$', blank),
    url(r'^admin/statistics', statistics),
    url(r'^admin/home', adminhome),
    url(r'^admin/', admin.site.urls),
    url(r'^register/', include('register.urls',namespace='register')),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^logout/',user_logout),
    url(r'^HealthNet/#calendar?', modappointment),
    url(r'^HealthNet/#profile', home),
    url(r'^HealthNet/', home),
    url(r'^viewprofile?', viewprofile),
    url(r'^doctor/', doctor),
    url(r'^nurse/', nurse),
    url(r'^cal', calendar),
    url(r'^makedoctorappointment', makeappointmentdoctor),
    url(r'^makenurseappointment', makeappointmentnurse),
    url(r'^makeappointment', makeappointmentpatient),
    url(r'^medical', medical),
    url(r'^message', message),
    url(r'^modappointment', include('modappointment.urls', namespace='modappointment')),
    url(r'^delappointment', include('modappointment.urls', namespace='delappointment')),
    url(r'^transfer?', transfer),
    url(r'^discharge?', discharge),
    url(r'^comment', comment)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
