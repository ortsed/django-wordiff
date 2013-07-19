from django.db import models
from lawdiff.models import Bill_File

class ObjectGramManager(models.Manager):
	pass
	
class ObjectGram(models.Model):

	objects = ObjectGramManager()
	
	state = models.CharField(max_length=10, null=False, blank=False)
	
	object = models.ForeignKey(Bill_File, null=False, blank=False)
	
	gram = models.CharField(max_length=1000, null=False, blank=False)
	
	rank = models.PositiveIntegerField(null=False, blank=False)

	date_created = models.DateTimeField(auto_now_add=True)
	
	@property
	def similar_objects(self):
		qs = ObjectGram.objects.filter(gram=self.gram).order_by("object")
		qs.group_by = ['object']
		return qs
		
	def __unicode__(self, *args, **kwargs):
		return self.gram
	

class GramRankings(models.Model):

	gram = models.CharField(max_length=1000, null=False, blank=False)
	
	rank = models.PositiveIntegerField(null=False, blank=False)
	
class GramUnique(models.Model):

	gram = models.CharField(max_length=1000, null=False, blank=False)
	
	state = models.CharField(max_length=10, null=False, blank=False)
	
class IgnoredGram(models.Model):
    gram = models.CharField(max_length=255L, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
