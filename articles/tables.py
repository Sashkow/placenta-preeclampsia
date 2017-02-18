# tutorial/tables.py
from django_tables2 import Table
from articles.models import Experiment


class ExperimentTable(Table):
    class Meta:
        model = Experiment
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
