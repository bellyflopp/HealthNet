from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime
from HealthNet.static.localflavor.us.models import *
from itertools import chain

import sys

'''
class representing a hospital. It the name of the hospital and is linked to patients
and doctors via foreign keys
'''
class Hospital(models.Model):
    name = models.CharField(default='',max_length=100, verbose_name='Name')
    number = models.IntegerField(default=0, verbose_name='Number')
    street = models.CharField(max_length=50, default="", verbose_name='Street Name')
    town = models.CharField(max_length=50, default="", verbose_name='Town')
    state = USStateField(default="", verbose_name='State')
    zip = USZipCodeField(default="", verbose_name='Zip')
    phone = PhoneNumberField(default="", verbose_name='Phone Number')

    # returns str value for hospital
    def __str__(self):
        return str(self.name)
    # returns a list of all the employees in the hospital
    def getEmployees(self):
        return chain(DoctorProfile.objects.filter(hospital=self), NurseProfile.objects.filter(hospital=self))

    # returns a list of all the patients in a hospital
    def getPatients(self):
        return PatientProfile.objects.filter(hospital=self)

    # transfers a patient to this hospital.
    # patientProf is the patient to be transferred
    # newDoctor
    def transferPatient(self, patientProf, newDoctor):
        patientProf.hospital = self

        # doctor cannot be assigned to a patient if they aren't at the same hospital
        if newDoctor.hospital == self:
            patientProf.doctor = newDoctor
        else:
            print("Error, cannot assign doctor "+str(newDoctor)+" to patient "+str(patientProf)+" during transfer to hospital "+str(self))
            patientProf.doctor = None

        patientProf.save()

        return


######################################################################################################################
'''
model representing a doctor. Stores personal and employee information
'''
class DoctorProfile(models.Model):
    # key to the user
    doctor = models.ForeignKey(User, verbose_name='User')

    # The additional attributes we wish to include. Filled in with forms
    houseNumber = models.IntegerField(default=0, verbose_name='House number')
    street = models.CharField(max_length=50, default="", verbose_name='Street')
    town = models.CharField(max_length=50, default="", verbose_name='Town')
    state = USStateField(verbose_name='State')
    zip = USZipCodeField(verbose_name='Zip')
    birthday = models.DateField(default=timezone.now, verbose_name='Birthday(YYYY-MM-DD)')
    gender = models.CharField(max_length=1, choices=(('M', 'male'), ('F', 'female')), default="", verbose_name='Gender')
    phone = PhoneNumberField(verbose_name='Phone Number')
    SSN = USSocialSecurityNumberField(default="", verbose_name='Social Security Number')
    hospital = models.ForeignKey(Hospital, default=None, verbose_name='Hospital')

    # returns a str value of doctor
    def __str__(self):
        return self.doctor.username

    # returns whether doctor is on staff
    def is_staff(self):
        return True

    '''
    Check to see if there is a patient that has this doctor
    Return:
        True if the doctor has the patient
    '''
    def hasPatient(self,patient):
        # filter patients by doctor, then check to see if the patient profile is in the set
        return patient in PatientProfile.objects.filter(doctor__id=self.id)

    '''
    Get all of this doctor's patients
    '''
    def getPatients(self):
        return PatientProfile.objects.filter(doctor__id=self.id)


#######################################################################################################################
'''
model representing a nurse. stores personal and employee information
'''
class NurseProfile(models.Model):
    # This line is required. Links UserProfile to a Nurse model instance.
    nurse = models.ForeignKey(User, verbose_name='User')

    # The additional attributes we wish to include.
    houseNumber = models.IntegerField(default=0, verbose_name='House Number')
    street = models.CharField(max_length=50, default="", verbose_name='Street')
    town = models.CharField(max_length=50, default="", verbose_name='Town')
    state = USStateField(verbose_name='State')
    zip = USZipCodeField(verbose_name='Zip')
    birthday = models.DateField(default=timezone.now, verbose_name='Birthday(YYYY-MM-DD)')
    gender = models.CharField(max_length=1, choices=(('M', 'male'), ('F', 'female')), default="", verbose_name='Gender')
    phone = PhoneNumberField(verbose_name='Phone Number')
    SSN = USSocialSecurityNumberField(verbose_name='Social Security Number')
    hospital = models.ForeignKey(Hospital, default=None, verbose_name='Hospital')

    # returns str value of nurse
    def __str__(self):
        return self.nurse.username

    # returns whether nurse is on staff
    def is_staff(self):
        return True


#######################################################################################################################

