# tutorial/tables.py
import django_tables2 as tables
from articles.models import *

class ExperimentTable(tables.Table):
    class Meta:
        model = Experiment
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}