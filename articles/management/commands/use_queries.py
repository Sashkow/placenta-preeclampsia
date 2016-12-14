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
        # list_old_names_values_with_unified()

        exp = Experiment.objects.get(data__contains={'accession':'E-GEOD-4707'})

        samples = Sample.objects.filter(experiment=exp)

        for sample in samples:
            sample.

        diagnosis = UnificatedSamplesAttributeName.objects.get(name='Diagnosis')

        # attributes = SampleAttribute.objects.filter(sample__in=samples, unificated_name=diagnosis)

        attributes = SampleAttribute.objects.filter(sample__in=samples)


        for attribute in attributes:
            if 
            SampleAttribute.objects.create()

        """
        для кожного семпла з екперимента: Якщо в семплі ще не має потрібного атрибута тоді створити новий, інакше додати в той, що є     """







  


