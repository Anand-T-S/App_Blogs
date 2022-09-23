from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile-pics", null=True)
    bio = models.CharField(max_length=240, null=True)


class Blogs(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=230)
    image = models.ImageField(upload_to="posts-images", null=True)
    posted_date = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors")
    liked_by = models.ManyToManyField(User)

    def __str__(self):
        return self.title


class Comments(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)