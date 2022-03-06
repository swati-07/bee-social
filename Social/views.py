from django.shortcuts import render ,redirect
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .forms import Register
from .models import Profile,Post,Comment,Chatroom,Saved,Story
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .documents import User_document
import os
import json



def autocomplete(request):
    if request.is_ajax():
        username_query = request.GET.get('username_query', '')
        usernames = (User.objects
                     .filter(username__startswith=username_query)
                     .values_list('username', flat=True))
        data = {
            'usernames': list(usernames),
        }
        
        return JsonResponse(data,safe=False)




		
def searchview(request):
	if request.method=='POST':
		searchq=request.POST.get('username')
		try:
			searchq=Profile.objects.get(user__username=searchq)
		except:
			searchq=Profile.objects.get(user__firstname=searchq)

	
# Create your views here.
@login_required
def indexview(request):
	posts=Post.objects.all().order_by('-time')	
	user=request.user
	profile=Profile.objects.get(user__username=user)
	comments=Comment.objects.all().order_by('-time')
	savedobj,created=Saved.objects.get_or_create(user=user)
	stories=Story.objects.all()
	mystory=profile.getStory()
	return render(request,'index.html',{'show':"no",'posts':posts,
		'comments':comments,'profile':profile,'filter':0,"savedobj":savedobj,'stories':stories,'mystory':mystory})
	

def registerview(request):
	if request.user.is_authenticated:
		return redirect('/social')
	else:
		form=Register()
		if request.method=='POST':
			form=Register(request.POST)
			if form.is_valid():
				form.save()
				username=request.POST.get('username')
				profile=Profile()
				profile.user=User.objects.get(username=username)
				profile.save()
				return redirect('Social:login')
		return render(request,'signin.html',{'form':form})

def loginview(request):
	if request.user.is_authenticated:
		return redirect('/social')
	else:
		if request.method=='POST':
			username=request.POST.get('username')
			password=request.POST.get('password')
			user=authenticate(request,username=username,password=password)
			if user is not None:
				login(request,user)
				return redirect('/social')
			else:
				return redirect('Social:login')
			
		return render(request,'login.html',{})

def logoutview(request):
	logout(request)
	return redirect('Social:login')

def storyview(request,pk):
	story=Story.objects.get(pk=pk)
	story.openedby.add(request.user)
	story.save()
	return render(request,'story.html',{'story':story})

def storyimageview(request):
	profile=Profile.objects.get(user__username=request.user)
	if request.method=='POST' and ('story1' in request.FILES or 'story2' in request.FILES or 'story3' in request.FILES) :
		story_obj,created=Story.objects.get_or_create(profile=profile)
		
		if 'story1' in request.FILES:
			story1=request.FILES['story1']
			story_obj.story1=story1
		if 'story2' in request.FILES:
			story2=request.FILES['story2']
			story_obj.story2=story2
		if 'story3' in request.FILES:
			story3=request.FILES['story3']
			story_obj.story3=story3
		story_obj.save()
	return redirect('/social')

def profileview(request,pk):
	profile=Profile.objects.get(pk=pk)
	postcount=profile.countPosts()
	posts=profile.getPosts()
	profile2=Profile.objects.get(user=request.user)
	# followersNum=profile.countFollowers()

	
	# followingNum=followingobj.countFollowing()
	return render(request,'profile.html',{'profile':profile,'profile2':profile2,'postcount':postcount,'posts':posts})

def profileposts(request,pk):
	profile=Profile.objects.get(pk=pk)
	postcount=profile.countPosts()
	posts=profile.getPosts()
	profile2=Profile.objects.get(user=request.user)
	# followersNum=profile.countFollowers()

	
	return render(request,'profileposts.html',{'profile':profile,'profile2':profile2,'postcount':postcount,'posts':posts})

def postimageview(request):
	
	profile=Profile.objects.get(user__username=request.user)
	if request.method=='POST' and 'photo' in request.FILES :
		caption=request.POST['caption']
		print(caption)
		filternum=request.POST['filternum']
		image=request.FILES['photo']
		post_obj=Post(caption=caption,image=image,profile=profile,time=datetime.now(),filterNum=filternum)
		post_obj.save()
	return redirect('/social')

