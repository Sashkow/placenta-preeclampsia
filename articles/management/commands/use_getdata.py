from django.core.management.base import BaseCommand, CommandError
from articles.getdata import *
from articles.models import Experiment, Microarray



class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        """
        exp = 'E-GEOD-73685'
        # exp_to_db(exp)
        # unify_exp(exp)

        # tsv_to_db()

        for item in StandardValue.objects.all():
            print(item.value)

        
        # lst = get_placenta_accession()
        # experiment_id = lst[0]
        # # get_experiment_attributes(experiment_id)
        # print(get_experiment_samples_attributes(experiment_id))