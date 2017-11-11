from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

from articles.getdata import *


class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        experiment_id = 'E-GEOD-10588'

        exp = Experiment.objects.get(data__contains={'accession':experiment_id})
        health_range = list(range(225470,225481)) + list(range(225483,225498))
        pre_eclampsia_range = list(range(225481,225482))+list(range(225498,225514))
        health_samples = ['GSM'+str(item) for item in health_range]
        pre_eclampsia_samples = ['GSM'+str(item) for item in pre_eclampsia_range]

        diagnosis = StandardName.objects.get(name='Diagnosis')
        pre_eclampsia = StandardValue.objects.get(value='severe preeclampsia')
        health = StandardValue.objects.get(value='Health')

        samples_in_experiment= Sample.objects.filter(experiment=exp)

        for sample in samples_in_experiment:
            sample_name = SampleAttribute.objects.get(
                            sample=sample,
                            old_name='name').old_value
            sample_name = str(sample_name)[:-2] # delete " 1" in the end 
            print(sample_name)
            if sample_name in health_samples:
                SampleAttribute.objects.create(sample=sample, 
                                               unificated_name=diagnosis,
                                               unificated_value=health)
                
                
            elif sample_name in pre_eclampsia_samples:
                SampleAttribute.objects.create(sample=sample, 
                                               unificated_name=diagnosis,
                                               unificated_value=pre_eclampsia)
                # for item in d:
                #     item.delete()
                
            else:
                print("something went wrong")




        