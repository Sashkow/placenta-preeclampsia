from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *




class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):

        print("Receiving incomming transmission...")

        # for attribute  in SampleAttribute.objects.filter(unificated_value=None):
        #     print(attribute)

        print(SampleAttribute.objects.filter(old_value = 'GSM1891989_P13.CEL')[1].sample.experiment)


        # exp = Experiment.find('E-GEOD-73685')
        # print(exp.status())
        # print(exp.cached_status())

        # all_to_tsv()
        # all_experiments_to_tsv()
        # all_samples_to_tsv()

        # i = 0
        #
        # for attribute in SampleAttribute.objects.filter(Q(unificated_name__isnull=True)|Q(unificated_value__isnull=True)):
        #     i += 1
        #     print(i, attribute)



        # sample = SampleAttribute.objects.get(old_value = "GSM1900950 1").sample
        # for attr in SampleAttribute.objects.filter(sample=sample):
        #     print(attr)




            

        # exps = ['E-GEOD-74341', 'E-GEOD-48424', 'E-GEOD-43942', 'E-GEOD-15789',
        #  'E-GEOD-10588', 'E-GEOD-13155', 'E-GEOD-12216'] 
        # for exp in exps:
        #     print(exp, Experiment.objects.get(data__contains = {'accession':exp}).get_microarrays_lst())