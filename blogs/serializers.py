from rest_framework import serializers
from .models import *

class CreateBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blogs
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs


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
