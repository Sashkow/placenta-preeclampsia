from django.core.management.base import BaseCommand, CommandError
from articles.getdata import *
from articles.models import Experiment, Microarray



class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        """
        print_exp_accession_microarrays_platform_name()

        
        # lst = get_placenta_accession()
        # experiment_id = lst[0]
        # # get_experiment_attributes(experiment_id)
        # print(get_experiment_samples_attributes(experiment_id))

        