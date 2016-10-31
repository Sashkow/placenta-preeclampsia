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

        show_exps_of_good_platforms()

            
        # samples = total_samples()
        # for sample in samples:
        #     sample_attributes = SampleAttributes.objects.filter(sample=sample)
        #     csection = sample_attributes.filter(unificated_value__value='')


