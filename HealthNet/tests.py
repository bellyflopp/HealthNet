from django.test import TestCase, Client
from HealthNet.models import PatientProfile, Hospital, DoctorProfile, NurseProfile, Appointment, Message, News
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, User
from django.utils import timezone

#tests fuctionality in models
class ModelsTests(TestCase):
    #sets up database
    def setUp(self):
        patient=User.objects.create(username="BobAcct", email="bob@hotmail.com", password="golisano17")
        doc=User.objects.create(username="testDoc", email="testDoc@gmail.com", password="hosp22412")
        nurse=User.objects.create(username="testNurse", email="testNurse@gmail.com", password="lolhi47")
        hosp=Hospital.objects.create(name="Sacred Heart", number=17, street="Smith Way", town="Henrietta",
                                      state="New York", zip=14623, phone="123-456-7890")
        docProf=DoctorProfile.objects.create(doctor=doc, houseNumber=12, street="Henrietta St", town="Rochester",
                                     state="New York", zip=12312, birthday="1960-12-01", gender="M",
                                     phone="122-432-3423", SSN="133-32-3513", hospital=hosp)
        nurseProf=NurseProfile.objects.create(nurse=nurse, houseNumber=185, street="Becky Way", town="Pittsford",
                                              state="New York", zip=23343, birthday="1967-12-05", gender="F",
                                              phone="425-535-4343", SSN="74-17-6655", hospital=hosp)
        patProf=PatientProfile.objects.create(patient=patient, birthday="1976-05-21", gender="M", phone="159-324-3432",
                                      houseNumber=284, street="Perkins St", town="Greece", state="New York",
                                      zip=14264, SSN="454-63-5363", emergencyContactFirst="Debra",
                                      emergencyContactLast="Smith", emergencyContactEmail="deb@yahoo.com",
                                      emergencyContactPhone="123-555-3920", height=61, weight=183,
                                      insuranceNum=33249, doctor=docProf, hospital=hosp, bloodType="O+")
        apt1=Appointment.objects.create(doctor=docProf, patient=patProf, hospital=hosp, time=datetime.time(10,0,0),
                                        date=datetime.date(2016,5,16))
        ap2=Appointment.objects.create(doctor=docProf, patient=patProf, hospital=hosp, time=datetime.time(11,0,0),
                                       date=datetime.date(2016,5,17))

        News.objects.create(date=datetime.datetime(2016, 1,12,12,00,00), content="test")

    def test_get_doc(self):
        pat1=PatientProfile.objects.get(SSN="454-63-5363")
        doc1=DoctorProfile.objects.get(SSN="133-32-3513")
        self.assertEqual(pat1.getDoctor(), doc1)

    def test_has_patient(self):
        pat1=PatientProfile.objects.get(SSN="454-63-5363")
        doc1=DoctorProfile.objects.get(SSN="133-32-3513")
        self.assertEqual(doc1.hasPatient(pat1), True)

    def test_appt_conflicts(self):
        pat1=PatientProfile.objects.get(SSN="454-63-5363")
        doc1=DoctorProfile.objects.get(SSN="133-32-3513")
        apt1=Appointment.objects.get(doctor=doc1, time="10:00:00", date="2016-05-16")
        hosp=Hospital.objects.get(name="Sacred Heart")
        aptConf=Appointment.objects.create(doctor=doc1, patient=pat1, hospital=hosp, time=datetime.time(10,5,0),
                                           date=datetime.date(2016,5,16))
        aptNoConf=Appointment.objects.create(doctor=doc1, patient=pat1, hospital=hosp, time=datetime.time(12,0,0),
                                             date=datetime.date(2016,5,16))

        self.assertEqual(aptConf.checkAppointment(), False)
        self.assertEqual(aptNoConf.checkAppointment(), True)

#tests fuctionality in views
class ViewsTests(TestCase):
    #sets up database
    def setUp(self):
        patient=User.objects.create_user(username="BobAcct", email="bob@hotmail.com", password="golisano17")
        doc=User.objects.create_user(username="testDoc", email="testDoc@gmail.com", password="hosp22412")
        nurse=User.objects.create(username="testNurse", email="testNurse@gmail.com", password="lolhi47")
        hosp=Hospital.objects.create(name="Sacred Heart", number=17, street="Smith Way", town="Henrietta",
                                      state="New York", zip=14623, phone="123-456-7890")
        docProf=DoctorProfile.objects.create(doctor=doc, houseNumber=12, street="Henrietta St", town="Rochester",
                                     state="New York", zip=12312, birthday="1960-12-01", gender="M",
                                     phone="122-432-3423", SSN="133-32-3513", hospital=hosp)
        nurseProf=NurseProfile.objects.create(nurse=nurse, houseNumber=185, street="Becky Way", town="Pittsford",
                                              state="New York", zip=23343, birthday="1967-12-05", gender="F",
                                              phone="425-535-4343", SSN="74-17-6655", hospital=hosp)
        patProf=PatientProfile.objects.create(patient=patient, birthday="1976-05-21", gender="M", phone="159-324-3432",
                                      houseNumber=284, street="Perkins St", town="Greece", state="New York",
                                      zip=14264, SSN="454-63-5363", emergencyContactFirst="Debra",
                                      emergencyContactLast="Smith", emergencyContactEmail="deb@yahoo.com",
                                      emergencyContactPhone="123-555-3920", height=61, weight=183,
                                      insuranceNum=33249, doctor=docProf, hospital=hosp, bloodType="O+")
        apt1=Appointment.objects.create(doctor=docProf, patient=patProf, hospital=hosp, time=datetime.time(10,0,0),
                                        date=datetime.date(2016,5,16))
        ap2=Appointment.objects.create(doctor=docProf, patient=patProf, hospital=hosp, time=datetime.time(11,0,0),
                                       date=datetime.date(2016,5,17))

        Message.objects.create(sender=doc, receiver=patient, body="First message",
                               timeStamp=timezone.now())
        Message.objects.create(sender=patient, receiver=doc, body="Second message",
                               timeStamp=timezone.now())
        News.objects.create(date=datetime.datetime(2016, 1,12,12,00,00), content="test")

        self.client=Client()
        docGroup=Group.objects.create(name="Doctors")
        docGroup.user_set.add(doc)

        #test appropriate response code on register page
    def test_register(self):
        response=self.client.get(reverse('register:reg'))
        self.assertEqual(response.status_code, 200)

    #test redirect if not logged in and trying to access messages
    def test_login_required_redirect(self):
        response=self.client.get('/message')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login')

    #logged in user attempting to access login page
    def test_already_logged_in_redirect(self):
        self.client.login(username="BobAcct", password="golisano17")
        response=self.client.get(reverse('login:HealthNet'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/HealthNet/')
        self.client.logout()

    #tests all appointments load on calendar
    def test_appts_load(self):
        self.client.login(username="BobAcct", password="golisano17")
        response=self.client.get('/HealthNet/#calendar')
        self.assertEqual(len(response.context['appointments']), 2)
        self.client.logout()

    #test all messages load
    def test_messages_load(self):
        self.client.login(username="BobAcct", password="golisano17")
        response=self.client.get('/HealthNet/#messages')
        self.assertEqual(len(response.context['messages']), 2)
        self.client.logout()








