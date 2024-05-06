
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    image = models.ImageField(upload_to='blog/', default='blog/default.jpg')
    tags = TaggableManager(blank=True)
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=255)
    content = models.TextField()
    counted_view = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return "{}- {}".format(self.title, self.id)

    def get_absolute_url(self):
        return reverse("blog:single", kwargs={'pid': self.id})


class Likes(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_likes")
