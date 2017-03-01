from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *




class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        command's handle method
        """
        all_microarrays_to_tsv()

        # samples_by_diagnosis()


 