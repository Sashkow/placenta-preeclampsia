from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *




class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        # all_samples_to_tsv()
        print("here")
        # for exp in Experiment.to_list_of_dicts():
        #     print(exp.keys())

        all_samples_to_tsv()

        # exps = ['E-GEOD-74341', 'E-GEOD-48424', 'E-GEOD-43942', 'E-GEOD-15789',
        #  'E-GEOD-10588', 'E-GEOD-13155', 'E-GEOD-12216'] 
        # for exp in exps:
        #     print(exp, Experiment.objects.get(data__contains = {'accession':exp}).get_microarrays_lst())