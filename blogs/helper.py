from .models import Tags
from .serializers import CommentSerializer, LikeSerializer
from rest_framework.response import Response

def search_tag(request, queryset):
    tag_search = request.query_params.get("tag_search", None)
    if(tag_search != None):
        queryset = queryset.filter(tags__name = tag_search)
    return queryset


def add_tag(request, blog):
    tags_list = get_tags_list(request.data["tags"].split(','))
    for tag in tags_list:
        blog.tags.add(tag)
    blog.save()

def get_tags_list(lst_with_tag_name):
    lst_with_tag_uid = []
    for i in lst_with_tag_name:
        lst_with_tag_uid.append(Tags.objects.get_or_create(name = i)[0].uid)
    return lst_with_tag_uid

def like_comment_function(self, request, msg, *args, **kwargs):
    blog_id = kwargs.pop('blog_id')
    blog = self.model_class.objects.get(uid = blog_id)
    serializer = LikeSerializer(data={
        **{
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