'''
model representing a patient. Stores personal information.
'''
class PatientProfile(models.Model):
    # Links the patient to a user for authentication
    patient = models.ForeignKey(User, verbose_name='User')

    # profile information:

    birthday = models.DateField(default='', verbose_name='Birthday(YYYY-MM-DD)')
    gender = models.CharField(max_length=1, choices=(('M', 'male'), ('F', 'female')), default="", verbose_name='Gender')
    phone = PhoneNumberField(verbose_name='Phone Number')
    houseNumber = models.IntegerField(default=0, verbose_name='House Number')
    street = models.CharField(max_length=50, default="", verbose_name='Street')
    town = models.CharField(max_length=50, default="", verbose_name='Town')
    state = USStateField(verbose_name='State')
    zip = USZipCodeField(verbose_name='Zip')
    SSN = USSocialSecurityNumberField(verbose_name='Social Security Number')
    emergencyContactFirst = CharField(max_length=50,default="", verbose_name='Emergency Contact First Name')
    emergencyContactLast = CharField(max_length=50,default="", verbose_name='Emergency Contact Last Name')
    emergencyContactEmail = models.EmailField(default=None, verbose_name='Emergency Contact Email')
    emergencyContactPhone = PhoneNumberField(default=None, verbose_name='Emergency Contact Phone Number')

    # medical information (needs to be separate in views):

    height = models.IntegerField(default=0, verbose_name='Height(inches)')
    weight = models.IntegerField(default=0, verbose_name='Weight(pounds)')
    insuranceNum = models.IntegerField(default=0000000000, verbose_name='Insurance Number')
    doctor = models.ForeignKey(DoctorProfile, default=None, verbose_name='Doctor Username')
    hospital = models.ForeignKey(Hospital, default=None, verbose_name='Preferred Hospital')

    BLOOD_TYPE_CHOICES = (
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    bloodType = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, default="", verbose_name='Blood Type')

    #Admitted to hospital
    admissionStatus = models.BooleanField(default=False)

    # there is a one to many relationship with tests and prescriptions, done with a foreign key in the respective
    # models

    # returns a str value of patient
    def __str__(self):
        return self.patient.username

    # returns if patient is on staff
    def is_staff(self):
        return False

    # returns patients current doctor
    def getDoctor(self):
        return self.doctor

    '''
    Check if patient has the doctor (DoctorProfile)
    Return:
        True if the patient has the doctor
    '''
    def hasDoctor(self,doctor):
        # filter to get current patient in database, then filter to doctor. exists() checks to
        # see if there are any results in the set
        # this is not very efficient, but django doesn't make this kind of query easy
        return self.doctor.id == doctor.id

    '''
    get all patient's test results
    '''
    def getTests(self):
        return TestModel.objects.all().filter(patient__id=self.id)

    '''
    get patient's released test results
    '''
    def getReleasedTests(self):
        return TestModel.objects.all().filter(patient__id=self.id,isComplete=True)


######################################################################################################################

'''
model representing a log entry. Stores user, date, time and type of log
'''
class Log(models.Model):
    user = models.ForeignKey(User, verbose_name='User')
    username = models.CharField(default='',max_length=100, verbose_name='Username')

    time = models.DateTimeField(verbose_name='Date Logged')
    type = models.CharField(max_length=100, verbose_name='Type')

    # returns a str value of log
    def __str__(self):
        return self.type


######################################################################################################################

'''
Model representing an appointment, has foreign keys to the doctor, patient, and
hospital.
'''
class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, verbose_name='Doctor')
    patient = models.ForeignKey(PatientProfile, verbose_name='Patient')
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')
    time = models.TimeField(default=timezone.now, verbose_name='Time of appointment(HH:MM:SS, 24hr time)')
    date = models.DateField(default=timezone.now, verbose_name='Date of appointment(YYYY-MM-DD)')

    # redundant, will remove later
    patient_name = models.CharField(default='', max_length=100)
    doctor_name = models.CharField(default='', max_length=100)
    hospital_name = models.CharField(default='', max_length=100)

    def __str__(self):
        return "Appointment " + str(self.id)

    # 'get appointments' functionality done with simple queries where needed, query is in calender view
    # for example

    '''
    checks appointment validity by comparing the time of appointment. Appointment length
    will be assumed to be 30 minutes for the time being. This should be called before saving
    an appointment to the database. The appointment is checked against all other appointments
    containing the patient and the doctor in the database.
    Return:
    True if appointment is valid, false otherwise
    '''
    def checkAppointment(self):

        # query the appointments
        appointments = Appointment.objects.filter(doctor__id=self.doctor.id) | \
                       Appointment.objects.filter(patient__id=self.patient.id)

        # check to see if the patient has the doctor
        if( not self.patient.hasDoctor(self.doctor) ):
            print("Error, patient "+str(self.patient.id)+
                  " does not have doctor " + str(self.doctor.id),file=sys.stderr)
            return False

        for appt in appointments:

            # skip if the current appointment is the same as the one being checked
            if(appt.id==self.id):
                continue

            # merge date and time fields into a datetime field
            dateAppt = datetime.combine(appt.date,appt.time)
            dateSelf = datetime.combine(self.date,self.time)

            # get datetimes where appointment and self end, assumed to be 30 minutes after
            timeEnd= dateAppt + timedelta(minutes=30)
            timeSelfEnd= dateSelf + timedelta(minutes=30)

            # check if the appointment conflicts with the current appointment's time
            if( (dateAppt <= dateSelf <= timeEnd) or (dateAppt <= timeSelfEnd <= timeEnd) ):
                print("Error, appointment "+str(self.id)+
                      " conflicts with appointment "+str(appt.id),file=sys.stderr) # not actually an error,
                                                                                    # no idea why it's red in pycharm
                return False

        # no issues found, appointment is valid
        return True

    '''
    Returns a string that fullcalendar.io can understand. Messy, but
    fullcalendar is picky about the formatting
    '''
    def dateString(self):
        datestring=str(self.date.year)
        if(self.date.month<10):
            datestring+="-0"
        else:
            datestring+="0"
        datestring+=str(self.date.month)
        if(self.date.day<10):
            datestring+="-0"
        else:
            datestring+="-"
        datestring+=str(self.date.day)

        if(self.time.hour<10):
            datestring+="T0"
        else:
            datestring+="T"
        datestring+=str(self.time.hour)
        if(self.time.minute<10):
            datestring+=":0"
        else:
            datestring+=":"
        datestring+=str(self.time.minute)
        if(self.time.second<10):
            datestring+=":0"
        else:
            datestring+=":"
        datestring+=str(self.time.second)

        return datestring

    '''
    Returns a string representing the end time for fullcalendar.io
    '''
    def dateStringEnd(self):
        date=datetime.combine(self.date,self.time)
        date += timedelta(minutes=30)

        datestring=str(date.year)
        if(date.month<10):
            datestring+="-0"
        else:
            datestring+="0"
        datestring+=str(date.month)
        if(date.day<10):
            datestring+="-0"
        else:
            datestring+="-"
        datestring+=str(date.day)

        if(date.hour<10):
            datestring+="T0"
        else:
            datestring+="T"
        datestring+=str(date.hour)
        if(date.minute<10):
            datestring+=":0"
        else:
            datestring+=":"
        datestring+=str(date.minute)
        if(date.second<10):
            datestring+=":0"
        else:
            datestring+=":"
        datestring+=str(date.second)

        return datestring

