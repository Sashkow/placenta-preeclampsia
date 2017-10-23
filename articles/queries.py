import collections
from articles.models import *
# from prettytable import PrettyTable

from django.db.models import Q

from plotly.graph_objs import *
import plotly.plotly as py
import plotly.graph_objs as go
import plotly



import numpy as np


def get_healthy_term():
    """
    get all exps that are term
    """
    exps = []
    samples = total_samples()
    term_samples = []

    for sample in samples:
        if sample.get_gestational_age_category() == "Term" and sample.get_attribute_value('Diagnosis') == 'Healthy':
            print(sample)
            term_samples.append(sample.get_attribute_value('Sample Name'))
    #         exp = str(sample.experiment)
    #         if not exp in exps:
    #             exps.append(exp)

    # print(len(exps), exps)
    # for exp in exps:
    #     print(exp)

    print(term_samples)
    print(len(term_samples))


 





def get_exp_status():
    exp = Experiment.objects.filter(data__contains ={'accession':'E-GEOD-25906'}).exists()
    print(exp)



def all_samples_to_tsv():
    samples = Sample.to_dict()
    column_names = ColumnOrder.objects.all().order_by(
            'column_order').values_list('unificated_name__name', flat=True)

    with open('articles/static/tsv/samples.tsv','w') as tsv:
        tsv.write('\t'.join(column_names)+'\n')
        for sample in samples:
            row = []
            for column_name in column_names:
                if column_name in sample:
                    row.append(sample[column_name])
                else:
                    row.append("_")
            tsv.write("\t".join(row)+'\n')


def all_experiments_to_tsv():
    mapp = Experiment.must_have_attributes_map
    must_have = [mapp[item] for item in Experiment.must_have_attributes]
    extra = Experiment.extra_attributes

    column_names = must_have + extra

    experiments = [exp.to_dict() for exp in Experiment.objects.all()]

    with open('articles/static/tsv/experiments.tsv','w') as tsv:
        tsv.write('\t'.join(column_names)+'\n')
        for exp in experiments:
            row = []
            for column_name in column_names:
                if column_name in exp:
                    row.append(exp[column_name])
                else:
                    row.append("_")
            tsv.write("\t".join(row)+'\n')


def all_microarrays_to_tsv():
    column_names = Microarray.must_have_attributes

    microarrays = [item.to_dict() for item in Microarray.objects.all()]

    with open('articles/static/tsv/microarrays.tsv','w') as tsv:
        tsv.write('\t'.join(column_names)+'\n')
        for microarray in microarrays:
            row = []
            for column_name in column_names:
                if column_name in microarray:
                    row.append(microarray[column_name])
                else:
                    row.append("_")
            tsv.write("\t".join(row)+'\n')





def fullfill_column_order_with_defaluts():
    names = UnificatedSamplesAttributeName.objects.all()
    ordered_names = ColumnOrder.objects.all().values_list("unificated_name", flat=True)

    for name in names:
        if not (name in ordered_names):
            ColumnOrder.objects.create(unificated_name=name)


def set_has_minimal():
    for exp in Experiment.objects.all():
        exp.set_has_minimal()


def cluster_samples():
    # """
    # split samples into classes of equivalence based on Diagnosis,
    # Gestational Age and Biological Specimen
    # """

    # samples = total_samples()

    # diagnosis = UnificatedSamplesAttributeName.objects.get(name="Diagnosis")
    
    # specimen = UnificatedSamplesAttributeName.objects.get(name="Biological Specimen")


    # diagnosis_values = UnificatedSamplesAttributeValue.objects.filter(
    #         unificated_name=diagnosis) #.values_list('value', flat=True).order_by()

    # geatation_values = [
    #         "First Trimester",
    #         "Second Trimester",
    #         "Early Preterm",
    #         "Late Preterm",
    #         "Term"
    #             ]

    # specimen_values = UnificatedSamplesAttributeValue.objects.filter(
    #         unificated_name=specimen) #.values_list('value', flat=True).order_by()

    # groups = {}

    # print("start:")

    # for diagnosis_value in diagnosis_values:
    #     for specimen_value in specimen_values:
    #         for gestation_value in geatation_values:
    #             group_name = " ".join([str(diagnosis_value.value),
    #                                    str(specimen_value.value),
    #                                    str(gestation_value)
    #                                     ])

    #             if not group_name in groups:
    #                 groups[group_name] = [[], 0]

    # print("mapping:")

    # for sample in samples:
    #     diag = sample.get_attribute_value(diagnosis)
    #     gest = sample.get_gestational_age_category()
    #     spec = sample.get_attribute_value(specimen)

    #     group_name = " ".join([str(diag),
    #                            str(spec),
    #                            str(gest),
    #                             ])
    #     if group_name in groups:
    #         if not (str(sample.experiment) in groups[group_name][0]):
    #             groups[group_name][0].append(str(sample.experiment))
    #         groups[group_name][1] += 1
    #     else:
    #         print(group_name, sample.experiment)

    import pickle
    # with open('mapping.txt', 'wb') as f:
    #     pickle.dump(groups, f)

    with open('mapping.txt', 'rb') as f:
        groups = pickle.load(f)

    summ = 0
    merged_list = []

    for group in sorted(groups):
        if groups[group][1] > 0 and not "Adipose" in group and not "Blood" in group:
            print(group, groups[group])




    #     if groups[group][1] > 0:
    #         # if "Healthy" in group and not "Adipose" in group and not "Blood" in group:
    #         current_list = [str(item) for item in groups[group][0]]  
    #         merged_list = merged_list + list(set(current_list) - set(merged_list))
    # print(merged_list)
    # print(len(merged_list))


