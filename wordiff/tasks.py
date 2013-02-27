from wordiff.models import ObjectGram, GramRankings
from wordiff.n_gram_splitter import lang_model
from django.conf import settings
from HTMLParser import HTMLParser

NGRAM_LENGTH = 8

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()


if hasattr(settings, "WORDIFF_NGRAM_LENGTH"):
	NGRAM_LENGTH = settings.WORDIFF_NGRAM_LENGTH

def gram_parse_object_text(object, object_text):
	""" 
	Parses out an object into its N-grams and saves them
	Can be included as a task, celery task, a post-save signal, 
	or part of the save method
	but may need to be modified accordingly
	"""
	
	parsed = lang_model(strip_tags(object_text))
	
	for gram in parsed.gram(NGRAM_LENGTH):
		object_gram = ObjectGram()
		object_gram.gram = gram
		object_gram.content_object = object
		object_gram.save()
		


def update_gram_rankings():
	object_grams = ObjectGram.objects.all()
	#ObjectGram.objects.distinct("content_type").all()
	
	GramRankings.objects.all().delete()
	
	for object_gram in object_grams:
		rankings = ObjectGram.objects.raw("\
		SELECT id, gram, COUNT(*) as quantity, MAX(date_created) as date_recent_match FROM wordiff_objectgram WHERE \
		content_type_id='%s'\
		GROUP BY gram ORDER BY quantity DESC LIMIT 20\
		" % object_gram.content_type_id)
		
		
	inserts = []
	
	for rank in rankings:
		if rank.quantity > 1:
			ranking = GramRankings()
			ranking.gram = rank.gram
			ranking.ranking = rank.quantity
			ranking.content_type = rank.content_type
			ranking.date_recent_match = rank.date_recent_match
			inserts.append(ranking)
	
	if inserts:
		GramRankings.objects.bulk_create(inserts)

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