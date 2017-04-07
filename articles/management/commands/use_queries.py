from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *




class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
<<<<<<< Updated upstream
        command's handle method
        """
        get_exp_status()
=======
        command's hande method
        """        

        list_old_names_values_with_unified()
    

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

        # samples_by_diagnosis()


 