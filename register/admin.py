from django.contrib import admin
from HealthNet.models import PatientProfile, DoctorProfile, NurseProfile

admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)
