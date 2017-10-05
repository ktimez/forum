from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Reply.objects.filter(topic__category=self).count()
    def get_last_post(self):
        return Reply.objects.filter(topic__category=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')
    views = models.PositiveIntegerField(default=0)
    #last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Reply(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return self.truncated_message.chars(30)

