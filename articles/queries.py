from articles.models import *


def sample_attribute_old_name_value():
    """
    for each sample attribute name print in which experiments it appears add
    which values it takes in those experiments
    """
    attributes = SampleAttribute.objects.all()

    names = attributes.order_by().values_list(
      'old_name', flat=True).distinct()

    with open("names_values.txt", "w") as text_file:
        for name in names:
            print(name, file=text_file)
            values = SampleAttribute.objects.filter(
              old_name=name).order_by().values_list(
                'old_value', flat=True).distinct()
            for value in values:
                print("     ", value, file=text_file)

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

    exps = []
    for exp in all_exps:
        if exp.data['accession'] in exp_ids:
            exps.append(exp)

    samples = Sample.objects.filter(experiment__in=exps)
    print(len(samples))
    #262
    print(len(Sample.objects.all()))
    return samples

def preeclampsia_samples():
    preeclampsia = UnificatedSamplesAttributeValue.objects.get(value='Pre-Eclampsia')
    preeclampsia_syn = UnificatedSamplesAttributeValue.objects.filter(
      synonyms__in=[preeclampsia])
    pre_syn_lst = list(preeclampsia_syn)
    pre_syn_lst.append(preeclampsia)
    samples = total_samples()
    pre_samples = []
    for sample in samples:
        #if the sample contains attribute value preeclampsia or synonym 
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_value__in=pre_syn_lst).exists():
            pre_samples.append(sample)
    print(pre_samples)
    print(len(pre_samples))
    #80


def health_samples():
    diagnosis = UnificatedSamplesAttributeName.objects.get(name='Diagnosis')
    health = UnificatedSamplesAttributeValue.objects.get(value='Health')
    
    samples = total_samples()
    pre_samples = []
    for sample in samples:
        #if the sample contains attribute diagnosis with value health
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=diagnosis,
          unificated_value=health).exists():
            pre_samples.append(sample)
    print(pre_samples)
    print(len(pre_samples))
    #107

def fgr_samples():
    diagnosis = UnificatedSamplesAttributeName.objects.get(name='Diagnosis')
    health = UnificatedSamplesAttributeValue.objects.get(value='Fetal Growth Retardation')
    
    samples = total_samples()
    pre_samples = []
    for sample in samples:
        #if the sample contains attribute diagnosis with value health
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=diagnosis,
          unificated_value=health).exists():
            pre_samples.append(sample)
    print(pre_samples)
    print(len(pre_samples))

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
            if not(SampleAttribute.objects.filter(sample=sample, unificated_name__name='Cells, Cultured').exists()):
                print(sample.experiment.data['accession'], sample.id)
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
            print(sample.experiment.data['accession'])
            parts_dict[organism_part_value]+=1
        else:
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
    samples = total_samples()
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
                print(sample.experiment.data['accession'], sample.id)
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
            print(sample.experiment.data['accession'])
            parts_dict[organism_part_value]+=1
        else:
            parts_dict["other"]+=1

    print(parts_dict)

def samples_by_gestation_age():
    cells_cultured = UnificatedSamplesAttributeName.objects.get(name='Cells, Cultured')
    trim = UnificatedSamplesAttributeName.objects.get(name='Pregnancy Trimesters')
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Gestational Age')
    organism_parts = UnificatedSamplesAttributeValue.objects.filter(unificated_name=organism_part)

    
    # parts_dict = {}
    # for part in organism_parts:
    #     parts_dict[part] = 0
    # parts_dict["other"] = 0
    total = 0
    tr = 0
    samples = total_samples()
    for sample in samples:
        if SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=organism_part).exists():
            # organism_part_value = SampleAttribute.objects.get(sample=sample, 
            #   unificated_name=organism_part).unificated_value
            print(sample.experiment.data['accession'])
            total+=1
        elif SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=trim).exists():
            tr += 1
        elif SampleAttribute.objects.filter(
          sample=sample,
          unificated_name=cells_cultured).exists():
            pass
        else:
            print(sample.experiment.data['accession'], sample.id)
    print(total,tr)


def samples_by_race():
    organism_part = UnificatedSamplesAttributeName.objects.get(name='Race')
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
            print(sample.experiment.data['accession'])
            parts_dict[organism_part_value]+=1
        else:
            parts_dict["other"]+=1

    print(parts_dict)
















            

