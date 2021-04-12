from django.db.models.query import QuerySet
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

# Create your views here.
class CreateBlogView(APIView):
    def get(self, request):
        try:  
            _data = [] 
            QuerySet = Blogs.objects.filter(user = request.user)   
            for blog in QuerySet:
                serializer = CreateBlogSerializer(blog)
                _data.append(serializer.data)

            return Response({
                'status': True,
                'message': 'Login Successful',
                'data': _data
            })

        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = CreateBlogSerializer(data={
                **request.data,
                **{
                    "user": request.user.uid,
                }
            })   
            serializer.is_valid(raise_exception=True)   
            serializer.save()      
            return Response({
                'status': True,
                'message': 'Login Successful',
                'data': serializer.data
            })

        except Exception:
            return Response({"blog creation Failed"}, status.HTTP_400_BAD_REQUEST)