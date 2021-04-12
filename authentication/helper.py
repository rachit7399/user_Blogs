from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status

def Verify_Email(request, user, user_data, relativeLink):
    current_site = get_current_site(request).domain
    absurl = 'http://'+current_site+relativeLink+ str(user.uid )      
    email_body = 'Hi '+ "User" + \
        ' Use the link below to verify your email \n' + absurl
    data = {'email_body': email_body, 'to_email': user.email,
            'email_subject': 'Verify your email'} 
    send_mail('Verify your email' ,email_body, 'rbprimevideo@gmail.com',[user.email],)
    return Response(user_data, status = status.HTTP_201_CREATED)