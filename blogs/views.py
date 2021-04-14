# from django.db import models
# from rest_framework.decorators import action
from rest_framework import viewsets
# from rest_framework.response import Response
from .serializers import CreateBlogSerializer
from .models import Blogs 
from .utils import BaseFilterMixin, CrudMixin, CommentMixin, LikeMixin

class CreateBlogViewSet(viewsets.ViewSet, BaseFilterMixin, CrudMixin, CommentMixin, LikeMixin):

    model_class  = Blogs
    serializer_class = CreateBlogSerializer



            