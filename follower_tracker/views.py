from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import follower
from authentication.models import User
from rest_framework import status

# Create your views here.
class FollowRequestView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            to_follow_user = User.objects.get(uid = pk)
            follower_user = request.user
            if(to_follow_user == follower_user):
                return Response({'data': "You cannot Follow Yourself "})
            if( follower.objects.filter(my_followers = follower_user).exists()):
                return Response({'data': "You Already Follow " + str(to_follow_user.uid)})
            if( follower.objects.filter(my_requests = follower_user).exists()):
                return Response({'data': "You have Already Requested " + str(to_follow_user.uid)})
            
            obj = follower()
            obj.user = to_follow_user

            if(to_follow_user.is_private):
                obj.my_requests = follower_user
                obj.save()
                return Response({'data': " Request Send " + str(to_follow_user.uid)})
            else:
                obj.my_followers = follower_user
                obj.save()
                return Response({'data': "You started Following " + str(to_follow_user.uid)})
            
            
        
        except User.DoesNotExist:
            return Response({"UnSuccessfull"}, status.HTTP_400_BAD_REQUEST)

