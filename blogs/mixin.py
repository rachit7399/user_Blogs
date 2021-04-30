from rest_framework import filters
from rest_framework.response import Response
from .models import  Blogs, Tags, Likes, Activity
from .serializers import TagsBlogSerializer
import logging
import operator
from django.http import HttpResponse
from datetime import datetime
import csv


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
        serializer = self.get_serializer(data={
            **{
                "comment": request.data["comment"],
                "user": blog.user.uid,
                "blog" : blog.uid
            }
        })   
        serializer.is_valid(raise_exception=True)   
        serializer.save()   
        logging.info("commented on blog with uid = '%s'", str(blog.uid)) 
        msg = "comented : " + str(request.data["comment"])
        # msg = f"commented: {str(request.data['comment'])}"
        obj = Activity.objects.create(blog = blog, user = blog.user, msg = msg)  
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
            obj = Activity.objects.create(blog = blog, user = blog.user, msg = "Disliked")  
            logging.info("disliked on blog with uid = '%s'", str(blog.uid)) 
        else:
            serializer = self.get_serializer(data={
                **{
                    "user": blog.user.uid,
                    "blog" : blog.uid
                }
            })   
            serializer.is_valid(raise_exception=True)   
            serializer.save() 
            _data = serializer.data  
            obj = Activity.objects.create(blog = blog, user = blog.user, msg = "liked")  
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
            serializer_data = TagsBlogSerializer(tag_obj).data
            serializer_data["count"] = dct_with_tagsand_count_sorted[tag_obj]
            serializer_data["rank"] = rank
            _data.append(serializer_data)
            rank += 1
        return _data
    
    def csv_details(self, request, fname):
        s1 = request.query_params.get("s1", None)
        s2 = request.query_params.get("s2", None)
        if(s1 == None or s2 == None):
            qs = self.model_class.objects.all()
        else:
            qs = self.model_class.objects.filter(created_at__range=[s1, s2])

        response = HttpResponse(content_type='text/csv')
        file_name = fname + str(datetime.now()) + ".csv"
        response['Content-Disposition'] = 'attachment; filename= {}'.format(file_name)
        serializer = self.get_serializer(qs, many = True)
        header = self.get_serializer().Meta.fields   
        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        return response