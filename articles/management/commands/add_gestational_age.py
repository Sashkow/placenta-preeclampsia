from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

from articles.getdata import *

import xlrd

def add74341():
    exp_id = "E-GEOD-74341"
    exp = Experiment.objects.get(data__contains={'accession':exp_id})
    samples = Sample.objects.filter(experiment=exp)
    
    age_avg = UnificatedSamplesAttributeName.objects.get(name="Average Gestational Age")
    age_dev = UnificatedSamplesAttributeName.objects.get(name="Deviation Gestational Age") 



    # 284.4 (267-321) 40.63  +- 5.23
    # 211.4 196-225  30.2 +- 2.1 
    # 267 (258-277)  38.14 +- 1.36
    # 222 (188-234)  31.7 +- 3.28

    lst_late = ['GSM1917675', 'GSM1917676', 'GSM1917677', 'GSM1917678', 'GSM1917679']
    lst_early = ['GSM1917680','GSM1917681', 'GSM1917682', 'GSM1917683', 'GSM1917684']

    for sample in samples:
        if SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=onset,
                                  unificated_value=early_onset).exists():
            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 31.7)
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 3.28)
            print("late pre-eclampsia")

        elif SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=onset,
                                  unificated_value=late_onset).exists():
            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 38.14)
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 1.36)
            print("early pre-eclampsia")

        else:
            name = SampleAttribute.objects.get(sample=sample,
                                       unificated_name__name='name').old_value
            
            in_list = False
            for item in lst_late:
                if item in name:
                    in_list = True

            if in_list:
                SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 40.63)
                SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 5.23)
                print("early")

            in_list = False
            for item in lst_early:
                if item in name:
                    in_list = True

            if in_list:
                SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 30.2)
                SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 2.1)
                print("late")

def add30186():

    exp_id = "E-GEOD-30186"
    exp = Experiment.objects.get(data__contains={'accession':exp_id})
    samples = Sample.objects.filter(experiment=exp)
    
    age_avg = UnificatedSamplesAttributeName.objects.get(name="Average Gestational Age")
    age_dev = UnificatedSamplesAttributeName.objects.get(name="Deviation Gestational Age") 


    # 273 5
    # 255 6

    print("start:")
    for sample in samples:
        if SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=diagnosis,
                                  unificated_value=health).exists():
            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 39)
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, round(5.0/7,2))
            print("late pre-eclampsia")

        elif SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=diagnosis,
                                  unificated_value=pre_eclampsia).exists():
            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, round(255.0/7,2))
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, round(6.0/7,2))
            print("early pre-eclampsia")


def add4707():

    exp_id = "E-GEOD-4707"
    exp = Experiment.objects.get(data__contains={'accession':exp_id})
    samples = Sample.objects.filter(experiment=exp)
    
    age_avg = UnificatedSamplesAttributeName.objects.get(name="Average Gestational Age")
    age_dev = UnificatedSamplesAttributeName.objects.get(name="Deviation Gestational Age") 

    # 32.9  5.6
    # 32.9  4.0

    print("start:")

    for sample in samples:

        if SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=diagnosis,
                                  unificated_value=health).exists():
            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 32.9)
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 5.6)
            print("health")

        elif SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=diagnosis,
                                  unificated_value=pre_severe).exists():
            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 32.9)
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 4.0)
            print("pre")
        else:
            print(SampleAttribute.objects.get(sample=sample, unificated_name=diagnosis))


def add12216():

    exp_id = "E-GEOD-12216"
    exp = Experiment.objects.get(data__contains={'accession':exp_id})
    samples = Sample.objects.filter(experiment=exp)
    
    age_avg = UnificatedSamplesAttributeName.objects.get(name="Average Gestational Age")
    age_dev = UnificatedSamplesAttributeName.objects.get(name="Deviation Gestational Age") 

    # 236 + 24
    # 274 + 5

    print("start:")

    for sample in samples:

        if SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=diagnosis,
                                  unificated_value=fgr).exists():
            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, round(236.0/7,2))
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, round(24/7,2))
            print("fgr")

        elif SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=diagnosis,
                                  unificated_value=health).exists():
            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, round(274/7,2))
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, round(5/7,2))
            print("health")
        else:
            print(SampleAttribute.objects.get(sample=sample, unificated_name=diagnosis))
