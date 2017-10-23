from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

from articles.getdata import *





class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        experiment_id = 'E-GEOD-14722'

        exp = Experiment.objects.get(data__contains={'accession':experiment_id})
        samples = Sample.objects.filter(experiment=exp)
        samples.delete()


        experiment, microarrays = get_experiment_attributes(experiment_id)
        samples = get_experiment_samples_attributes(experiment_id)
        experiment_obj = Experiment.add_or_replace(data=experiment)


        for microarray in microarrays:
            microarray_obj = Microarray.add_or_replace(data=microarray)
            if not(experiment_obj.microarrays.filter(id=microarray_obj.id).exists()):
                experiment_obj.microarrays.add(microarray_obj)
                experiment_obj.save()

        for sample in samples:  
            sample_obj = Sample.objects.create(experiment=experiment_obj)

            ample_attributes = SampleAttribute.objects.filter(sample=sample_obj)
            for old_name, old_value in sample.items():

                if old_value == None or old_value == '':
                    SampleAttribute.add_or_replace(sample_obj, old_name, '<empty>')
                elif old_name == 'condition':
                    week_diagnosis = old_value.split(' ')
                    week = week_diagnosis[0][:-2].strip()
                    diagnosis = week_diagnosis[1].strip()
                    SampleAttribute.add_or_replace(sample_obj, 'gestational age', week)
                    SampleAttribute.add_or_replace(sample_obj, 'diagnosis', diagnosis)
                else:
                    SampleAttribute.add_or_replace(sample_obj, old_name, old_value)