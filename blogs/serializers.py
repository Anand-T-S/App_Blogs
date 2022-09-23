from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from blogs.models import Blogs, Comments


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]

        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class BlogSerializer(ModelSerializer):
    id = serializers.CharField(read_only=True)
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Blogs
        exclude = ("posted_date", "liked_by")

    def create(self, validated_data):
        user = self.context.get("user")
        return Blogs.objects.create(**validated_data, author=user)


class CommentSerializer(ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    blog = serializers.CharField(read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "blog", "comment", "user"]

    def create(self, validated_data):
        user = self.context.get("user")
        blog = self.context.get("blog")
        return Comments.objects.create(**validated_data, blog=blog, user=user)