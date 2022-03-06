from django_elasticsearch_dsl import Document,Index

from django.contrib.auth.models import User

user=Index('user')
@user.doc_type
class User_document(Document):
	class Django:
		model=User
		fields=['username','first_name','last_name']





