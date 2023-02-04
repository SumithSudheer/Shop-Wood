
from rest_framework.views import APIView
from .serializers import FacultySerializer
from rest_framework.response import Response
from rest_framework import exceptions, generics, status
from django.core.mail import send_mail
# Create your views here.    
from smtplib import SMTP
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import faculty
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
import secrets
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
#faculty registration working pakka

class FacultyRegisterView(APIView):
    def post(self, request):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password
            faculty = serializer.save()
            email = request.data['email']
            name=request.data['name']
            print(email)
            #send a email to the faculty after registration
            mail_subject = f'Subject: {name} your booking is Pending'
            to_email = email
            body = "Your registration is pending... \nIf your selected we message confiramtion message to your whatsapp \nLogin Link: http://example.com/login \n\n\nACE EDUCATION CENTER"
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()
            response = {
                "messages" : "Your registration  is Pending,if you are select give a wahtsapp message ace education center.",
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
            
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class facultylogin(APIView):
    def get(self, request):
        email = request.data['email']
        passwords = request.data['password']
        try:
            tutor = faculty.objects.get(email=email)
            if tutor.is_verified==True:
                
                if check_password(passwords,tutor.password):
                    return Response(FacultySerializer(tutor).data)
                else:
                    return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "Your data validation is not completed..."})
        except faculty.DoesNotExist:
            return Response({"error": "Faculty with provided email does not exist."}, status=status.HTTP_404_NOT_FOUND)
import os
from dotenv import load_dotenv


#31-1-2023 vrification faculty is verified send to a whatsapp message
class adminfacultyverificationwithWhatsapp(APIView):
    # permission_classes=[IsAuthenticated]
    def post(self,request,id):
        users=get_object_or_404(faculty,id=id)
        print(users)
        phone=users.whatsapp_contact_number
        print(phone)
        if users.is_verified==False:
            print("is_vverified is false")
            users.is_verified=True
            users.save()
            load_dotenv()

            access_token = os.getenv("ACCESS_TOKEN")
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
                        
                        
            
            
         
            print("OOOOOOOOOOOOOOOO")
            payload = {
                "messaging_product": "whatsapp",
                "to": f'{phone}',
                "type": "template",
                "template": {
                    "name": "ace",
                    "language": {
                        "code": "en"
                    }
                }
            }
            response = requests.post(
                'https://graph.facebook.com/v15.0/113400621655857/messages',
                headers=headers,
                data=json.dumps(payload)
            )
            return Response({'status': response.status_code})
       
        if users.is_verified==True:
                print("is_vverified is false")
                users.is_verified=False
                users.save()
                load_dotenv()

                access_token = os.getenv("ACCESS_TOKEN")
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json',
                }
                             
                
                
                
                
                
                
             
                print("OOOOOOOOOOOOOOOO")
                payload = {
                    "messaging_product": "whatsapp",
                    "to": f'{phone}',
                    "type": "template",
                    "template": {
                        "name": "ace",
                        "language": {
                            "code": "en"
                        }
                    }
                }
                response = requests.post(
                    'https://graph.facebook.com/v15.0/113400621655857/messages',
                    headers=headers,
                    data=json.dumps(payload)
                )
                return Response({'status': response.status_code,'message':'you are blocked'})


class facultyforgotpassword(APIView):
    def get(self, request):
        email = request.data['email']
        try:
            totors = faculty.objects.get(email=email)
            if totors.is_verified==True:
                password = secrets.token_hex(nbytes=4) # it will generate 8 characters
                totors.password = make_password(password) # it will hash the password
                totors.is_verified=True
                totors.password=password
                totors.password = make_password(totors.password) # it will hash the password
                
                print(totors.password,'thsi is new password')
                totors.save()
                send_mail(
                    'Your password is changed',
                    'You have been successfully verified as a faculty member. Here is your new password: ' + password,
                    'from@example.com',
                    [totors.email],
                fail_silently=False,
                )
        except faculty.DoesNotExist:
            return Response({"error": "Faculty with provided email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'Your password is send to your email'},status=status.HTTP_201_CREATED)





















#working api 
import json
# import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response



# class facultylogin(APIView):
#     def get(self, request):
#         print("LLLLLL")
#         email = request.data['email']
#         passwords=request.data['password']
#         tutor = faculty.objects.get(email=email)
#         print(tutor.password)
#         if check_password(passwords, tutor.password):
#             print(passwords)
#             print(tutor.password)
#         #password is valid, proceed with login
#             try:
#                 tutor = faculty.objects.get(email=email)
#                 print(tutor.password,'this is tutor')
#             except faculty.DoesNotExist:
#                 return Response({"error": "Faculty with provided mobile number does not exist."}, status=status.HTTP_404_NOT_FOUND)
#                 print(email,'thsi is mobile number')
#                 print(passwords)
#         else:
#             print("else")
   
       
#         return Response(FacultySerializer(tutor).data)

       
        
       


















