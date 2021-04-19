from rest_framework import filters
from rest_framework.response import Response
from .models import Tags, Likes



class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator
    def paginate_queryset(self, queryset):
        
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                   self.request, view=self)
    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)



class BaseFilterMixin:
    search_fields = ['title', 'content']
    filter_backends = (filters.SearchFilter, )
    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset



class LikeCommentMixin:

    def comment_function(self, request, msg, *args, **kwargs):
        blog_id = kwargs.pop('pk')
        blog = self.model_class.objects.get(uid = blog_id)
        serializer = self.serializer_class(data={
            **{
                "comment": request.data["comment"],
                "user": request.user.uid,
                "blog" : blog.uid
            }
        })   
        serializer.is_valid(raise_exception=True)   
        serializer.save()      
        return Response({
            'status': True,
            'message': msg,
            'data': serializer.data
        })

    def like_function(self, request, msg, *args, **kwargs):
        blog_id = kwargs.pop('pk')
        blog = self.model_class.objects.get(uid = blog_id)
        if(Likes.objects.filter(blog__uid = blog_id).exists()):
            Likes.objects.filter(blog__uid = blog_id).delete()
            msg = "Disliked Successfull"
            _data = []
        else:
            serializer = self.serializer_class(data={
                **{
                    "user": request.user.uid,
                    "blog" : blog.uid
                }
            })   
            serializer.is_valid(raise_exception=True)   
            serializer.save() 
            _data = serializer.data   
        return Response({
            'status': True,
            'message': msg,
            'data': _data
        })



class TagMixin():

    def get_tags_list(self, lst_with_tag_name):
        lst_with_tag_uid = []
        for i in lst_with_tag_name:
            lst_with_tag_uid.append(Tags.objects.get_or_create(name = i)[0].uid)
        return lst_with_tag_uid

    def search_tag(self, request, queryset):
        tag_search = request.query_params.get("tag_search", None)
        if(tag_search != None):
            queryset = queryset.filter(tags__name = tag_search)
        return queryset

    def add_tag(self, request, blog):
        tags_list = self.get_tags_list(request.data["tags"].split(','))
        for tag in tags_list:
            blog.tags.add(tag)
        blog.save()

