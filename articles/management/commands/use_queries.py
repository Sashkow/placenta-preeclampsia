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
        exp_id = "E-GEOD-74341"
        
        
        # exp_id = "E-GEOD-12767"
        # exp = Experiment.objects.get(data__contains={'accession':exp_id})# exp.has_minimal()

        
            
        # samples = total_samples()
        # for sample in Sample.objects.all():
        #     sample_attributes = SampleAttribute.objects.filter(sample=sample)
        #     for sample_attribute in sample_attributes:
        #         if sample_attribute.old_value:
        #             if 'basal' in sample_attribute.old_value:
        #                 print(sample_attribute.old_value, sample.experiment)


