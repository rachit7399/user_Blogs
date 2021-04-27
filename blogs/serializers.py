from rest_framework import serializers
from rest_framework.serializers import FileField
from .models import *
from authentication.serializers import UserLikedSerializer

class TagsBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['name']
        
    def validate(self, attrs):
        return attrs

class CreateBlogSerializer(serializers.ModelSerializer):
    tags = TagsBlogSerializer(read_only = True, many = True)
    
    class Meta:
        model = Blogs
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs

class ActivitySerializer(serializers.ModelSerializer):
    user = UserLikedSerializer()
    blog = CreateBlogSerializer()

    class Meta:
        model = Activity
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs

class UploadSerializer(serializers.ModelSerializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comments
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Likes
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs

class ALLLikeSerializer(serializers.ModelSerializer):
    user = UserLikedSerializer()
    
    class Meta:
        model = Likes
        fields = ['user']
        
    def validate(self, attrs):
        return attrs

class LeaderboardSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    tags = TagsBlogSerializer(read_only = True, many = True)
    class Meta:
        model = Blogs
        fields = "__all__"
        # fields = ["uid", "title", "media", "content", "user" ,"likes_count", "comments_count"]
        
    def get_likes_count(self, blog_obj):
        return blog_obj.like_blogs.all().count()

    def get_comments_count(self, blog_obj):
        return blog_obj.comment_blogs.all().count()

class CSVBlogSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    user_comments = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()

    class Meta:
        model = Blogs
        fields = ["created_at", "uid", "title", "content", "media", "tags", "likes_count", "user_liked", "comments_count", "user_comments"]
        
    def get_likes_count(self, blog_obj):
        return blog_obj.like_blogs.all().count()

    def get_comments_count(self, blog_obj):
        return blog_obj.comment_blogs.all().count()
    
    def get_user_comments(self, blog_obj):
        list_of_comment = []
        for comm_obj in blog_obj.comment_blogs.all():
            list_of_comment.append(comm_obj.user.first_name +" -> "+ comm_obj.comment)
        return ", ".join(list_of_comment)

    def get_user_liked(self, blog_obj):
        list_of_likes = []
        for like_obj in blog_obj.like_blogs.all():
            list_of_likes.append(like_obj.user.first_name +" "+ like_obj.user.last_name)
        return ", ".join(list_of_likes)

    def get_tags(self, blog_obj):
        list_of_tags = []
        for tag_obj in blog_obj.tags.all():
            list_of_tags.append(tag_obj.name)
        return ", ".join(list_of_tags)


class CSVLikeSerializer(CSVBlogSerializer):

    class Meta:
        fields = ["created_at", "uid", "title", "content", "media", "tags", "likes_count", "user_liked"]


class CSVCommentSerializer(CSVBlogSerializer):
    
    class Meta:
        fields = ["created_at", "uid", "title", "content", "media", "tags", "comments_count", "user_comments"]
