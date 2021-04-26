from rest_framework import viewsets
from .serializers import CreateBlogSerializer
from .models import Blogs 
from .viewsets import CrudViewset, CommentViewset, LikeViewset, FeaturesViewset

class CreateBlogViewSet(viewsets.ViewSet, CrudViewset, CommentViewset, LikeViewset, FeaturesViewset):

    model_class  = Blogs
    serializer_class = CreateBlogSerializer
