from rest_framework import filters
from rest_framework.response import Response
from .models import  Blogs, Tags, Likes, Activity
import logging
import operator


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
        logging.info("commented on blog with uid = '%s'", str(blog.uid)) 
        msg = "comented : " + str(request.data["comment"])
        obj = Activity.objects.create(blog = blog, user = request.user, msg = msg)  
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
            obj = Activity.objects.create(blog = blog, user = request.user, msg = "Disliked")  
            logging.info("disliked on blog with uid = '%s'", str(blog.uid)) 
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
            obj = Activity.objects.create(blog = blog, user = request.user, msg = "liked")  
            logging.info("liked on blog with uid = '%s'", str(blog.uid))  
        return Response({
            'status': True,
            'message': msg,
            'data': _data
        })



class TagMixin:

    def get_tags_list(self, lst_with_tag_name):
        lst_with_tag_uid = []
        for i in lst_with_tag_name:
            if(i != ""):
                lst_with_tag_uid.append(Tags.objects.get_or_create(name = i.lower())[0].uid)
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


class GenMixin:
    def get_dct_with_tagsand_count(self):
        dct = {}
        qs = Tags.objects.all()
        for i in qs:
            dct[i] = Blogs.objects.filter(tags__name = i.name).count()
        return dct

    def sort_for_leaderboard_tags(self):
        dct_with_tagsand_count = self.get_dct_with_tagsand_count()
        dct_with_tagsand_count_sorted = dict( sorted(dct_with_tagsand_count.items(), key=operator.itemgetter(1),reverse=True))
        _data = []
        rank = 1
        for tag_obj in dct_with_tagsand_count_sorted:
            serializer_data = self.serializer_class(tag_obj).data
            serializer_data["count"] = dct_with_tagsand_count_sorted[tag_obj]
            serializer_data["rank"] = rank
            _data.append(serializer_data)
            rank += 1
        return _data