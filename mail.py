import smtplib
import random
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('emergencyresponse80@gmail.com','enter your app password')
otpnum = str(random.randint(100000,999999))
def send_mail_otp(email):
    server.sendmail('emergencyresponse80@gmail.com',email,"your veification code for emergency response system app is\n\n"+otpnum)

def send_mail_alert(email,name,loc):
    string="I am "+name+"You are my emergency contact i need help...\nThis is my approximate location: "+loc
    server.sendmail('emergencyresponse80@gmail.com',email,string)

def send_mail_booked(email,num,loc):
    string="AMBULANCE HAS BEEN BOOKED!!! \n Drivers number: "+num+" \nhere trace the location of the ambulance"+loc;
    server.sendmail('emergencyresponse80@gmail.com',email,string+"\n\n our life saviours are arriving....\n\n\nget well soon @CodeHunters")

def send_mail_driver(email):
    string="Emergency ambulance has been booked \n patients location is: https://www.google.com/maps/search/?api=1&query=12.938424,77.534852"
    server.sendmail('emergencyresponse80@gmail.com',email,string+"\n\n\n\n@CodeHunters")