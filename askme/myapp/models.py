from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    photo = models.ImageField(null=True,blank=True)

    def __str__(self):
        return "profile {}".format(self.user.username)

class Question(models.Model):

    slug = models.SlugField(max_length=120)
    author = models.ForeignKey(User , related_name='blog_posts' , on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body


class Comment(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    ques = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='ques_comment')
    likes = models.ManyToManyField(User , related_name='comment_likes',blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.ques.body , self.user.username)



class Replies(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_reply')
    comment = models.ForeignKey(Comment , on_delete=models.CASCADE,related_name='comment_reply')
    ques = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='ques_reply')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.comment.id,self.ques.body,self.user.username)