def editprofileview(request,pk):
	profile=Profile.objects.get(pk=pk)
	if request.method=='POST':
		username=request.POST['username']
		print(username)
		bio=request.POST['bio']
		profile.user.username=username
		profile.bio=bio
		if 'photo' in request.FILES:
			image_path=profile.pimage.path
			if os.path.exists(image_path):
				os.remove(image_path)
				profile.pimage=request.FILES['photo']
		profile.save()
		profile.user.save()
	return redirect('Social:profile',pk=pk)


def likeview(request):
	if request.method=="GET":
		user=request.user
		pk=request.GET['postpk']
		
		post=Post.objects.get(pk=int(pk))
		if post.pLiked.filter(username=user.username).exists():
		 	post.pLiked.remove(user)
		 	post.likes=post.likes-1
		 	post.save()
		else:
		 	post.pLiked.add(user)
		 	post.likes=post.likes+1
		 	post.save()

	ctx={'likes':post.likes}
	print(post.likes)
	return JsonResponse(ctx,safe=False) 
def savedview(request):
	if request.method=='POST':
		pk=request.POST.get('pk')
		post=Post.objects.get(pk=pk)
		savedobj,created=Saved.objects.get_or_create(user=request.user)
		if savedobj.savedpost.filter(pk=pk).exists():
			savedobj.savedpost.remove(post)
			savedobj.save()
			saved=False
		else:
			savedobj.savedpost.add(post)
			savedobj.save()
			saved=True
	ctx={'saved':saved}
	return JsonResponse(ctx,safe=False)

def savedimgview(request,pk):
	
	profile=Profile.objects.get(pk=pk)
	user=profile.user
	saved_obj,created=Saved.objects.get_or_create(user=user)
	print(saved_obj)
	return render(request,'savedimg.html',{'saved_obj':saved_obj,'profile':profile})

def savedimglistview(request,pk):
	
	profile=Profile.objects.get(pk=pk)
	user=profile.user
	saved_obj,created=Saved.objects.get_or_create(user=user)
	print(saved_obj)
	return render(request,'savedimglist.html',{'saved_obj':saved_obj,'profile':profile})

def followview(request):
	if request.method=='GET':
		user=request.user
		profile2=Profile.objects.get(user=user)
		
		pk=request.GET['profilepk']
		profile=Profile.objects.get(pk=pk)
		
		if profile.followers.filter(user=user).exists():
			profile.followers.remove(profile2)
			profile2.following.remove(profile)
			profile2.save()
			profile.save()
			
			

		else:
			profile.followers.add(profile2)
			profile.save()
			profile2.following.add(profile)
			profile2.save()
	
	ctx={'followers':"yes"}
	
	return JsonResponse(ctx,safe=False)




def add_comment(request,pk):
	post=Post.objects.get(pk=pk)
	
	if request.method=='POST':
		
		comment=request.POST['comment']
		print(comment)
		user=request.user
		comment_obj=Comment(user=request.user,comment=comment,post=post)
		comment_obj.save()
		post.comments.add(comment_obj)

	return redirect('/social'+'#'+str(post.pk))

def add_comment_specific(request,pk):
	post=Post.objects.get(pk=pk)
	
	if request.method=='POST':
		
		comment=request.POST['comment']
		print(comment)
		user=request.user
		comment_obj=Comment(user=request.user,comment=comment,post=post)
		comment_obj.save()
		post.comments.add(comment_obj)
	return render(request,'comments.html',{'post':post})
	
	
def seemore(request,pk):
	post=Post.objects.get(pk=pk)
	return render(request,'comments.html',{'post':post})

def message(request,pk):
	user_me=request.user
	another_user=Profile.objects.get(pk=pk).user.username
	if str(user_me)<str(another_user):
		room_code=str(user_me)+another_user
	else:
		room_code=another_user+str(user_me)
	
	chatroomobj=Chatroom.objects.filter(room_code=room_code)
	if chatroomobj is None:
		chatroomobj=Chatroom(room_code=room_code)
		chatroomobj.save()
	return redirect('/social/chat/'+room_code)

def room(request,room_code):
	show="yes"
	posts=Post.objects.all().order_by('-time')	
	user=request.user
	profile=Profile.objects.get(user__username=user)
	comments=Comment.objects.all().order_by('-time')
	return render(request,'index.html',{'show':show,'room_code':room_code,'posts':posts,'comments':comments,'profile':profile})