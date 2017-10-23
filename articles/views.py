import collections
# from django.shortcuts import render, render_to_response, HttpResponseRedirect
# import django

# tutorial/views.py
from django.shortcuts import render
# from django_tables2 import RequestConfig
import django_tables2 as tables

# from articles.models import *
# from articles.tables import *

from articles.models import Sample, Experiment, Microarray, ColumnOrder

from articles.queries import sample_attribute_name_value


def get_column_class_names(self, classes_set, bound_column):
    '''
    An override. Returns a set of HTML class names for cells (both td and th) of a
    **bound column** in this table.
    By default this returns the column class names defined in the table's
    attributes, and additionally the bound column's name.
    This method can be overridden to change the default behavior, for
    example to simply `return classes_set`.
    Arguments:
        classes_set(set of string): a set of class names to be added
          to the cell, retrieved from the column's attributes. In the case
          of a header cell (th), this also includes ordering classes.
          To set the classes for a column, see `.Column`.
          To configure ordering classes, see :ref:`ordering-class-name`
        bound_column(`.BoundColumn`): the bound column the class names are
          determined for. Useful for accessing `bound_column.name`.
    Returns:
        A set of class names to be added to cells of this column
    '''
    joined_column_name = bound_column.name.replace(' ', '_').replace(',', '_')
    classes_set.add(joined_column_name)
    return classes_set


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


    # print("all", Experiment.objects.all())
    exps_dicts = [exp.to_dict() for exp in Experiment.objects.all()]


    table = ExpTable(exps_dicts)
    tables.RequestConfig(request,  paginate={'per_page': 100}).configure(table)
    table.name = 'Experiments'
    return table


#not a view
def build_mic_table(request):
    """

    """
    cols = {
            attr:
            tables.Column()
            for attr in Microarray.must_have_attributes
    }

   
    MicTable = type('MicTable', (tables.Table,), cols)
    MicTable._meta.attrs = {'class':'table table-hover'}

    exps_dicts = [mic.to_dict() for mic in Microarray.objects.all()]

    table = MicTable(exps_dicts)
    tables.RequestConfig(request,  paginate={'per_page': 100}).configure(table)
    table.name = 'Microarrays'
    return table


#not a view
def build_sample_table(request):
    all_col_orders = ColumnOrder.objects.all()

    col_order = list(all_col_orders.values_list(
            "unificated_name__name", "column_order"))
    
    col_order = sorted(col_order, key=lambda item:item[1])
    
    ordered_cols = [item[0] for item in col_order]
    
    


    
    sample_dicts = Sample.to_dict()
    

    # for sample_dict in sample_dicts:
    #     for attribute in sample_dict:
    #         if attribute not in cols:
    #             cols[attribute] = tables.Column()



    
    # col_sequence = (
    #         'experiment', 
    #         'name', 
    #         'Biological Specimen', 
    #         'Diagnosis', 
    #         'Gestational Age', 
    #         'Fetus Sex',
    #         'Maternal Age',
    #         'Cells, Cultured')


    # cols = {col:tables.Column() for col in ordered_cols}

    cols = {}
    for col in ordered_cols:
        cols[col] = tables.Column()
    # cols['name'].verbose_name = 'Sample Name'

    # for col in cols:
    #     print("    ",col,cols[col])


    SampleTable = type('SampleTable', (tables.Table,), cols)

    SampleTable.get_column_class_names = get_column_class_names

    

    SampleTable._meta.attrs = {'class':'table table-hover'}
    # set column display order

    # table_column_names = [ column.name for column in SampleTable.columns]
    # for col in ordered_cols:
    #     assert(col in table_column_names)


    
    SampleTable._meta.sequence = tuple(ordered_cols)    

    table = SampleTable(sample_dicts)
    table.name = 'Biological Samples'

    print(dir(table))


    if 'per_page' in request.GET:
        per_page = int(request.GET['per_page'])
        tables.RequestConfig(request,  paginate={'per_page': per_page}).configure(table)
    else:
        tables.RequestConfig(request,  paginate={'per_page': 50}).configure(table)

    # print(dir(table.per_page_field))



    # choose those columns to display by default
    cols_to_show = ColumnOrder.objects.filter(show_by_default=True)
    cols_to_show = list(cols_to_show.values_list(
            "unificated_name__name",
            flat=True))

    for column in table.columns:
        if str(column.header) in cols_to_show:
            column.display = True
        else:
            column.display = False

    


    

    table.leng = len(table.rows)

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

def microarrays(request):
    # display_cols = (
    #        'Title',
    #        )

    table = build_mic_table(request)

    for column in table.columns:
        column.display = True

    return render(
            request,
            'articles/microarrays.html',
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




    search = sample_attribute_name_value()

    # print(search)

    # search = collections.OrderedDict()
    # print("search")
    # for item in search:
    #     print(item,search[item])

    search_checked = ColumnOrder.objects.filter(
            show_by_default=True).values_list('unificated_name__name', flat=True)



    return render(
            request,
            'articles/samples.html',
            {
                # 'column_classes': column_classes,
                'table': table,
                'search': search,
                'search_checked': search_checked
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
