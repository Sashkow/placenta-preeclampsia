
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