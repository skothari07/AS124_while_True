# While True (SIH 2020)

## Problem Statement ( AS124 ) :

Promoting holistic nutrition among women and children through/with the help of IT for Poshan Abhiyaan. Design a system for health worker to monitor and trigger alarms if some women/child have not come for upcoming dose. Additionally, if mobile number of the patient is registered then provide notification to them to get the dose.

## Team Members:

- Saurabh Kothari (Team Leader)
- Alen Biju
- Akhil R Abraham
- Paresh Pandit
- Rayan Crasta
- Saumya Purohit



## Overview:

We have thought of a solution that will bring every kind of target audience in action i.e we have a digital platform for various stakeholders 

**1) Web portal:** that will be used by health workers to register beneficiaries and reschedule their appointments in case they miss an appointment and many other features.

**2) Analytics:** so that government authorities can have a live feedback on the status, an interactive interface to analyse and increase the impact of the Abhiyaan Nation wide also it will help them to improvise and better decision making, which will lead to betterment of the Abhiyaan.

**3) Android app:** for beneficiaries which includes a notification section where they will receive notifications about their upcoming and missed appointments, FAQ section where they will be given general info about Poshan Abhiyaan and nutrition with Multilingual and text to speech feature,Help section where they can contact the local authorities via calling, Profile section to view their info

**4)Local/Phone messaging:** Those who do not have android phones will receive messages in their phone with all the details regarding there appointments.



## Project Modules:

### Web portal:

#### Health Worker

1. ​	Health Worker Login 
2. ​	Health Worker Dashboard
3. ​    Beneficiary Registration
4. ​	SMS Notification for Upcoming and Missed Appointments
5. ​	Beneficiary Monitoring
6. ​	Appointment Monitoring
7. ​	Automatic appointment generation
8. ​    Manual Appointment
9. ​    Appointment Rescheduling
10. ​	Beneficiary Verification 
11. ​	Health Monitoring
12. ​	Missed Appointments Monitoring



### Beneficiary

1. Beneficiary Login
2. Beneficiary Appointments
3. Beneficiary Health History Timeline



### Android App:

1. Beneficiary Automatic Login via OTP
2. Beneficiary Profile
3. Appointments Section (Multi Lingual)
4. FAQ Section : Multi Lingual and Text to Speech



### Real time Analytics Dashboard : 

1. Map Plotting
2. Filtering with State and Date
3. Interactive Graphs based on WHO standard BMI levels
4. Interactive  Graphs based on Financial Background
5. Interactive  Graphs based on Education 
6. Interactive  Enrolment Density per State



## Technology Stack:

### Web Portal:

- Django
- Twillio API
- Google Translate API
- Mysql (AWS RDS)



### Android App:

- Android Studio ( Java )
- PHP API
- Firebase 
- Mysql (AWS RDS)



### Realtime Analytics:

- Flask
- Plotly Dash
- Python (Pandas)



### Deployment:

- AWS EC2  with Nginx
- AWS RDS











