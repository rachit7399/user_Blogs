from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class ReadProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['uid', 'email']
        
    def validate(self, attrs):
        return attrs

class ChangePassSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'confirm_pass']

class ForgetPassSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']
    def validate(self, attrs):
        return attrs

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        return attrs   

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)


    def validate_password(self, value):
        return make_password(value)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        return attrs 

class UserLikedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['uid', 'first_name', 'last_name']

    def validate(self, attrs):
        return attrs       
