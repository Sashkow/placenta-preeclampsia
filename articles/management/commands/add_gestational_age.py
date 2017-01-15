from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

from articles.getdata import *

import xlrd

def add74341():
    exp_id = "E-GEOD-74341"
    # get experiment
    exp = Experiment.objects.get(data__contains={'accession':exp_id})
    # get samples for experiment 
    samples = Sample.objects.filter(experiment=exp)
    
    # get standard names, the rest are in the bottom
    age_avg = UnificatedSamplesAttributeName.objects.get(name="Average Gestational Age")
    age_dev = UnificatedSamplesAttributeName.objects.get(name="Deviation Gestational Age") 


    # 284.4 (267-321) 40.63  +- 5.23 
    # 211.4 196-225  30.2 +- 2.1  
    # 267 (258-277)  38.14 +- 1.36 
    # 222 (188-234)  31.7 +- 3.28 
    # control group consisted of control for first case (early onset preeclampsia)
    # and for the second one (late onset), but they both Healthy in our database  
    # so we search corresponding samples by id
    
    lst_late = ['GSM1917675', 'GSM1917676', 'GSM1917677', 'GSM1917678', 'GSM1917679']
    lst_early = ['GSM1917680','GSM1917681', 'GSM1917682', 'GSM1917683', 'GSM1917684']
    # for each sample in exp
    for sample in samples:
        # if there is attribute that belongs sample and
        # has name onset and value early onsetзна

        if SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=onset,
                                  unificated_value=early_onset).exists():
            # add or replace average age and deviation with corresponding values
            # add_or_replace_numeric is my function 

            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 31.7)
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 3.28) 
            print("early pre-eclampsia") 
        # the same for late onset
        elif SampleAttribute.objects.filter(sample=sample,
                                  unificated_name=onset,
                                  unificated_value=late_onset).exists():
            SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 38.14)
            SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 1.36)
            print("late pre-eclampsia")
        #if healthy
        else:
            # get sample name
            name = SampleAttribute.objects.get(sample=sample,
                                       unificated_name__name='name').old_value
            # check if name in one of the lst_late list's items
            in_list = False
            for item in lst_late:
                if item in name:
                    in_list = True 

            # if name in list of healthy1
            if in_list:
                SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 40.63)
                SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 5.23)
                print("late")

            in_list = False
            for item in lst_early:
                if item in name:
                    in_list = True

            # if name in list of healthy2
            if in_list:
                SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 30.2)
                SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 2.1)
                print("ear")


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

        trim =UnificatedSamplesAttributeName.objects.get(name='Pregnancy Trimesters')

        term_preterm =UnificatedSamplesAttributeName.objects.get(name='Gestation')


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

        trim1 = UnificatedSamplesAttributeValue.objects.get(value='Pregnancy Trimester, First')
        trim2 = UnificatedSamplesAttributeValue.objects.get(value='Pregnancy Trimester, Second')
        trim3 = UnificatedSamplesAttributeValue.objects.get(value='Pregnancy Trimester, Third')

        term = UnificatedSamplesAttributeValue.objects.get(value='Term Birth')
        preterm = UnificatedSamplesAttributeValue.objects.get(value='Premature Birth')

        
        # Healthy - 38.6 (35–41)
        # PE - 32.8 (22–40)
        categories = {
            "First Trimester":  0,
            "Second Trimester": 0,
            "Early Preterm":    0,
            "Late Preterm":     0,
            "Term":             0,
            "Unknown Age Category": 0
        }

        samples = total_samples()
        for sample in samples:
            category = sample.get_gestational_age_category()
            if category in categories:
                categories[category]+=1
                print(category)
            else:
                print("ha")
        print(categories)


            


        exp_id = "E-GEOD-74341"
        # get experiment
        exp = Experiment.objects.get(data__contains={'accession':exp_id})

        # get samples for experiment 
        samples = Sample.objects.filter(experiment=exp)
        
        # get standard names, the rest are in the bottom
        age_avg = UnificatedSamplesAttributeName.objects.get(name="Average Gestational Age")
        age_dev = UnificatedSamplesAttributeName.objects.get(name="Deviation Gestational Age") 




        # for sample in samples:
        #     attributes = sample.attributes()
        #     if not attributes.filter(sample=sample, unificated_name=age_avg).exists():
        #         print(sample)
        #         for attribute in attributes:
        #             print("     ", attribute)

        
        # 284.4 (267-321) 40.63  +- 5.23 
        # 211.4 196-225  30.2 +- 2.1  
        # 267 (258-277)  38.14 +- 1.36 
        # 222 (188-234)  31.7 +- 3.28 
        # control group consisted of control for first case (early onset preeclampsia)
        # and for the second one (late onset), but they both Healthy in our database  
        # so we search corresponding samples by id



        # SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 38.14)
        # SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 1.36)





        


        # lst_late = ['GSM1917675', 'GSM1917676', 'GSM1917677', 'GSM1917678', 'GSM1917679']
        # lst_early = ['GSM1917680','GSM1917681', 'GSM1917682', 'GSM1917683', 'GSM1917684']
        # for each sample in exp

        # for sample in samples:
        #     # if there is attribute that belongs sample and
        #     # has name onset and value early onsetзна

        #     if SampleAttribute.objects.filter(sample=sample,
        #                               unificated_name=onset,
        #                               unificated_value=early_onset).exists():
        #         # add or replace average age and deviation with corresponding values
        #         # add_or_replace_numeric is my function 

        #         SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 31.7)
        #         SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 3.28) 
        #         print("early pre-eclampsia") 
        #     # the same for late onset
        #     elif SampleAttribute.objects.filter(sample=sample,
        #                               unificated_name=onset,
        #                               unificated_value=late_onset).exists() or \
        #         SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 38.14)
        #         SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 1.36)
        #         print("late pre-eclampsia")
        #     #if healthy
        #     else:
        #         # get sample name
        #         name = SampleAttribute.objects.get(sample=sample,
        #                                    unificated_name__name='name').old_value
        #         # check if name in one of the lst_late list's items
        #         in_list = False
        #         for item in lst_late:
        #             if item in name:
        #                 in_list = True 

        #         # if name in list of healthy1
        #         if in_list:
        #             SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 40.63)
        #             SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 5.23)
        #             print("late")

        #         in_list = False
        #         for item in lst_early:
        #             if item in name:
        #                 in_list = True

        #         # if name in list of healthy2
        #         if in_list:
        #             SampleAttribute.add_or_replace_numeric(sample, age_avg, weeks, 30.2)
        #             SampleAttribute.add_or_replace_numeric(sample, age_dev, weeks, 2.1)
        #             print("ear")