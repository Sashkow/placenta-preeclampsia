from django.core.management.base import BaseCommand, CommandError

from articles.models import *

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        command's hande method
        """        
        

        # samples = Sample.objects.all()
        # uns = UnificatedSamplesAttributeName.objects.all()

        # for sample in samples:
        #     for un in uns:
        #         if len(SampleAttribute.objects.filter(
        #           sample=sample,
        #           unificated_name=un)) > 1:
        #             print("!!!!!",sample.experiment.data['accession'], sample.id, un)

        for sample_attribute in SampleAttribute.objects.all():
            un = sample_attribute.unificated_name
            uv = sample_attribute.unificated_value
            if un and uv:
                if un.name == 'Diagnosis' and \
                   uv.value == 'Early Onset Pre-Ecpampsia (at gestational age <31 weeks)':
                    print(sample_attribute.sample.experiment.data['accession'], sample_attribute.sample.id)
