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