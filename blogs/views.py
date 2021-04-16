from rest_framework import viewsets
from .serializers import CreateBlogSerializer
from .models import Blogs 
from .utils import BaseFilterMixin, CrudMixin, CommentMixin, LikeMixin

class CreateBlogViewSet(viewsets.ViewSet, BaseFilterMixin, CrudMixin, CommentMixin, LikeMixin):

    model_class  = Blogs
    serializer_class = CreateBlogSerializer
