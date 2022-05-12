from rest_framework import serializers

from django.contrib.auth import get_user_model

from users.models import UserDocs
User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocs
        # fields = "__all__"
        exclude = ('user', )

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "father_name")


class UserDataSerializer(serializers.ModelSerializer):
    document = UserDocsSerializer(required=False, many=False)
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ('groups', 'user_permissions')

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
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    document = UserDocsSerializer(required=False, many=False)
    class Meta:
        model = User
        fields = "__all__"