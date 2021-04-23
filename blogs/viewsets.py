from rest_framework.exceptions import ValidationError
from blogs.models import Comments, Likes
from .models import Activity
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from django.contrib.sites.shortcuts import get_current_site
from .mixin import LikeCommentMixin, PaginationHandlerMixin, BaseFilterMixin, TagMixin, GenMixin
from .serializers import CommentSerializer, LikeSerializer, ActivitySerializer, ALLLikeSerializer, TagsBlogSerializer, LeaderboardSerializer
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("mylogs.log"),
        logging.StreamHandler()
    ]
    )


class CrudViewset(PaginationHandlerMixin, BaseFilterMixin, TagMixin, GenMixin):
    pagination_class    = PageNumberPagination  
    def list(self, request):
        queryset = self.search_tag(request, self.filter_queryset(self.model_class.objects.filter(user = request.user) ))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(queryset, many=True)
        logging.info("list of blogs for the user '%s'", str(request.user.uid))
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.model_class.objects.filter(user = request.user) )
        blog = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(blog)
        logging.info("blog details of '%s'", str(blog.uid))
        obj = Activity.objects.create(blog = blog, user = request.user, msg = "retrieved blog data")
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
        logging.info("blog created with uid '%s'", str(blog.uid))
        obj = Activity.objects.create(blog = blog, user = request.user, msg = "Blog Created")
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
        if(request.FILES.get('file_uploaded') != None):
            blog.media = request.FILES.get('file_uploaded')
            
        blog.save()
        serializer = self.serializer_class(blog)
        logging.info("blog updated with uid '%s'", str(blog.uid))
        obj = Activity.objects.create(blog = blog, user = request.user, msg = "Blog updated")
        return Response({
            'status': True,
            'message': 'update Successful',
            'data': serializer.data
        })

    def delete(self, request, pk):
        blog = self.model_class.objects.get(uid = pk)
        obj = Activity.objects.create(blog = blog, user = request.user, msg = "Blog deleted")
        blog.delete()
        logging.info("blog deleted with uid '%s'", str(pk))
        return Response({
            'status': True,
            'message': 'Delete Successful',
            'data': []
        })

    @action(methods=["GET"],
            detail=False,
            url_path="tags/(?P<tag>[^/.]+)",
            url_name="tags_search")
    def tags_search(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.model_class.objects.filter(user = request.user))
        queryset = queryset.filter(tags__name = kwargs['tag'])
        serializer = self.serializer_class(queryset, many=True)
        logging.info("Tag search with tag '%s'", str(kwargs.pop('tag')))
        return Response(serializer.data)


    @action(methods=["GET"],detail=False,url_path="get-blogs/all",url_name="get-all")
    def get_all(self, request, *args, **kwargs):
        queryset = self.model_class.objects.all()  
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(queryset, many=True)
        logging.info("all blogs available")
        return Response(serializer.data) 

    @action(methods=["GET"], detail=True)
    def all_activity(self, request, *args, **kwargs):
        try:
            self.serializer_class = ActivitySerializer
            self.model_class = Activity
            querySet = self.model_class.objects.filter(user__uid = kwargs.pop('pk'))
            serializer = self.serializer_class(querySet, many=True)
            return Response({
                'status': True,
                'message': 'All Activity',
                'data': serializer.data
            })
        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"],detail=False,url_path="learderboard/all",url_name="learderboard")
    def learderboard(self, request, *args, **kwargs):
        try:
            sort = request.query_params.get("sort", "likes")
            s1 = request.query_params.get("s1", None)
            s2 = request.query_params.get("s2", None)
            _data = []

            if(sort == "tags"):
                self.serializer_class = TagsBlogSerializer
                _data = self.sort_for_leaderboard_tags()

            else:
                if(s1 == None or s2 == None):
                    qs = self.model_class.objects.all()
                else:
                    qs = self.model_class.objects.filter(created_at__range=[s1, s2])
                _data = LeaderboardSerializer(qs, many = True).data
                if(sort == "likes"):
                    _data = sorted(_data, key = lambda i: i['likes_count'],reverse=True)
                elif(sort == "comments"):
                    _data = sorted(_data, key = lambda i: i['comments_count'],reverse=True)
                else:
                    _data = "Wrong sorting filter"
                
            
            return Response({
                'status': True,
                'message': 'learderboard',
                'data': _data
            })
            
        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)




class CommentViewset(LikeCommentMixin):
    @action(methods=["POST"], detail=True)
    def comment(self, request, *args, **kwargs):
        try:
            self.serializer_class = CommentSerializer
            return self.comment_function(request, "Comment Successful", *args, **kwargs)
        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)
    
    @action(methods=["GET"], detail=True)
    def get_all_comments(self, request, *args, **kwargs):
        try:
            self.serializer_class = CommentSerializer
            self.model_class = Comments
            querySet = self.model_class.objects.filter(blog__uid = kwargs["pk"])
            serializer = self.serializer_class(querySet, many = True)
            logging.info("all comments of blog with uid = '%s'", str(kwargs["pk"])) 
            return Response({
                'status': True,
                'message': 'All Comments',
                'data': serializer.data
            })

        except Exception:
            raise ValidationError({
                'status': False,
                'message': 'Failed',
                'data': []
            })

    @action(methods=["GET"], detail=True)
    def get_comment(self, request, *args, **kwargs):
        try:
            self.serializer_class = CommentSerializer
            self.model_class = Comments
            comment_obj = self.model_class.objects.get(uid = kwargs["pk"])
            _data = self.serializer_class(comment_obj).data
            logging.info("comment with uid = '%s'", str(kwargs["pk"])) 
            return Response({
                'status': True,
                'message': 'Successfull',
                'data': _data
            })

        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=True)
    def update_comment(self, request, *args, **kwargs):
        try:
            self.serializer_class = CommentSerializer
            self.model_class = Comments
            comment_obj = self.model_class.objects.get(uid = kwargs["pk"])
            comment_obj.comment = request.data["comment"]
            comment_obj.save()
            _data = self.serializer_class(comment_obj).data
            logging.info("updated comment with uid = '%s'", str(kwargs["pk"])) 
            return Response({
                'status': True,
                'message': 'updated Successfully',
                'data': _data
            })

        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)

    @action(methods=["DELETE"], detail=True)
    def delete_comment(self, request, *args, **kwargs):
        try:
            self.serializer_class = CommentSerializer
            self.model_class = Comments
            self.model_class.objects.get(uid = kwargs["pk"]).delete()
            logging.info("deleted comments of uid = '%s'", str(kwargs["pk"])) 
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


    @action(methods=["GET"], detail=True)
    def get_all_likes(self, request, *args, **kwargs):
        try:
            self.serializer_class = ALLLikeSerializer
            queryset = Likes.objects.filter(blog__uid = kwargs["pk"])
            serializers = self.serializer_class(queryset, many = True)                
            logging.info("all likes of blog with uid = '%s'", str(kwargs["pk"])) 
            return Response({
                'likes_count': queryset.count(),
                'status': True,
                'message': 'All likes',
                'data': serializers.data
            })

            
        except Exception:
            return Response({"Failed"}, status.HTTP_400_BAD_REQUEST)


