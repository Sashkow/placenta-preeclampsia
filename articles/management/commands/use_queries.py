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
        
        sample_attribute_name_experiment_value()

        # for obj in Microarray.objects.all():
        #     if 'name' in obj.data:
        #         print(obj.data['name'])
        #     else:
        #         print(None)
        

