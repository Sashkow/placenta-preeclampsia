from django.shortcuts import render, render_to_response, HttpResponseRedirect
import django

# tutorial/views.py
from django.shortcuts import render
from django_tables2 import RequestConfig

from articles.models import *
from articles.tables import *

from articles.queries import sample_attribute_name_value_qulalitative


#not a view
def build_exp_table(request):
    """

    """
    cols = {Experiment.must_have_attributes_map[attr] : tables.Column() 
                for attr in Experiment.must_have_attributes
            }

    cols.update({attr : tables.Column() 
                for attr in Experiment.extra_attributes
            })  

    ExpTable = type('ExpTable', (tables.Table,), cols)
    ExpTable._meta.attrs = {'class':'table table-hover'}

    exps_dicts = [exp.to_dict() for exp in Experiment.objects.all()]

    table = ExpTable(exps_dicts)
    RequestConfig(request,  paginate={'per_page': 100}).configure(table)
    table.name = 'Experiments'
    return table

#not a view
def build_sample_table(request):
    # sample_dicts = [sample.to_dict() for sample in Sample.objects.all()]
    sample_dicts = Sample.to_dict()
    cols = {}
    for sample_dict in sample_dicts:
        for attribute in sample_dict:
            if not attribute in cols:
                cols[attribute] = tables.Column()

    # ColumnOrder.objects.all().values("unificated_name__name", "")
    # sorted(cols, key=lambda : student[2]ambda:)

    col_sequence = (
            'experiment', 
            'name', 
            'Biological Specimen', 
            'Diagnosis', 
            'Gestational Age', 
            'Fetus Sex',
            'Maternal Age',
            'Cells, Cultured')


    # cols = {col:tables.Column() for col in col_sequence}
    # cols['name'].verbose_name = 'Sample Name'


    SampleTable = type('SampleTable', (tables.Table,), cols)
    # print(dir(SampleTable.base_columns))
    
    SampleTable._meta.attrs = {'class':'table table-hover'}
    

    table = SampleTable(sample_dicts)
    table.name = 'Biological Samples'

    RequestConfig(request,  paginate={'per_page': 2000}).configure(table)

    cols = ColumnOrder.objects.filter(
            show_by_default=True).select_related("unificated_name")

    



    for column in table.columns:
        if str(column.header) in table_display:
            column.display = True
        else:
            column.display = False


    return table


def experiments(request):    
    display_cols = (
            'Title', 
            )

    table = build_exp_table(request)

    for column in table.columns:
        column.display = True

    return render(
            request,
            'articles/experiments.html',
            {
                'table': table,
            }
    )

def samples(request):
    """
    view all samples with ability to filter by attribute
    names and values
    """
    table = build_sample_table(request)
    print("table")


    search = sample_attribute_name_value_qulalitative()
    print("search")
    # for item in search:
    #     print(item,search[item])

    search_checked = (
        'Biological Specimen', 
        'Diagnosis', 
        'Fetus Sex'
    )

    return render(
            request,
            'articles/samples.html',
            {
                'table': table,
                # 'search': search,
                # 'search_checked': search_checked
            }
    )

def home(request):

    return render(
            request,
            'articles/base.html',
            {
                'samples': len(Sample.objects.all()),
                'experiments': len(Experiment.objects.all()),
                'microarrays': len(Microarray.objects.all()),
            })

