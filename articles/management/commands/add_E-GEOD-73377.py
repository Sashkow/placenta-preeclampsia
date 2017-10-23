from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

from articles.getdata import *

import xlrd


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        infant sex
              male
              female
        organism part
              decidua basalis
        parity
              
        maternal age yrs
              
        name
              
        gestational age wks
              
        organism
              Homo sapiens
        infant weight g
              
        gravidity
              
        subject status
              pre-eclamptic patient
              normotensive control patient

        """
        experiment_id = 'E-GEOD-73377'

        # exp_to_db(experiment_id)
        
        exp = Experiment.objects.get(data__contains={'accession':experiment_id})




        # exp.data['mail sent']
        # exp.save()

        organism = UnificatedSamplesAttributeName.objects.get(name='Classification')
        organism_part = UnificatedSamplesAttributeName.objects.get(name='Organism Part')
        diagnosis = UnificatedSamplesAttributeName.objects.get(name='Diagnosis')
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

        
        samples_in_experiment = exp.samples()
        
        # fetal sex female Fetus Sex None
        # maternal race Black Race None
        for sample in samples_in_experiment:
            current_race = SampleAttribute.objects.get(
              sample=sample,
              old_name='race')

            current_age = SampleAttribute.objects.get(
              sample=sample,
              old_name='gestational age')


            if current_race.old_value.isdigit():
                current_race.old_value, \
                 current_age.old_value = \
                   current_age.old_value, \
                    current_race.old_value
                current_race.save()
                current_age.save()



            SampleAttribute.unify(
              sample=sample,
              old_name='race',
              old_value='Caucasian',
              unificated_name=ancestry,
              unificated_value=european)

            SampleAttribute.unify(
              sample=sample,
              old_name='race',
              old_value='Other',
              unificated_name=ancestry,
              unificated_value=other)

            SampleAttribute.unify(
              sample=sample,
              old_name='race',
              old_value='Hispanic',
              unificated_name=ancestry,
              unificated_value=hispanic)

            SampleAttribute.unify(
              sample=sample,
              old_name='race',
              old_value='African American',
              unificated_name=ancestry,
              unificated_value=african)

            SampleAttribute.unify(
              sample=sample,
              old_name='race',
              old_value='Asian',
              unificated_name=ancestry,
              unificated_value=asian)

            SampleAttribute.unify(
              sample=sample,
              old_name='organism part',
              old_value='placenta',
              unificated_name=organism_part,
              unificated_value=placenta)

            
            SampleAttribute.unify_for_each_old_value(
              sample=sample,
              old_name='maternal age',

              unificated_name=maternal_age,
              unificated_value=years)

            SampleAttribute.unify_for_each_old_value(
              sample=sample,
              old_name='gestational age',

              unificated_name=age,
              unificated_value=weeks)

            SampleAttribute.unify(
              sample=sample,
              old_name='organism',
              old_value='Homo sapiens',
              unificated_name=organism,
              unificated_value=humans)

            SampleAttribute.unify(
              sample=sample,
              old_name='diagnosis',
              old_value='preeclamptic',
              unificated_name=diagnosis,
              unificated_value=pre_eclampsia)

            SampleAttribute.unify(
              sample=sample,
              old_name='diagnosis',
              old_value='normotensive',
              unificated_name=diagnosis,
              unificated_value=health)

            SampleAttribute.unify_name(sample=sample)



        # for attr in SampleAttribute.objects.filter(sample=twin_sample):
        #     attr.unificated_name = excluded_name
        #     attr.unificated_value = excluded_value
        #     attr.save()




















        





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
