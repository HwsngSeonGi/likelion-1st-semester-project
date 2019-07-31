from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, editable =False, null=True, blank=True, on_delete=models.SET_NULL,)
    title=models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_user_set', through='Like')

    @property
    def like_count(self):
       return self.like_user_set.count()

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]

class Like(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   blog = models.ForeignKey(Post, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   class Meta:
      unique_together = (('user', 'blog'))

class Comment(models.Model):
    post_key = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_contents = models.CharField(max_length=200)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.comment_contents
        