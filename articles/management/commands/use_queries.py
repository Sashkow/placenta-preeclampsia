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
        instance = SampleAttribute.objects.all()[0]
        experiment = instance.sample.experiment

        samples_in_experiment = Sample.objects.filter(experiment=experiment)

        print(len(samples_in_experiment))

        samples_in_experiment=samples_in_experiment.exclude(id=instance.sample.id)

        print(len(samples_in_experiment))
#         search = UnificatedSamplesAttributeValue.objects.get(value="Chorionic Villi")
        

#         samples = SampleAttribute.objects.filter(
# unificated_value=search).values_list('sample', flat=True)

#         samples = Sample.objects.filter(id__in=samples)

#         for sample in samples:
#             print(sample.experiment.data['accession'])


        # Experiment.objects.filter()
        # sample_attribute_name_experiment_value()

        # for obj in Microarray.objects.all():
        #     if 'name' in obj.data:
        #         print(obj.data['name'])
        #     else:
        #         print(None)
        