class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        subject status
              patients with late-onset (>36 weeks) preeclampsia (LOPE)
              controls who delivered preterm (<34 weeks)
              controls who delivered at term (>36 weeks)
              patients with early-onset (<34 weeks) preeclampsia (EOPE)

        """
        
        # organism = UnificatedSamplesAttributeName.objects.get(name='Classification')
        # organism_part = UnificatedSamplesAttributeName.objects.get(name='Organism Part')
        diagnosis = UnificatedSamplesAttributeName.objects.get(name='Diagnosis')
        # delivery = UnificatedSamplesAttributeName.objects.get(name='Delivery, Obstetric')
        onset = UnificatedSamplesAttributeName.objects.get(name='Pre-Eclampsia Onset')
        # biosource = UnificatedSamplesAttributeName.objects.get(name='biosource provider')
        sex = UnificatedSamplesAttributeName.objects.get(name='Fetus Sex')
        labor = UnificatedSamplesAttributeName.objects.get(name='Labor, Obstetric')
        batch = UnificatedSamplesAttributeName.objects.get(name='Batch')
        age = UnificatedSamplesAttributeName.objects.get(name='Gestational Age')
        cultured = UnificatedSamplesAttributeName.objects.get(name='Cells, Cultured')
        fetal_weight = UnificatedSamplesAttributeName.objects.get(name='Fetal Weight')
        ancestry = UnificatedSamplesAttributeName.objects.get(name='Continental Population Groups')
        parity = UnificatedSamplesAttributeName.objects.get(name='Parity')
        gravidity = UnificatedSamplesAttributeName.objects.get(name='Gravidity')
        maternal_age =UnificatedSamplesAttributeName.objects.get(name='Maternal Age')
        excluded_name =UnificatedSamplesAttributeName.objects.get(name='(excluded)')

        humans = UnificatedSamplesAttributeValue.objects.get(value='Humans')
        # mice = UnificatedSamplesAttributeValue.objects.get(value='Mice')
        pre_eclampsia = UnificatedSamplesAttributeValue.objects.get(value='Pre-Eclampsia')
        pre_severe = UnificatedSamplesAttributeValue.objects.get(value='Severe Pre-Eclampsia')
        health = UnificatedSamplesAttributeValue.objects.get(value='Healthy')
        early_onset = UnificatedSamplesAttributeValue.objects.get(value='Early Onset Pre-Ecpampsia (at gestational age <31 weeks)')
        late_onset =  UnificatedSamplesAttributeValue.objects.get(value='Late Onset Pre-Eclampsia ( at gestational age >=31 weeks)')
        fgr = UnificatedSamplesAttributeValue.objects.get(value='Fetal Growth Retardation')
        
        text = UnificatedSamplesAttributeValue.objects.get(value='Text Value')
        cytotrophoblast = UnificatedSamplesAttributeValue.objects.get(value='Cytotrophoblasts')
        syncitiotrophoblast = UnificatedSamplesAttributeValue.objects.get(value='Syncitiotrophoblasts')
        african = UnificatedSamplesAttributeValue.objects.get(value='African Continental Ancestry Group')
        american = UnificatedSamplesAttributeValue.objects.get(value='American Native Continental Ancestry Group')
        european = UnificatedSamplesAttributeValue.objects.get(value='European Continental Ancestry Group')
        asian = UnificatedSamplesAttributeValue.objects.get(value='Asian Continental Ancestry Group')
        hispanic = UnificatedSamplesAttributeValue.objects.get(value='Hispanic Americans')
        
        excluded_value = UnificatedSamplesAttributeValue.objects.get(value='(excluded)')
        
        decidua = UnificatedSamplesAttributeValue.objects.get(value='Decidua')
        placenta = UnificatedSamplesAttributeValue.objects.get(value='Placenta')

        female = UnificatedSamplesAttributeValue.objects.get(value='Female')
        male = UnificatedSamplesAttributeValue.objects.get(value='Male')

        weeks = UnificatedSamplesAttributeValue.objects.get(value='Number in weeks')
        grams = UnificatedSamplesAttributeValue.objects.get(value='Number in grams')
        years = UnificatedSamplesAttributeValue.objects.get(value='Number in years')
        numeric = UnificatedSamplesAttributeValue.objects.get(value='Numeric')

        exp_id = "E-GEOD-24129"
        exp = Experiment.objects.get(data__contains={'accession':exp_id})
        samples = Sample.objects.filter(experiment=exp)
        
        age_avg = UnificatedSamplesAttributeName.objects.get(name="Average Gestational Age")
        age_dev = UnificatedSamplesAttributeName.objects.get(name="Deviation Gestational Age") 

        # 38.1 ± 0.8  37.3 ± 1.0  34.4 ± 1.8  

        print("start:")

        for sample in samples:

            if SampleAttribute.objects.filter(sample=sample,
                                      unificated_name=diagnosis,
                                      unificated_value=health).exists():
                SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 38.1)
                SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 0.8)
                print("controls")

            elif SampleAttribute.objects.filter(sample=sample,
                                      unificated_name=diagnosis,
                                      unificated_value=fgr).exists():
                SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 37.3)
                SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 1.0)
                print("fgr")
            elif SampleAttribute.objects.filter(sample=sample,
                                      unificated_name=diagnosis,
                                      unificated_value=pre_severe).exists():
                SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 34.4)
                SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 1.8)
                print("pre")
            else:
                print(SampleAttribute.objects.get(sample=sample, unificated_name=diagnosis))