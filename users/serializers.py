from rest_framework import serializers

from django.contrib.auth import get_user_model

from users.file_read import names
from users.models import UserDocs
User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocs
        exclude = ('user', )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "first_name", "last_name", "father_name", "school", "klass")

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions')

        extra_kwargs = {
            'password':{'required':False}
        }
    def create(self, attrs):
        user = User(**attrs)
        user.set_password(attrs.get('password', '1'))
        user.save()
        return user


    def update(self, instance, attrs):
        keys = attrs.keys()
        if 'password' in keys:
            instance.set_password(attrs['password'])
        if 'first_name' in keys:
            instance.first_name = attrs.get('first_name', instance.first_name)
        if 'last_name' in keys:
            instance.last_name = attrs.get('last_name', instance.last_name)
        if 'father_name' in keys:
            instance.father_name = attrs.get('father_name', instance.father_name) 
        if 'school' in keys:
            instance.school = attrs.get('school', instance.school)
        if 'klass' in keys:
            instance.klass = attrs.get('klass', instance.klass)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    # document = UserDocsSerializer(required=False, many=False)
    class Meta:
        model = User
        fields = "__all__"