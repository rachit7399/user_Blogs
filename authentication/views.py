from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .helper import *
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        try:
            import pdb; pdb.set_trace()
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            relativeLink = "/auth/email-verify/"
            return Verify_Email(request, user, user_data, relativeLink)

        except Exception:
            return Response({"Resgisteration Failed"}, status.HTTP_400_BAD_REQUEST)        
       
class VerifyEmail(generics.GenericAPIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(uid = pk)
            user.is_verified = True
            user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"Not a valid token"}, status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        user = self.request.data
        try:
            
            for field in ['email', 'password']:
                if not user.get(field):
                    return Response({f"{field} is required"}, status.HTTP_400_BAD_REQUEST)
            
            _user = User.objects.get(email=self.request.data['email']) 

            if(_user.is_verified == False):
                return Response({"User is not Verified"}, status.HTTP_400_BAD_REQUEST)

            if not _user.check_password(self.request.data['password']):
                return Response({f"Incorrect Password "}, status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken.for_user(_user)
            serializer = LoginSerializer(_user)
            _data = serializer.data
            _data.update({'token': str(token.access_token)})
            del _data['password']
            _user.is_active = True
            _user.save()
            return Response({
                'status': True,
                'message': 'Login Successful',
                'data': _data
            })

        except Exception:
            return Response({f"{field} Doesn't Exists "}, status.HTTP_400_BAD_REQUEST)        

class ForgetPassView(generics.GenericAPIView):
    serializer_class = ForgetPassSerializer
    def post(self, request):
        try:
            user = self.request.data
            if not user.get('email'):
                return Response({f"Email is required"}, status.HTTP_400_BAD_REQUEST)   

            _user = User.objects.get(email=self.request.data['email'])   
            serializer = ForgetPassSerializer(_user)
            _data = serializer.data  
            relativeLink = "/auth/change-pass/"

            return Verify_Email(request, _user, _data, relativeLink)        
        
        except Exception:
            return Response({"User Not Found"}, status.HTTP_400_BAD_REQUEST)        

class ChangePassView(generics.GenericAPIView):
    serializer_class = ChangePassSerializer
    def post(self, request, pk):
        try:
            for field in ['confirm_pass', 'password']:
                if not self.request.data.get(field):
                    return Response({f"{field} is required"}, status.HTTP_400_BAD_REQUEST)
            if(self.request.data['password'] != self.request.data['confirm_pass']):
                return Response({"Password Dont Match"}, status.HTTP_400_BAD_REQUEST)

            _user = User.objects.get(uid = pk) 
            _user.set_password(request.data['password'])
            _user.save()
            return Response({"status":True, "message":"password changed sucessfully", "data":{}}, status = status.HTTP_201_CREATED)
        
        except Exception:
            return Response({"User Not Found"}, status.HTTP_400_BAD_REQUEST)

class TokenTestingView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReadProjectSerializer
    def get(self, request):
        try:
            user = request.user
            serializer = ReadProjectSerializer(user)
            _data = serializer.data   
            return Response({'data': _data})
        
        except User.DoesNotExist:
            return Response({"Not a valid token"}, status.HTTP_400_BAD_REQUEST)
