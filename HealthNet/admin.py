from django.contrib import admin
from HealthNet.models import Log, Hospital, Appointment, Message, FileUpload, TestModel, Prescription, Comment, Visit, News

'''
Administrator settings for viewing logs
'''
class LogAdmin(admin.ModelAdmin):
    list_display = ('type', 'time', 'username')
    list_filter = ['time','type']
    search_fields = ['username', 'type']


'''
Administrator settings for viewing Appointments
'''
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor_name', 'hospital_name', 'date', 'time')
    list_filter = ['date', 'time']
    search_fields = ['patient_name', 'doctor_name', 'hospital_name']

admin.site.site_header = 'HealthNet Administration'
admin.site.index_title = 'HealthNet Administration'
admin.site.register(Log, LogAdmin)
admin.site.register(Hospital)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Message)  #Temporary, keep until we can delete messages without admin. Make sure not in R2.
admin.site.register(FileUpload)
admin.site.register(TestModel)
admin.site.register(Prescription)
admin.site.register(Comment)
admin.site.register(Visit)
admin.site.register(News)
