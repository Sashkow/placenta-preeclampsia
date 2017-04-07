from django.core.management.base import BaseCommand, CommandError
from articles.getdata import *
from articles.models import Experiment, Microarray



class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        """
        annual_attributes_per_sample_in_placenta()
        # lst = get_placenta_accession()
        # experiment_id = lst[0]
        # # get_experiment_attributes(experiment_id)
        # print(get_experiment_samples_attributes(experiment_id))

        