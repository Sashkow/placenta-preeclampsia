from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

def is_unified(obj):
        exp_samples = obj.samples()
        has_empty_name = SampleAttribute.objects.filter(
          sample__in=exp_samples,
          unificated_name=None).exists()

        has_empty_value = SampleAttribute.objects.filter(
          sample__in=exp_samples,
          unificated_value=None).exists()
        if has_empty_name or has_empty_value:
            return False
        else:
            return True

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        command's hande method
        """        

            


        exps = Experiment.objects.all()
        for exp in exps:
            if is_unified(exp):
                print(exp.data['accession'])

