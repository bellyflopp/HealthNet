Group: The Procrastinators (Group 3)
Team Members: Chris Lim, Cole Rogers, Kyle McVay, Soowon Moon, Maximillian McMullen

Developer Tool Versions:
Python 3.4.3
SQLite version 3.7.11
Django 1.9.1
PyCharm 5.0.3
FullCalender 2.6.1
JQuery 1.12.1

Prerequisites for proper execution of HealthNet (These steps MUST be followed in order):
- unzip any files submitted (files should come in proper format)
- execute commands in the directory containing manage.py in order:
    1)  "python3 manage.py migrate"
    2)  "python3 manage.py makemigrations"
    3)  "python3 manage.py migrate"
- Create a superuser executing the command "python3 manage.py createsuperuser" and create an admin
- Runserver using "python3 manage.py runserver"
- Open internet explorer or safari and navigate to either "localhost:8000/" or "http://127.0.0.1:8000/"
- Log in using your admin credentials
- Select admin site
- Click 'Add' on Groups
- Create Group "Doctors"
- Create Group "Nurses"
- Go home
- Click 'Add' on Hospital
- Create at least one Hospital
- Go home
- Click 'Add' on DoctorProfiles
- Click the green plus on users
- Enter the username and password for the doctor
- Click the yellow pen to create a name and email address for the user
- Scroll down to groups and double click on "Doctors"
- Make sure "Doctors" shows in the chosen groups
- Scroll down and save
- Finish filling in DoctorProfile and save (these steps can be repeated for any doctor)
- Go back home
- Click 'Add' on Newss
- Create at least one news objects
- Navigate to either "localhost:8000/" or "http://127.0.0.1:8000/"
You are now ready to start using HealthNet!


Things to note:
- When creating doctors make sure to add them to the "Doctors" group otherwise redirects may fail
- When creating nurses make sure to add them to the "Nurses" group otherwise redirects may fail
- When creating doctors or nurses make sure that you create a new user along with them by clicking the green plus next
    to "Doctor: " or "Nurse: " respectively
- When creating new users you can add information by clicking the pen once they are created and adding their first name,
    last name, and email.
- Admin's cannot see patient profiles however they can see all Users in the system. Make sure that none of these users
    are deleted to avoid conflicts with the patient profile.
- When creating users of any type, do not use the Django permissions built-in feature