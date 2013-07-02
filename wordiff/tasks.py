from wordiff.models import ObjectGram, IgnoredGram, GramRankings
from wordiff.n_gram_splitter import lang_model
from django.conf import settings
from HTMLParser import HTMLParser
from django.db import connection
from datetime.datetime import today

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
	cursor = connection.cursor()
	cursor.execute("DELETE FROM wordiff_objectgramrank;\
	INSERT INTO \
			wordiff_objectgramrank\
			(`gram`, `rank`)\
		\
			SELECT gram, count(id) FROM wordiff_objectgram\
			GROUP BY gram;\
		UPDATE wordiff_objectgram\
		LEFT JOIN wordiff_objectgramrank\
		ON wordiff_objectgram.gram = wordiff_objectgramrank.gram\
		SET wordiff_objectgram.rank = wordiff_objectgramrank.rank\
		")
		
def remove_ignored_grams():
	ignored_grams = IgnoredGram.objects.all()
	for gram in ignored_grams:
		ObjectGram.objects.filter(gram=gram).delete()
	
	
def add_common_grams_to_ignored():
	common_grams = ObjectGram.objects.filter(rank__gt=25)
	for gram in common_grams:
		ignored_gram = IgnoredGram()
		ignored_gram.gram = gram.gram
		ignored_gram.date_published = today()
		ignored_gram.save()
		gram.delete()
	
#	cursor = connection.cursor()
#	cursor.execute("INSERT INTO wordiff_ignoredgram (`gram`, `date_created`) SELECT gram, NOW() FROM wordiff_objectgram WHERE rank > 25")



