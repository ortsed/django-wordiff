from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ObjectGramManager(models.Manager):

	def most_recent_matches(content_type_id, offset=0, count=20):
	
		""" 
		Grabs the most recent groups of texts with common n-gram sets
		and returns a list of dicts containing the n-grams, and the sets of texts
		"""

		ngrams = GramRankings.objects.all().filter(content_type=content_type_id).order_by("-ranking", "-date_recent_match")[offset:count]
		
		model_class = ContentType.objects.get(id=content_type_id).model_class()
		
		trending_similarities = []
		
		for ngram in ngrams:
			common_texts = model_class.objects.filter(id__in=ObjectGram.objects.filter(gram=ngram.gram).values_list("object_id"))
			
			trending_similarities.append({ "ngram":ngram, "common_texts": common_texts })
		
		return trending_similarities

class ObjectGram(models.Model):

	objects = ObjectGramManager()
	
	content_type = models.ForeignKey(ContentType, null=False, blank=False)
	
	object_id = models.PositiveIntegerField(null=False, blank=False)
	
	content_object = generic.GenericForeignKey("content_type", "object_id")
	
	gram = models.CharField(max_length=1000, null=False, blank=False)

	date_created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self, *args, **kwargs):
		return self.gram
	

class GramRankings(models.Model):

	gram = models.CharField(max_length=1000, null=False, blank=False)
	
	ranking = models.PositiveIntegerField(null=False, blank=False)
	
	content_type = models.ForeignKey(ContentType, null=False, blank=False)
	
	date_recent_match = models.DateTimeField()
	
	date_created = models.DateTimeField(auto_now_add=True)
	
	date_modified = models.DateTimeField(auto_now=True)