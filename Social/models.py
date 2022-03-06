from django.db import models
from django.contrib.auth.models import User


from datetime import datetime,timedelta

# Create your models here.
class Profile(models.Model):

	pimage=models.ImageField(blank=True,null=True,default='user.png',upload_to='images/')
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	bio=models.CharField(max_length=200)
	followers=models.ManyToManyField('self',null=True,blank=True,related_name='f1',symmetrical=False)
	following=models.ManyToManyField('self',null=True,blank=True,related_name='f2',symmetrical=False)

	def countPosts(self):
		posts=Post.objects.filter(profile__pk=self.pk)
		return len(posts)
	def getPosts(self):
		posts=Post.objects.filter(profile__pk=self.pk)
		return posts
	def getStory(self):
		mystory,created=Story.objects.get_or_create(profile=self)
		
		return mystory
		
class Story(models.Model):
	profile=models.OneToOneField(Profile,on_delete=models.CASCADE)
	story1=models.ImageField(blank=True,null=True,upload_to='stories/')
	story2=models.ImageField(blank=True,null=True,upload_to='stories/')
	story3=models.ImageField(blank=True,null=True,upload_to='stories/')
	opened=models.BooleanField(default=False,null=True,blank=True)
	openedby=models.ManyToManyField(User)
	start=models.DateTimeField(null=True,blank=True)
	end=models.DateTimeField(null=True,blank=True)
	start2=models.DateTimeField(null=True,blank=True)
	end2=models.DateTimeField(null=True,blank=True)
	start3=models.DateTimeField(null=True,blank=True)
	end3=models.DateTimeField(null=True,blank=True)

class Post(models.Model):
	caption=models.CharField(max_length=2000)
	image=models.ImageField(blank=True,upload_to='images/')
	time=models.DateTimeField()
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
	comments=models.ManyToManyField('Comment',blank=True)
	filterNum=models.IntegerField(blank=True,null=True)
	likes=models.IntegerField(blank=True,null=True,default=0)
	pLiked=models.ManyToManyField(User,null=True,blank=True)

class Saved(models.Model):
	user=models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)
	savedpost=models.ManyToManyField(Post,blank=True,null=True)


class Comment(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE, blank=True,null=True)
	
	comment=models.CharField(max_length=100)
	time=models.DateTimeField(auto_now_add=True)


class Chatroom(models.Model):
	room_code=models.CharField(max_length=100)

	def __str__(self):
		return f'{self.room_code}'

class Jokes(models.Model):
	jokes=models.CharField(max_length=20)