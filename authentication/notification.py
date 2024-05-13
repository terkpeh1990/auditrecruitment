import threading
from django.http import request
from django.utils.datastructures import MultiValueDictKeyError
from auditrecruitment.settings import  endPoint,key,Sender_Id, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import requests
from django.core.mail import send_mail, EmailMessage

class  NotificationThread(threading.Thread):
    def __init__(self,user):
        self.user = user
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id

        usermessage =  'Dear ' + self.user.last_name +' ' +self.user.first_name  +','+'\nFind your application verification code below:\nVERIFICATION CODE: ' + str(self.user.code)
        phone = '233'+self.user.phone_number
        
        try:
            subject = "Audit Service Recruitment"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.user.email]
            send_mail(subject, message, sender, to)
            print('mail one success')
        except Exception as e:
            print(e)
            pass
       
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass

class  CompleteNotificationThread(threading.Thread):
    def __init__(self,user):
        self.user = user
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id

        usermessage =  'Dear ' + self.user.last_name +' ' +self.user.first_name  +','+'\nYou have successfully submitted your application.'
        phone = '233'+self.user.phone_number
        
        try:
            subject = "Audit Service Recruitment"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.user.email]
            send_mail(subject, message, sender, to)
            print('mail one success')
        except Exception as e:
            print(e)
            pass
       
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass