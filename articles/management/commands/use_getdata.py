from django.core.management.base import BaseCommand, CommandError
from articles.getdata import *
from articles.models import Experiment, Microarray

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        command's hande method
        """        
        acc = "E-GEOD-74341"
        exp_to_db(acc)

        # for obj in Microarray.objects.all():
        #     if 'name' in obj.data:
        #         print(obj.data['name'])
        #     else:
        #         print(None)
        

