from django.shortcuts import render
from blogs.serializers import UserSerializer, BlogSerializer, CommentSerializer
from blogs.models import Blogs, Comments
from rest_framework import status, permissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.


class UserViewSetView(ViewSet):
    """User Creation/Signup"""

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogViewSetView(ViewSet):
    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data, context={"user": request.user})
        if not serializer.is_valid():
            return Response(serializer.errors)
        else:
            serializer.save()
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        blog_id = kwargs.get("pk")
        blog = Blogs.objects.get(id=blog_id, author=self.request.user)
        serializer = BlogSerializer(instance=blog, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        else:
            serializer.save()
            return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        qs = Blogs.objects.filter(author=self.request.user)
        serializer = BlogSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        blog_id = kwargs.get("pk")
        blog = Blogs.objects.get(id=blog_id, author=self.request.user)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        blog_id = kwargs.get("pk")
        blog = Blogs.objects.get(id=blog_id, author=self.request.user)
        blog.delete()
        return Response({"msg": "successfully deleted"})


class PublicBlogViewSetView(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        p_blogs = Blogs.objects.all()
        serializer = BlogSerializer(p_blogs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        p_blog_id = kwargs.get("pk")
        p_blog = Blogs.objects.get(id=p_blog_id)
        serializer = BlogSerializer(p_blog)
        return Response(serializer.data)

    """Add like to blog"""
    @action(methods=['GET'], detail=True)
    def add_like(self, request, *args, **kwargs):
        p_blog_id = kwargs.get("pk")
        p_blog = Blogs.objects.get(id=p_blog_id)
        p_blog.liked_by.add(request.user)
        total_likes = p_blog.liked_by.all().count()
        return Response({"like_count": total_likes})

    @action(methods=['GET'], detail=True)
    def get_likes(self, request, *args, **kwargs):
        p_blog_id = kwargs.get("pk")
        p_blog = Blogs.objects.get(id=p_blog_id)
        print(p_blog)
        data = p_blog.liked_by.all()
        print(data)
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)


class CommentViewSetView(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    """Post my comment"""
    def create(self, request, *args, **kwargs):
        blog_id = kwargs.get("pk1", None)
        blog = Blogs.objects.get(id=blog_id)
        serializer = CommentSerializer(data=request.data, context={"blog": blog, "user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    """List all comments"""
    def list(self, request, *args, **kwargs):
        blog_id = kwargs.get("pk1", None)
        print(blog_id)
        comments = Comments.objects.filter(blog=blog_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    """Detail all comments"""
    def retrieve(self, request, *args, **kwargs):
        com_id = kwargs.get("pk")
        print(com_id)
        comment = Comments.objects.get(id=com_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    """Edit my comment"""
    def update(self, request, *args, **kwargs):
        com_id = kwargs.get("pk")
        print(com_id)
        comment = Comments.objects.get(id=com_id, user=self.request.user)
        serializer = CommentSerializer(instance=comment, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        else:
            serializer.save()
            return Response(serializer.data)

    """Delete my comment"""
    def destroy(self, request, *args, **kwargs):
        com_id = kwargs.get("pk")
        comment = Comments.objects.get(id=com_id, user=self.request.user)
        comment.delete()
        return Response({"msg": "successfully deleted"})