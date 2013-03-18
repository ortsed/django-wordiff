from django.core.management.base import BaseCommand
from wordiff.tasks import update_gram_rankings

class Command(BaseCommand):
    help = 'Update n-gram rankings'
    def handle(self, *args, **options):
        update_gram_rankings()
        self.stdout.write("Done.\n")
