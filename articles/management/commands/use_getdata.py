from django.core.management.base import BaseCommand, CommandError
from articles.getdata import *
from articles.models import Experiment, Microarray



class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        command's hande method
        """  
        plot_annual_attrs_per_sample()   


        # get_expression_matrix()
        

        # count = 0
        # for exp in Experiment.objects.all():
        #     if not 'Excluded' in exp.status() and not exp.is_cell_line():
        #         count += 1
        #         if 'secondaryaccession' in exp.data:
        #             geo = exp.data['secondaryaccession']
        #         else:
        #             geo = "-"

        #         print(exp.data['accession'], geo)
        # print(count)
    
    

    

    # py.sign_in('username', 'api_key')
    # plotly.tools.set_credentials_file(username='lykhenko.olexandr', api_key='rCWQFhYQQNErBAVxXJPf')
    
    

    # trace0 = Scatter(
    #     x=[1, 2, 3, 4],
    #     y=[10, 15, 13, 17]
    # )
    # trace1 = Scatter(
    #     x=[1, 2, 3, 4],
    #     y=[16, 5, 11, 9]
    # )
    # data = Data([trace0, trace1])

    # py.plot(data, filename = 'basic-line')

                

