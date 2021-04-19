from django.db.models.query import QuerySet
from blogs.models import Comments
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.contrib.sites.shortcuts import get_current_site
from .mixin import LikeCommentMixin, PaginationHandlerMixin, BaseFilterMixin, TagMixin
from .serializers import CommentSerializer, LikeSerializer, CreateBlogSerializer


class CrudViewset(PaginationHandlerMixin, BaseFilterMixin, TagMixin):
    pagination_class    = PageNumberPagination
    def list(self, request):
        queryset = self.search_tag(request, self.filter_queryset(self.model_class.objects.filter(user = request.user) ))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.model_class.objects.filter(user = request.user) )
        blog = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(blog)
        return Response(serializer.data)

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        serializer = self.serializer_class(data={
            **{
                "title": request.data["title"],
                "content": request.data["content"],
                "media":file_uploaded,
                "user": request.user.uid,
            }
        })
        serializer.is_valid(raise_exception=True)
        blog = serializer.save()
        self.add_tag(request, blog)
        _data = serializer.data
        absurl = get_current_site(request).domain
        _data["media"] = 'http://' + absurl + _data["media"]
        return Response({
            'status': True,
            'message': 'object creation Successful',
            'data': _data
        })  

    def update(self, request, pk):
        blog = self.model_class.objects.get(uid = pk)
        if(request.data.get("title", []) != []):
            blog.title = request.data.get("title")
        if(request.data.get("content", []) != []):
            blog.content = request.data.get("content")  
        if(request.data.get("tags", []) != []):
            blog.tags.through.objects.filter(blogs_id = pk).delete()
            self.add_tag(request, blog)

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

    @action(methods=["GET"],detail=False,url_path="get-blogs/all",url_name="get-all")
    def get_all(self, request, *args, **kwargs):
        queryset = self.model_class.objects.all()  
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)      



class CommentViewset(LikeCommentMixin):
    @action(methods=["POST"], detail=True)
    def comment(self, request, *args, **kwargs):
        try:
            self.serializer_class = CommentSerializer
            return self.comment_function(request, "Comment Successful", *args, **kwargs)
        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)
    
    @action(methods=["GET"], detail=True)
    def get_comments(self, request, *args, **kwargs):
        try:
            self.serializer_class = CommentSerializer
            self.model_class = Comments
            QuerySet = self.model_class.objects.filter(blog__uid = kwargs["pk"])
            _data = []
            for comment_obj in QuerySet:
                _data.append(self.serializer_class(comment_obj).data)

            return Response({
                'status': True,
                'message': 'All Comments',
                'data': _data
            })

            
        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)

    @action(methods=["DELETE"], detail=True)
    def delete_comment(self, request, *args, **kwargs):
        try:
            self.serializer_class = CommentSerializer
            self.model_class = Comments
            self.model_class.objects.filter(uid = kwargs["pk"]).delete()
            return Response({
                'status': True,
                'message': 'Delete Successfull',
                'data': []
            })

        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)


class LikeViewset(LikeCommentMixin):
    @action(methods=["GET"], detail=True)
    def like(self, request, *args, **kwargs):
        try:
            self.serializer_class = LikeSerializer
            return self.like_function(request, "liked Successful", *args, **kwargs)
        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)



