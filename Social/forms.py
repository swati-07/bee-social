from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

class Register(UserCreationForm):
	
	class meta:
		model=User
		fields=['username','password1','password2','email','first_name','last_name']

