from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

from articles.getdata import *

import xlrd


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
        delivery = UnificatedSamplesAttributeName.objects.get(name='Delivery, Obstetric')
        onset = UnificatedSamplesAttributeName.objects.get(name='Pre-Eclampsia Onset')
        biosource = UnificatedSamplesAttributeName.objects.get(name='biosource provider')
        sex = UnificatedSamplesAttributeName.objects.get(name='Fetus Sex')
        labor = UnificatedSamplesAttributeName.objects.get(name='Labor, Obstetric')
        batch = UnificatedSamplesAttributeName.objects.get(name='batch')
        age = UnificatedSamplesAttributeName.objects.get(name='Gestational Age')
        cultured = UnificatedSamplesAttributeName.objects.get(name='Cells, Cultured')
        fetal_weight = UnificatedSamplesAttributeName.objects.get(name='Fetal Weight')
        ancestry = UnificatedSamplesAttributeName.objects.get(name='Continental Population Groups')
        parity = UnificatedSamplesAttributeName.objects.get(name='Parity')
        gravidity = UnificatedSamplesAttributeName.objects.get(name='Gravidity')
        maternal_age =UnificatedSamplesAttributeName.objects.get(name='Maternal Age')
        excluded_name =UnificatedSamplesAttributeName.objects.get(name='(excluded)')






        humans = UnificatedSamplesAttributeValue.objects.get(value='Humans')
        mice = UnificatedSamplesAttributeValue.objects.get(value='Mice')
        pre_eclampsia = UnificatedSamplesAttributeValue.objects.get(value='Pre-Eclampsia')
        health = UnificatedSamplesAttributeValue.objects.get(value='Health')
        early_onset = UnificatedSamplesAttributeValue.objects.get(value='Early Onset Pre-Ecpampsia (at gestational age <31 weeks)')
        late_onset =  UnificatedSamplesAttributeValue.objects.get(value='Late Onset Pre-Eclampsia ( at gestational age >=31 weeks)')
        fgr = UnificatedSamplesAttributeValue.objects.get(value='Fetal Growth Retardation')
        pre_fgr = UnificatedSamplesAttributeValue.objects.get(value='pre-eclampsia and fgr')
        text = UnificatedSamplesAttributeValue.objects.get(value='Text Value')
        cytotrophoblast = UnificatedSamplesAttributeValue.objects.get(value='Cytotrophoblasts')
        syncitiotrophoblast = UnificatedSamplesAttributeValue.objects.get(value='Syncitiotrophoblasts')
        african = UnificatedSamplesAttributeValue.objects.get(value='African Continental Ancestry Group')
        american = UnificatedSamplesAttributeValue.objects.get(value='American Native Continental Ancestry Group')
        european = UnificatedSamplesAttributeValue.objects.get(value='European Continental Ancestry Group')
        asian = UnificatedSamplesAttributeValue.objects.get(value='Asian Continental Ancestry Group')
        hispanic = UnificatedSamplesAttributeValue.objects.get(value='Hispanic Americans')
        other = UnificatedSamplesAttributeValue.objects.get(value='Other')
        excluded_value = UnificatedSamplesAttributeValue.objects.get(value='(excluded)')
        term = UnificatedSamplesAttributeValue.objects.get(value='term')
        pretrem = UnificatedSamplesAttributeValue.objects.get(value='Obstetric Labor, Premature')
        





        decidua = UnificatedSamplesAttributeValue.objects.get(value='Decidua')
        placenta = UnificatedSamplesAttributeValue.objects.get(value='Placenta')

        female = UnificatedSamplesAttributeValue.objects.get(value='Female')
        male = UnificatedSamplesAttributeValue.objects.get(value='Male')

        spontaneous= UnificatedSamplesAttributeValue.objects.get(value='spontaneous')
        induced= UnificatedSamplesAttributeValue.objects.get(value='Labor, Induced')
        weeks = UnificatedSamplesAttributeValue.objects.get(value='Number in weeks')
        grams = UnificatedSamplesAttributeValue.objects.get(value='Number in grams')
        years = UnificatedSamplesAttributeValue.objects.get(value='Number in years')
        numeric = UnificatedSamplesAttributeValue.objects.get(value='Numeric')

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
            if SampleAttribute.filter(sample=sample,
                                      unificated_name=onset,
                                      unificated_value=early_onset).exists():
                add_or_replace_numeric(sample, age_avg, 31.7)
                add_or_replace_numeric(sample, age_dev, 3.28)
                print("late pre-eclampsia")

            elif SampleAttribute.filter(sample=sample,
                                      unificated_name=onset,
                                      unificated_value=late_onset).exists():
                add_or_replace_numeric(sample, age_avg, 38.14)
                add_or_replace_numeric(sample, age_dev, 1.36)
                print("early pre-eclampsia")

            else:
                name = SampleAttribute.get(sample=sample,
                                           unificated_name__name='name').old_value
        
                in_list = False
                for item in lst_late:
                    if name in item:
                        in_list = True

                if in_list:
                    add_or_replace_numeric(sample, age_avg, 40.63)
                    add_or_replace_numeric(sample, age_dev, 5.23)
                    print("early")

                in_list = False
                for item in lst_late:
                    if name in item:
                        in_list = True

                if in_list:
                    add_or_replace_numeric(sample, age_avg, 30.2)
                    add_or_replace_numeric(sample, age_dev, 2.1)
                    print("late")





                        







        
        










        





# Organism Part ['Chorionic Villi', 'Adipose Tissue', 'Decidua', 'Placenta', 'Trophoblasts']
# Maternal Age numeric
# Gravidity numeric
# Parity numeric
# Gestational Age numeric
# Gestational Age at time of Experiment numeric
# Diagnosis ['Health', 'Pre-Eclampsia', 'Fetal Growth Retardation']
# Pre-Eclampsia Onset ['Late Onset Pre-Eclampsia ( at gestational age >=31 weeks)', 'Early Onset Pre-Ecpampsia (at gestational age <31 weeks)']
# Classification ['Humans', 'Mice']
# Pregnancy Trimesters ['Pregnancy Trimester, Third', 'Pregnancy Trimester, Second', 'Pregnancy Trimester, First']
# Race ['Asian Continental Ancestry Group', 'Hispanic Americans', 'African Americans', 'European Continental Ancestry Group', 'Other']
# Labor, Obstetric ['vaginal', 'None']
# Delivery ['term', 'preterm']
# Cesarean Section ['True', 'False']

