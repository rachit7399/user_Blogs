from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

class CreateBlogViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Blogs.objects.filter(user = request.user)  
        serializer = CreateBlogSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Blogs.objects.all()
        blog = get_object_or_404(queryset, pk=pk)
        serializer = CreateBlogSerializer(blog)
        return Response(serializer.data)

    def create(self, request):
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
            'message': 'object creation Successful',
            'data': serializer.data
        })  

    def update(self, request, pk):
        blog = Blogs.objects.get(uid = pk)
        if(request.data.get("title", []) != []):
            blog.title = request.data.get("title")
        if(request.data.get("content", []) != []):
            blog.content = request.data.get("content")    
        blog.save()
        serializer = CreateBlogSerializer(blog)
        return Response({
            'status': True,
            'message': 'update Successful',
            'data': serializer.data
        })
        
    def delete(self, request, pk):
        Blogs.objects.get(uid = pk).delete()
        return Response({
            'status': True,
            'message': 'Delete Successful',
            'data': []
        })

    @action(methods=["POST"],detail=False,url_path="comment/(?P<blog_id>[^/.]+)",url_name="comment")
    def comment(self, request, *args, **kwargs):
        try:
            blog_id = kwargs.pop('blog_id')
            blog = Blogs.objects.get(uid = blog_id)
            serializer = CommentSerializer(data={
                **request.data,
                **{
                    "user": request.user.uid,
                    "blog" : blog.uid
                }
            })   
            serializer.is_valid(raise_exception=True)   
            serializer.save()      
            return Response({
                'status': True,
                'message': 'comment Successful',
                'data': serializer.data
            })

        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"],detail=False,url_path="like/(?P<blog_id>[^/.]+)",url_name="like")
    def like(self, request, *args, **kwargs):
        try:
            blog_id = kwargs.pop('blog_id')
            blog = Blogs.objects.get(uid = blog_id)
            serializer = LikeSerializer(data={
                **{
                    "user": request.user.uid,
                    "blog" : blog.uid
                }
            })   
            serializer.is_valid(raise_exception=True)   
            serializer.save()      
            return Response({
                'status': True,
                'message': 'liked Successful',
                'data': serializer.data
            })

        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)
