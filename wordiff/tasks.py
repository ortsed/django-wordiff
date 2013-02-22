from wordiff.models import ObjectGram
from wordiff.n_gram_splitter import lang_model
from django.conf import settings

NGRAM_LENGTH = 8

if hasattr(settings, "WORDIFF_NGRAM_LENGTH"):
	NGRAM_LENGTH = settings.WORDIFF_NGRAM_LENGTH

def gram_parse_object_text(object, object_text):
	""" 
	Parses out an object into its N-grams and saves them
	Can be included as a task, celery task, a post-save signal, or part of the save method
	but may need to be modified accordingly
	"""
	
	parsed = lang_model(object_text)
	
	for gram in parsed.gram(NGRAM_LENGTH):
		object_gram = ObjectGram()
		object_gram.gram = gram
		object_gram.content_object = object
		object_gram.save()
		


""" 

--- SAMPLE post_save signal function ---


from django.db.models.signals import post_save
from django.dispatch import receiver
from wordiff.tasks import gram_parse_object_text

from blog.models import Post

@receiver(post_save, sender=Post)
def post_save_gram_parse(sender, instance, created, **kwargs):
    if created:
    	gram_parse_object_text(instance, instance.content)


"""