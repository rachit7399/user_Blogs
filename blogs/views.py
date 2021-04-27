from rest_framework import viewsets
from .serializers import CreateBlogSerializer, CSVBlogSerializer, ActivitySerializer, LeaderboardSerializer, CommentSerializer, LikeSerializer, ALLLikeSerializer, CSVLikeSerializer, CSVCommentSerializer
from .models import Blogs 
from .viewsets import CrudViewset, CommentViewset, LikeViewset

class CreateBlogViewSet(viewsets.ModelViewSet, CrudViewset, CommentViewset, LikeViewset):
    
    model_class  = Blogs
    queryset = Blogs.objects.all()

    serializer_action_classes = {
        'all_activity' : ActivitySerializer,
        'learderboard' : LeaderboardSerializer,
        'comment' : CommentSerializer,
        'get_all_comments' : CommentSerializer,
        'get_comment' : CommentSerializer,
        'update_comment' : CommentSerializer,
        'like': LikeSerializer,
        'get_all_likes' : ALLLikeSerializer,
        'get_csv_all': CSVBlogSerializer,
        'get_csv_like' : CSVLikeSerializer,
        'get_csv_comment' : CSVCommentSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, CreateBlogSerializer)

