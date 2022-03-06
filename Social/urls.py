from django.urls import path
from . import views
app_name='Social'
urlpatterns=[
	path('',views.indexview,name='index'),
	path('login/',views.loginview,name='login'),
	path('register/',views.registerview,name='register'),
	path('logout/',views.logoutview,name='logout'),
	path('profile/<pk>',views.profileview,name='profile'),
	path('photos/<pk>',views.profileposts,name='profileposts'),
	path('addcomment<pk>/',views.add_comment,name='add_comment'),
	path('addcommentspecific<pk>',views.add_comment_specific,name='add_comment_specific'),
	path('seemore<pk>/',views.seemore,name='seemore'),
	path('message<pk>/',views.message,name='message'),
	path('chat/<room_code>/',views.room,name='room'),
	path('post/',views.postimageview,name='postimage'),
	path('edit<pk>/',views.editprofileview,name='editprofile'),
	path('like/',views.likeview,name='like'),
	path('follow/',views.followview,name='follow'),
	path('saved/',views.savedview,name='saved'),
	path('savedimg<pk>/',views.savedimgview,name='savedimg'),
	path('savedlist<pk>/',views.savedimglistview,name='savedimglist'),
	path('story<pk>/',views.storyview,name='story'),
	path('addstory/',views.storyimageview,name='storyimage'),
	path('results/',views.autocomplete,name='searchresult'),
]