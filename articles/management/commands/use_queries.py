from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        command's hande method
        """        
        sample_attribute_name_value()