######################################################################################################################

'''
Model that represents a message between two users
'''
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', default=None, verbose_name='Sender')
    receiver = models.ForeignKey(User, related_name='reciever', default=None, verbose_name='To')
    body = models.TextField(max_length=200, default='', verbose_name='Message')
    timeStamp = models.DateTimeField(default=None, verbose_name='Sent Data')


######################################################################################################################

'''
Model representing a prescription
'''
class Prescription(models.Model):
    patient = models.ForeignKey(PatientProfile, default=None, verbose_name='Patient')
    doctor = models.ForeignKey(DoctorProfile, default=None, verbose_name='Doctor')
    name = models.TextField(max_length=30, default='', verbose_name='Name')
    date = models.DateField(default=timezone.now, verbose_name='Date(YYYY-MM-DD)')
    note = models.TextField(max_length=200, default='', verbose_name='Note')


######################################################################################################################

'''
Model representing test results
'''
class TestModel(models.Model):
    patient = models.ForeignKey(PatientProfile, default=None, verbose_name='Patient')
    doctor = models.ForeignKey(DoctorProfile, default=None, verbose_name='Doctor')
    testName = models.TextField(max_length=30, default='', verbose_name='Name')
    result = models.TextField(max_length=50, default='', verbose_name='Result')
    notes = models.TextField(max_length=200, default='', verbose_name='Notes')
    isComplete = models.BooleanField(default=False)
    isReleased = models.BooleanField(default=False)

######################################################################################################################

'''
Model for a file uploaded by a doctor. Pictures can be uploaded with same model.
'''
class FileUpload(models.Model):
    user = models.ForeignKey(User, related_name="user", verbose_name='Username')
    userid = models.TextField(max_length=10, default='', verbose_name='Id')
    test = models.ForeignKey(TestModel, related_name="test", default=None, verbose_name='Test')#each upload is linked to a test, set on creation
    shortname = models.TextField(max_length=100, default='', verbose_name='Name')

    def userPath(instance, filename):
        path = "uploads/user_%s/%s" % (instance.user.id, filename)
        return path

    file = models.FileField(upload_to=userPath, verbose_name='File')

#####################################################################################################################

'''
Model representing comments left by doctors on a test
'''

class Comment(models.Model):
    patient = models.ForeignKey(PatientProfile, default=None, related_name="patient_for_comment", verbose_name="Patient for Comment")
    test = models.ForeignKey(TestModel, related_name="test_for_comment", verbose_name='Test to comment')
    author = models.ForeignKey(User, related_name="author_for_comment", verbose_name='Author')
    comment = models.TextField(max_length=200,default='', verbose_name='Comment')

#####################################################################################################################

'''
Model representing a patient visit, either short or extended. A non null discharge date means that the patient
has been discharged
'''

class Visit(models.Model):
    patient = models.ForeignKey(PatientProfile,default=None)
    reason = models.TextField(max_length=100,default='',verbose_name='Reason for Visit')
    admitDate = models.DateTimeField(verbose_name='Admission Date')

class News(models.Model):
    date = models.DateTimeField(verbose_name="News Date")
    content = models.TextField(max_length=200, default='', verbose_name='News')