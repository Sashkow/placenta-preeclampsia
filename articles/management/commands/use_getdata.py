from django.core.management.base import BaseCommand, CommandError
from articles.getdata import *
from articles.models import Experiment

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        command's hande method
        """        
        get_all_sample_attribute_names()
