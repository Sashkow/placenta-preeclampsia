# from django.shortcuts import render, render_to_response, HttpResponseRedirect
# import django

# tutorial/views.py
from django.shortcuts import render
# from django_tables2 import RequestConfig
import django_tables2 as tables

# from articles.models import *
# from articles.tables import *

from articles.models import Sample, Experiment, Microarray, ColumnOrder

# from articles.queries import sample_attribute_name_value_qulalitative


#not a view
def build_exp_table(request):
    """

    """
    cols = {
        Experiment.must_have_attributes_map[attr]:
            tables.Column()
            for attr in Experiment.must_have_attributes
    }

    cols.update({
        attr:
            tables.Column()
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
    # all_col_orders = ColumnOrder.objects.all()
    # ordered_cols = list(all_col_orders.values_list(
    #         "unificated_name__name",
    #         flat=True))

    # ordered_cols = sorted(
    #         ordered_cols, 
    #         key=lambda name: int(all_col_orders.get(
    #                 unificated_name__name=name).column_order))


    sample_dicts = Sample.to_dict()
    cols = {}
    for sample_dict in sample_dicts:
        for attribute in sample_dict:
            if attribute not in cols:
                cols[attribute] = tables.Column()



    # ColumnOrder.objects.all().values("unificated_name__name", "")
    # sorted(cols, key=lambda : student[2]ambda:)

    # col_sequence = (
    #         'experiment', 
    #         'name', 
    #         'Biological Specimen', 
    #         'Diagnosis', 
    #         'Gestational Age', 
    #         'Fetus Sex',
    #         'Maternal Age',
    #         'Cells, Cultured')


    # cols = {col:tables.Column() for col in col_sequence}
    # cols['name'].verbose_name = 'Sample Name'

    for col in cols:
        print("    ",col,cols[col])


    SampleTable = type('SampleTable', (tables.Table,), cols)
    # print(dir(SampleTable.base_columns))
    
    SampleTable._meta.attrs = {'class':'table table-hover'}
    

    table = SampleTable(sample_dicts)
    table.name = 'Biological Samples'

    tables.RequestConfig(request,  paginate={'per_page': 2000}).configure(table)


    # choose those columns to display by default
    shown_col_orders = ColumnOrder.objects.filter(show_by_default=True)
    cols = list(shown_col_orders.values_list(
            "unificated_name__name",
            flat=True))

    # cols = sorted(cols, key=lambda name: int(shown_col_orders.get(
    #                 unificated_name__name=name).column_order))
    cols = ['Experiment'] + cols

    for column in table.columns:
        if str(column.header) in cols:
            column.display = True
        else:
            column.display = False

    # set column display order
    print(cols)
    table._meta.sequence = tuple(cols)

    return table


def experiments(request):
    # display_cols = (
    #        'Title',
    #        )

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
    print("table")
    table = build_sample_table(request)



    # search = sample_attribute_name_value_qulalitative()
    # print("search")
    # for item in search:
    #     print(item,search[item])


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
                'samples': "100500",# str(len(Sample.objects.all())),
                'experiments': len(Experiment.objects.all()),
                'microarrays': len(Microarray.objects.all()),
            })
