from django.db import models
from django.contrib.auth.models import User

class UserContacts(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,primary_key=False)
	mobile = models.CharField(max_length=15 ,blank=True, null=True)
	name = models.CharField(max_length=100 ,blank=True, null=True)
	registered = models.CharField(max_length=3 ,blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'user_contacts'
		indexes = [
            models.Index(fields=['mobile',])
		]

class Spam(models.Model):
	mobile = models.CharField(max_length=15 ,blank=True, null=True)
	count = models.IntegerField(default=1)

	class Meta:
		db_table = 'spam_table'
		indexes = [
            models.Index(fields=['mobile',])
		]
