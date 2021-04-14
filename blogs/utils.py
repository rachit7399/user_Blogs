from rest_framework import filters
from .models import Tags
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .serializers import CommentSerializer, LikeSerializer
from rest_framework import status


def get_tags_list(lst_with_tag_name):
    lst_with_tag_uid = []
    for i in lst_with_tag_name:
        lst_with_tag_uid.append(Tags.objects.get(name = i).uid)
    return lst_with_tag_uid

class BaseFilterMixin:
    search_fields = ['tag']
    filter_backends = (filters.SearchFilter, )
    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

class CrudMixin:
    def list(self, request):
        queryset = self.model_class.objects.filter(user = request.user)  
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.model_class.objects.all()
        blog = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(blog)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data={
            **{
                "title": request.data["title"],
                "content": request.data["content"],
                "user": request.user.uid,
                "tags": get_tags_list(request.data["tags"])
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
        blog = self.model_class.objects.get(uid = pk)
        if(request.data.get("title", []) != []):
            blog.title = request.data.get("title")
        if(request.data.get("content", []) != []):
            blog.content = request.data.get("content")    
        blog.save()
        serializer = self.serializer_class(blog)
        return Response({
            'status': True,
            'message': 'update Successful',
            'data': serializer.data
        })

    def delete(self, request, pk):
        self.model_class.objects.get(uid = pk).delete()
        return Response({
            'status': True,
            'message': 'Delete Successful',
            'data': []
        })

    @action(methods=["GET"],detail=False,url_path="get-blogs/",url_name="get-all")
    def get_all(self, request, *args, **kwargs):
        queryset = self.model_class.objects.all()  
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)      

class CommentMixin:
    serializer_class = CommentSerializer
    @action(methods=["POST"],detail=False,url_path="comment/(?P<blog_id>[^/.]+)",url_name="comment")
    def comment(self, request, *args, **kwargs):
        try:
            
            blog_id = kwargs.pop('blog_id')
            blog = self.model_class.objects.get(uid = blog_id)
            serializer = self.serializer_class(data={
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


class LikeMixin:
    serializer_class = LikeSerializer
    @action(methods=["GET"],detail=False,url_path="like/(?P<blog_id>[^/.]+)",url_name="like")
    def like(self, request, *args, **kwargs):
        try:
            blog_id = kwargs.pop('blog_id')
            blog = self.model_class.objects.get(uid = blog_id)
            serializer = self.serializer_class(data={
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