def experiments_with_no_gestation_age():
    exps = Experiment.objects.all()
    needed_exps = []
    for exp in exps:
        if not (exp.has_minimal() or 
                exp.is_cell_line() or 
                exp.is_excluded()):
            needed_exps.append(exp)
    for exp in needed_exps:
        print(exp, end=", ")
    print(len(needed_exps))
    return needed_exps


def coverage():
    """
    for each UnificatedSampleAttributeName print amount of sapmles that contain it
    :return:
    """
    samples = total_samples()
    total = len(samples)
    attributes = SampleAttribute.objects.filter(sample__in=samples)
    lst = []
    names = UnificatedSamplesAttributeName.objects.all()
    
    for name in names:
        count = attributes.filter(
          unificated_name=name).values('sample').distinct().count()
        if count:
            lst.append((name.name, round(float(count)/total, 2)))
    lst = sorted(lst, key=lambda nme: nme[1], reverse=True)
    for item in lst:
        print(item[0],item[1],sep='\t')




# def list_old_names_values_with_unified():
#     """
#     uniqe rows:
#         old_name old_value unificated_name unificated_value
#     """

#     mappings = SampleAttribute.objects.filter(
#       unificated_value__unificated_name__name='Common'
#         ).values('old_name','unificated_name').distinct().order_by('unificated_name')

#     count = 0
#     for mapping in mappings:
#         if mapping['old_name'] != 'name':
            
#             if mapping['unificated_name'] and mapping['unificated_value']:
#                 count += 1
#                 print(UnificatedSamplesAttributeName.objects.get(id=mapping['unificated_name']),
#                       # UnificatedSamplesAttributeValue.objects.get(id=mapping['unificated_value']),
#                       mapping['old_name'],
#                       # mapping['old_value'],
#                       # mapping['sample']
#                       )
#     print(count)

def get_values(unificated_name):
    attributes = SampleAttribute.objects.filter(unificated_name=unificated_name)
    values = {}
    for attribute in attributes:
        if attribute.unificated_value:

            value = attribute.unificated_value.value
            
            old_value = attribute.old_value
            if value in values:
                old_values = values[value]
                if not (old_value in old_values):
                    old_values.append(old_value)
                    print("     ", value, old_value)
            else:
                values[value] = [old_value,]
    return values

def coma(lst):
    return ", ".join(lst)


def list_old_names_values_with_unified():
    """
    uniqe rows:
        old_name old_value unificated_name unificated_value
    names = {
                    "unificated_name":[["old_name", "old_name",...,], structure2],
                    "unificated_name":[["old_name", "old_name",...,], structure2],
                    ...
                 }

    values = {
                    "unificated_value":["old_value", "old_value",...],
                    "unificated_value":["old_value", "old_value",...],
                    ...
                 }
    
                    
    """
    unificated_names = UnificatedSamplesAttributeName.objects.filter(~Q(name='name'))

    attributes = SampleAttribute.objects.filter(~Q(unificated_name=None), unificated_value__unificated_name__name='Common')
    names = {}

    for attribute in attributes:
        if attribute.unificated_name and attribute.unificated_value:
            name = attribute.unificated_name.name
            old_name = attribute.old_name
            
            if name in names:
                old_names = names[name][0] 
                if not (old_name in old_names):
                    old_names.append(old_name)
                    print(name, old_name)

            else:
                # values = get_values(attribute.unificated_name)
                values = 0
                names[name] = [[old_name,], values]

        
    import pickle
    
    file = open('dump.txt', 'wb')
    pickle.dump(names, file)
    file.close()
    # import pickle 
    # file = open('dump.txt', 'rb')
    # names = pickle.load(file)

    for name in names:
        old_names = names[name][0]
        old_names = [str(item) for item in old_names if item]
        if old_names:
            print(name, "("+", ".join(old_names)+')')
        else:
            print(name)
        # values = names[name][1]
        # for value in values:
        #     old_values = values[value]
        #     old_values = [str(item) for item in old_values if item]
        #     if old_values:
        #         print("    ", value, "("+", ".join(old_values)+')')
        #     else:
        #         print("    ", value)





    # mappings = SampleAttribute.objects.filter(
    #   unificated_value__unificated_name__name='Common'
    #     ).values('old_name','unificated_name').distinct().order_by('unificated_name')

    # count = 0
    # for mapping in mappings:
    #     if mapping['old_name'] != 'name':
            
    #         if mapping['unificated_name'] and mapping['unificated_value']:
    #             count += 1
    #             print(UnificatedSamplesAttributeName.objects.get(id=mapping['unificated_name']),
    #                   # UnificatedSamplesAttributeValue.objects.get(id=mapping['unificated_value']),
    #                   mapping['old_name'],
    #                   # mapping['old_value'],
    #                   # mapping['sample']
    #                   )
    # print(count)


from django.db.models import Q


def list_old_names_values_with_unified():
    """
    uniqe rows:
        old_name old_value unificated_name unificated_value
    """

    mappings = SampleAttribute.objects.filter(
      unificated_value__unificated_name__name='Common'
        ).values('old_name','unificated_name').distinct().order_by('unificated_name')

    count = 0
    for mapping in mappings:
        if mapping['old_name'] != 'name':
            
            if not (mapping['unificated_name']==None and mapping['unificated_value']==None):
                count += 1
                print(UnificatedSamplesAttributeName.objects.get(id=mapping['unificated_name']),
                      # UnificatedSamplesAttributeValue.objects.get(id=mapping['unificated_value']),
                      mapping['old_name'],
                      # mapping['old_value'],
                      # mapping['sample']
                      )
    print(count)

    print(Sample.objects.get(id = 1059).experiment.data['accession'])





from django.db.models import Q


def list_old_names_values_with_unified():
    """
    uniqe rows:
        old_name old_value unificated_name unificated_value
    """

    mappings = SampleAttribute.objects.filter(
      unificated_value__unificated_name__name='Common'
        ).values('old_name','unificated_name').distinct().order_by('unificated_name')

    count = 0
    for mapping in mappings:
        if mapping['old_name'] != 'name':
            
            if not (mapping['unificated_name']==None and mapping['unificated_value']==None):
                count += 1
                print(UnificatedSamplesAttributeName.objects.get(id=mapping['unificated_name']),
                      # UnificatedSamplesAttributeValue.objects.get(id=mapping['unificated_value']),
                      mapping['old_name'],
                      # mapping['old_value'],
                      # mapping['sample']
                      )
    print(count)

    print(Sample.objects.get(id = 1059).experiment.data['accession'])





def show_exps_of_good_platforms():
    good_platforms = ['GPL570','GPL6244','GPL10558']
    # good_platforms = ['GPL10558',]

    microarrays = []
    for platform in good_platforms:
        microarray = Microarray.objects.filter(data__contains=
          {'secondaryaccession':platform}).first()
        if microarray:
            microarrays.append(microarray)
    print(microarrays)

    

#     for exp in all_exps:
#         if True in \
# [True for microarray in microarrays if microarray in exp.microarrays.all()]:
#             exps.append(exp)

    exps = Experiment.objects.filter(microarrays__in=microarrays)
    minimal_exps = [exp for exp in exps if exp.has_minimal()]
    for exp in minimal_exps:
        print(exp)

    samples = Sample.objects.filter(experiment__in=minimal_exps)
    human_health = []
    for sample in samples:
        is_human = SampleAttribute.objects.filter(
          sample=sample,
          unificated_name__name='Classification',
          unificated_value__value='Humans').exists()
        is_healthy = SampleAttribute.objects.filter(
          sample=sample,
          unificated_name__name='Diagnosis',
          unificated_value__value='Health').exists()
        if is_human and is_healthy:
            human_health.append(sample)
            age = SampleAttribute.objects.filter(
              sample=sample,
              unificated_name__name='Gestational Age').first().old_value
            print(age)

    for exp in minimal_exps:
        print(exp.data['secondaryaccession'])
        print(exp.microarrays.all())


def show_unfilled_samples():
    exp_id = 'E-GEOD-15787'
    exp = Experiment.objects.get(data__contains={'accession':exp_id})

    samples = Sample.objects.filter(
      experiment__data__contains={'accession':exp_id})
    attrs = SampleAttribute.objects.filter(sample__in=samples)
    for attr in attrs:
        if attr.unificated_name==None or attr.unificated_value==None:
            print(attr)


def show_experiment_samples(exp_id):
    # exp_id = 'E-GEOD-74341'
    exp = Experiment.objects.get(data__contains={'accession':exp_id})

    samples = Sample.objects.filter(
      experiment=exp)
    for sample in samples:
        print(sample)
        attributes = SampleAttribute.objects.filter(sample=sample)
        for attribute in attributes:
            if attribute.unificated_value.unificated_name.name=='Common':
                print("    ",
                      attribute.unificated_name,
                      attribute.old_value)
            else:
                print("    ",
                      attribute.unificated_name,
                      attribute.unificated_value)

    # names = attributes.order_by().values_list(
    #   'old_name', flat=True).distinct()
    # for name in names:
    #     print(name)
    #     values = attributes.filter(sample__in=samples,
    #       old_name=name).order_by().values_list('old_value', flat=True).distinct()
    #     for value in values:
    #         print("    ", value)
    

def sample_attribute_old_name_value():
    """
    for each sample attribute name print in which experiments it appears add
    which values it takes in those experiments
    """
    samples = total_samples()

    attributes = SampleAttribute.objects.filter(sample__in=samples)

    names = attributes.order_by().values_list(
      'old_name', flat=True).distinct()

    with open("names_values.txt", "w") as text_file:
        for name in names:
            print(name, file=text_file)
            print(name)

            values = SampleAttribute.objects.filter(sample__in=samples,
              old_name=name).order_by().values_list(
                'old_value', flat=True).distinct()
            for value in values:
                print("     ", value, file=text_file)
                print("     ", value)


def sample_attribute_name_value():
    """
    returns {unificated_name: [unificated_values]} dict
    """

    unificated_values = UnificatedSamplesAttributeValue.objects.all(
            ).select_related("unificated_name")

    all_col_orders = ColumnOrder.objects.filter(show_at_all=True)

    ordered_names = all_col_orders.order_by('column_order').values_list(
            "unificated_name__name", flat=True)




    name_values = collections.OrderedDict()

    for name in ordered_names:
        name_values[name] = []

    for unificated_value in unificated_values:
        name = unificated_value.unificated_name.name
        value = unificated_value.value
        if name in name_values:
            name_values[name].append(value)

    # for name in name_values:
    #     print(name, ":", name_values[name])




    return name_values




    # for unificated_name in unificated_names:
    #     name = unificated_name.name
    #     unificated_values = UnificatedSamplesAttributeValue.objects.filter(
    #       unificated_name=unificated_name)

    #     unificated_values_values = list([item.value for item in unificated_values])
    #     print(unificated_name.name, unificated_values_values)


exp_ids = ['E-GEOD-31679', 'E-GEOD-30186', 'E-GEOD-15789', 
           'E-GEOD-24129', 'E-GEOD-10588', 'E-GEOD-13155',
           'E-GEOD-14722', 'E-GEOD-12767', 'E-GEOD-13475', 'E-GEOD-12216',
           'E-GEOD-9984', 'E-GEOD-6573', 'E-GEOD-4100', 'E-GEOD-4707', 'E-GEOD-73375']


def total_samples():
    all_exps = Experiment.objects.all()
    total_total = []
    total = []
    exps =[]
    has_minimal = []
    mail_sent = []
    mail_received=[]

    for exp in all_exps:
        if not ('excluded' in exp.data):
            total_total.append(exp)
            if not exp.is_cell_line():
                total.append(exp) 

            #     if exp.has_minimal():
            #         has_minimal.append(exp)
            #     if exp.is_unified():
            #         exps.append(exp)
            # if 'mail sent' in exp.data:
            #     mail_sent.append(exp)
            # if 'mail received' in exp.data:
            #     mail_received.append(exp)


    samples = Sample.objects.filter(experiment__in=total)
    print('total exps with cell lines', len(total_total))
    print('total exps', len(total))

    # print('total',len(Sample.objects.filter(experiment__in=total)))
    # print('unified',len(samples))
    # print('has_minimal',len(Sample.objects.filter(experiment__in=has_minimal)))
    # print('mail_sent',len(mail_sent))
    # print('mail received',len(mail_received))
    return samples


def culture_samples():
    all_exps = Experiment.objects.all()
    culture = []

    for exp in all_exps:
        if exp.is_cell_line():
            culture.append(exp)

    samples = Sample.objects.filter(experiment__in=culture)
    print('culture exps', len(culture))
    print('culture samples',len(samples))
    return samples


def samples_by_diagnosis():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Diagnosis')
    organism_parts = UnificatedSamplesAttributeValue.objects.filter(unificated_name=organism_part)

    parts_dict = {}
    for part in organism_parts:
        parts_dict[part.value] = 0
    parts_dict["other"] = 0

    samples = total_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            organism_part_value = SampleAttribute.objects.get(sample=sample, 
              unificated_name=organism_part).unificated_value.value
            parts_dict[organism_part_value]+=1
        else:
            # print(sample.experiment.data['accession'], sample.id)
            parts_dict["other"]+=1

    for part in parts_dict:
        print(part, parts_dict[part])
    return parts_dict


def samples_by_organism_part():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Biological Specimen')
    organism_parts = UnificatedSamplesAttributeValue.objects.filter(unificated_name=organism_part)

    
    parts_dict = {}
    for part in organism_parts:
        parts_dict[part.value] = 0
    parts_dict["Unknown"] = 0

    samples = total_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            organism_part_value = SampleAttribute.objects.get(sample=sample, 
              unificated_name=organism_part).unificated_value.value
            parts_dict[organism_part_value]+=1
        else:
            print(sample.experiment.data['accession'], sample.id)
            parts_dict["Unknown"]+=1

    for part in parts_dict:
        print(part, parts_dict[part])
    return parts_dict


def samples_by_cells_cultured():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Organism Part')
    cells_cultured = UnificatedSamplesAttributeName.objects.get(name='Cells, Cultured')
    cells_cultures = UnificatedSamplesAttributeValue.objects.filter(unificated_name=cells_cultured)

    cultures_dict = {}
    for culture in cells_cultures:
        cultures_dict[culture.value] = 0
    cultures_dict["other"] = 0
    total = 0
    samples = culture_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            pass
        else:
            total+=1
            if SampleAttribute.objects.filter(
              sample=sample,
              unificated_name=cells_cultured).exists():
                culture_value = SampleAttribute.objects.filter(sample=sample, 
                  unificated_name=cells_cultured)[0].unificated_value.value
                # print(sample.experiment.data['accession'], sample.id)
                cultures_dict[culture_value]+=1
            else:
                # print(sample.experiment.data['accession'], sample.id)
                cultures_dict["other"]+=1

    print(cultures_dict)
    print('total',total)
    return cultures_dict


def samples_by_trim():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Pregnancy Trimesters')
    organism_parts = UnificatedSamplesAttributeValue.objects.filter(unificated_name=organism_part)

    
    parts_dict = {}
    for part in organism_parts:
        parts_dict[part.value] = 0
    parts_dict["other"] = 0

    samples = total_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            organism_part_value = SampleAttribute.objects.get(sample=sample, 
              unificated_name=organism_part).unificated_value.value
            # print(sample.experiment.data['accession'])
            parts_dict[organism_part_value]+=1
        else:
            parts_dict["other"]+=1

    print(parts_dict)
    return parts_dict


def samples_by_gestation_age():
    cells_cultured = UnificatedSamplesAttributeName.objects.get(name='Cells, Cultured')
    trim = UnificatedSamplesAttributeName.objects.get(name='Pregnancy Trimesters')
    age = UnificatedSamplesAttributeName.objects.get(name='Gestational Age')
    

    
    parts_dict = {}
    parts_dict['Age'] = 0
    parts_dict['ApproximateAge'] = 0


    at_birth_conditions = ['Caesarean Section', 'Labor, Obstetric', 'Delivery, Obstetric']
    total = 0
    tr = 0
    samples = total_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=age).exists():
            parts_dict['Age'] += 1
        else:
            parts_dict['ApproximateAge'] += 1
            # organism_part_value = SampleAttribute.objects.get(sample=sample, 
            #   unificated_name=organism_part).unificated_value

            
    #     elif SampleAttribute.objects.filter(
    #       sample=sample,
    #       unificated_name=trim).exists():
    #         parts_dict['Trimesters'] += 1
    #     elif SampleAttribute.objects.filter(
    #       sample=sample,
    #       unificated_name=cells_cultured).exists():
    #         pass

    #     elif SampleAttribute.objects.filter(
    #       sample=sample,
    #       unificated_name__name='Gestational Age Upper Bound').exists() or \
    #          SampleAttribute.objects.filter(
    #       sample=sample,
    #       unificated_name__name='Gestational Age Lower Bound').exists():
    #         parts_dict['ApproximateAge'] += 1
    #     elif SampleAttribute.objects.filter(
    #       sample=sample,
    #       unificated_name__name__in=at_birth_conditions).exists():
    #         parts_dict['AtBirth'] += 1
    #     else:
    #         parts_dict['Unknown'] += 1
    #         # print(sample.experiment.data['accession'], sample.id)
    # print(parts_dict)

            
        # elif SampleAttribute.objects.filter(
        #   sample=sample,
        #   unificated_name=trim).exists():
        #     parts_dict['Trimesters'] += 1
        # elif SampleAttribute.objects.filter(
        #   sample=sample,
        #   unificated_name=cells_cultured).exists():
        #     pass

        # elif SampleAttribute.objects.filter(
        #   sample=sample,
        #   unificated_name__name='Gestational Age Upper Bound').exists() or \
        #      SampleAttribute.objects.filter(
        #   sample=sample,
        #   unificated_name__name='Gestational Age Lower Bound').exists():
        #     parts_dict['ApproximateAge'] += 1
        # elif SampleAttribute.objects.filter(
        #   sample=sample,
        #   unificated_name__name__in=at_birth_conditions).exists():
        #     parts_dict['AtBirth'] += 1
        # else:
        #     parts_dict['Unknown'] += 1
        #     # print(sample.experiment.data['accession'], sample.id)
    print(parts_dict)

    return parts_dict


def samples_by_race():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Continental Population Groups')
    organism_parts = UnificatedSamplesAttributeValue.objects.filter(unificated_name=organism_part)

    
    parts_dict = {}
    for part in organism_parts:
        parts_dict[part.value] = 0
    parts_dict["other"] = 0

    samples = total_samples()

    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            organism_part_value = SampleAttribute.objects.get(sample=sample, 
              unificated_name=organism_part).unificated_value.value
            # print(sample.experiment.data['accession'])
            parts_dict[organism_part_value]+=1
        else:
            parts_dict["other"]+=1

    print(parts_dict)
    return parts_dict


def gestational_age_distribution():
    samples = total_samples()
    ages = []
    for sample in samples:
        age = sample.get_gestational_age()
        if age:
            ages.append(age)
    ages = [float(age) for age in ages]
    print(ages)
    print(len(ages))
    title = 'Gestational Age Distribution'

    layout = go.Layout(
    title=title,
    xaxis=dict(
        title='Gestational Age'
    ),
    yaxis=dict(
        title='Amount of Samples for Gestational Age'
    ),
    )

    data = [go.Histogram(
        x=ages,
        xbins=dict(start=np.min(ages), size=1, end= np.max(ages))
    )]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=title, fileopt='overwrite')


def stats(plots=True):
    if plots:
        plot(samples_by_organism_part(),"Organism Part")
        plot(samples_by_diagnosis(),"Diagnosis")
        plot(samples_by_cells_cultured(),"Cultured Cells")
        plot(samples_by_gestation_age(),"Gestational Age")
        plot(samples_by_race(),"Race")
    else:
        print("Organism Part")
        samples_by_organism_part()
        print("Diagnosis")
        samples_by_diagnosis()
        print("Cultured Cells")
        samples_by_cells_cultured()
        print("Gestational Age")
        samples_by_gestation_age()
        print("Race")
        samples_by_race()


def plot(labels_values, title):
    fig = {
        'data': [{'labels': list(labels_values.keys()),
                  'values': list(labels_values.values()),
                  'type': 'pie'}],
        'layout': {'title': title,
                   'legend':{'font':{'size':24}}
            
         }
    }

    py.plot(fig, filename=title, fileopt='overwrite', auto_open=False)