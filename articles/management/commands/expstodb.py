from django.core.management.base import BaseCommand, CommandError
from articles.getdata import exp_to_db, get_preeclampsia_accession, print_exp_array_title
from articles.models import Experiment

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        command's hande method
        """
        self.stdout.write("performs")
        accessions = get_preeclampsia_accession()
        for accession in accessions:
            print("Adding", accession, "to db")        
            exp_to_db(accession)

                                
        # for accession in accessions:
        #     print_exp_array_title(accession)

