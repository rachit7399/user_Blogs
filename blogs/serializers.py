from rest_framework import serializers
from .models import Blogs

class CreateBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blogs
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs