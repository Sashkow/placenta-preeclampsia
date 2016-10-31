
from articles.models import *
from prettytable import PrettyTable

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


def show_experiment_samples(exp):
    # exp_id = 'E-GEOD-74341'
    # exp = Experiment.objects.get(data__contains={'accession':exp_id})

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



    samples_in_experinment = Sample.objects.filter(
      experiment__data__contains={'accession':'E-GEOD-74341'})

    attributes = SampleAttribute.objects.filter(sample__in=samples_in_experinment)

    names = attributes.order_by().values_list(
      'old_name', flat=True).distinct()

    with open("names_values.txt", "w") as text_file:
        for name in names:
            print(name, file=text_file)
            print(name)

            values = SampleAttribute.objects.filter(sample__in=samples_in_experinment,
              old_name=name).order_by().values_list(
                'old_value', flat=True).distinct()
            for value in values:
                print("     ", value, file=text_file)
                print("     ", value)


def sample_attribute_name_value():
    """
    for each sample attribute name print in which experiments it appears add
    which values it takes in those experiments
    """
    unificated_names = UnificatedSamplesAttributeName.objects.all()

    for unificated_name in unificated_names:
        unificated_values = UnificatedSamplesAttributeValue.objects.filter(
          unificated_name=unificated_name)
        unificated_values_values = list([item.value for item in unificated_values])
        print(unificated_name.name, unificated_values_values)


          
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
                if exp.has_minimal():
                    has_minimal.append(exp)
                if exp.is_unified():
                    exps.append(exp)
            if 'mail sent' in exp.data:
                mail_sent.append(exp)
            if 'mail received' in exp.data:
                mail_received.append(exp)


    samples = Sample.objects.filter(experiment__in=exps)
    print('total exps with cell lines', len(total_total))
    print('total exps', len(total))
    print('total',len(Sample.objects.filter(experiment__in=total)))
    print('unified',len(samples))
    print('has_minimal',len(Sample.objects.filter(experiment__in=has_minimal)))
    print('mail_sent',len(mail_sent))
    print('mail received',len(mail_received))
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
        parts_dict[part] = 0
    parts_dict["other"] = 0

    samples = total_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            organism_part_value = SampleAttribute.objects.get(sample=sample, 
              unificated_name=organism_part).unificated_value
            parts_dict[organism_part_value]+=1
        else:
            # print(sample.experiment.data['accession'], sample.id)
            parts_dict["other"]+=1

    print(parts_dict)



def samples_by_organism_part():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Organism Part')
    organism_parts = UnificatedSamplesAttributeValue.objects.filter(unificated_name=organism_part)

    
    parts_dict = {}
    for part in organism_parts:
        parts_dict[part] = 0
    parts_dict["other"] = 0

    samples = total_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            organism_part_value = SampleAttribute.objects.get(sample=sample, 
              unificated_name=organism_part).unificated_value
            parts_dict[organism_part_value]+=1
        else:
            print(sample.experiment.data['accession'], sample.id)
            parts_dict["other"]+=1

    print(parts_dict)

def samples_by_cells_cultured():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Organism Part')
    cells_cultured = UnificatedSamplesAttributeName.objects.get(name='Cells, Cultured')
    cells_cultures = UnificatedSamplesAttributeValue.objects.filter(unificated_name=cells_cultured)

    cultures_dict = {}
    for culture in cells_cultures:
        cultures_dict[culture] = 0
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
                  unificated_name=cells_cultured)[0].unificated_value
                # print(sample.experiment.data['accession'], sample.id)
                cultures_dict[culture_value]+=1
            else:
                # print(sample.experiment.data['accession'], sample.id)
                cultures_dict["other"]+=1

    print(cultures_dict)
    print('total',total)

def samples_by_trim():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Pregnancy Trimesters')
    organism_parts = UnificatedSamplesAttributeValue.objects.filter(unificated_name=organism_part)

    
    parts_dict = {}
    for part in organism_parts:
        parts_dict[part] = 0
    parts_dict["other"] = 0

    samples = total_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            organism_part_value = SampleAttribute.objects.get(sample=sample, 
              unificated_name=organism_part).unificated_value
            # print(sample.experiment.data['accession'])
            parts_dict[organism_part_value]+=1
        else:
            parts_dict["other"]+=1

    print(parts_dict)

def samples_by_gestation_age():
    cells_cultured = UnificatedSamplesAttributeName.objects.get(name='Cells, Cultured')
    trim = UnificatedSamplesAttributeName.objects.get(name='Pregnancy Trimesters')
    age = UnificatedSamplesAttributeName.objects.get(name='Gestational Age')
    

    
    parts_dict = {}
    parts_dict['Age'] = 0
    parts_dict['ApproximateAge'] = 0
    parts_dict['Trimesters'] = 0
    parts_dict['AtBirth'] = 0
    parts_dict['Unknown'] = 0

    at_birth_conditions = ['Caesarean Section', 'Labor, Obstetric', 'Delivery, Obstetric']
    total = 0
    tr = 0
    samples = total_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=age).exists():
            parts_dict['Age'] += 1
            # organism_part_value = SampleAttribute.objects.get(sample=sample, 
            #   unificated_name=organism_part).unificated_value
            
        elif SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=trim).exists():
            parts_dict['Trimesters'] += 1
        elif SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=cells_cultured).exists():
            pass

        elif SampleAttribute.objects.filter(
          sample=sample,
          unificated_name__name='Gestational Age Upper Bound').exists() or \
             SampleAttribute.objects.filter(
          sample=sample,
          unificated_name__name='Gestational Age Lower Bound').exists():
            parts_dict['ApproximateAge'] += 1
        elif SampleAttribute.objects.filter(
          sample=sample,
          unificated_name__name__in=at_birth_conditions).exists():
            parts_dict['AtBirth'] += 1
        else:
            parts_dict['Unknown'] += 1
            # print(sample.experiment.data['accession'], sample.id)
    print(parts_dict)


def samples_by_race():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Continental Population Groups')
    organism_parts = UnificatedSamplesAttributeValue.objects.filter(unificated_name=organism_part)

    
    parts_dict = {}
    for part in organism_parts:
        parts_dict[part] = 0
    parts_dict["other"] = 0

    samples = total_samples()

    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            organism_part_value = SampleAttribute.objects.get(sample=sample, 
              unificated_name=organism_part).unificated_value
            # print(sample.experiment.data['accession'])
            parts_dict[organism_part_value]+=1
        else:
            parts_dict["other"]+=1

    print(parts_dict)


def stats():
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
    

















            

