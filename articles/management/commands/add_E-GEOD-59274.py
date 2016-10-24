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
        experiment_id = 'E-GEOD-59274'

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
        




        decidua = UnificatedSamplesAttributeValue.objects.get(value='Decidua')
        placenta = UnificatedSamplesAttributeValue.objects.get(value='Placenta')

        female = UnificatedSamplesAttributeValue.objects.get(value='Female')
        male = UnificatedSamplesAttributeValue.objects.get(value='Male')

        spontaneous= UnificatedSamplesAttributeValue.objects.get(value='spontaneous')
        induced= UnificatedSamplesAttributeValue.objects.get(value='Labor, Induced')
        weeks = UnificatedSamplesAttributeValue.objects.get(value='Number in weeks')
        grams = UnificatedSamplesAttributeValue.objects.get(value='Number in grams')
        years = UnificatedSamplesAttributeValue.objects.get(value='Number in years')

        
        samples_in_experiment = exp.samples()
        
        # fetal sex female Fetus Sex None
        # maternal race Black Race None
        for sample in samples_in_experiment:

            SampleAttribute.unify(
              sample=sample,
              old_name='infant sex',
              old_value='female',
              unificated_name=sex,
              unificated_value=female)

            SampleAttribute.unify(
              sample=sample,
              old_name='infant sex',
              old_value='male',
              unificated_name=sex,
              unificated_value=male)

            SampleAttribute.unify(
              sample=sample,
              old_name='organism part',
              old_value='decidua basalis',
              unificated_name=organism_part,
              unificated_value=decidua)

            SampleAttribute.unify_for_each_old_value(
              sample=sample,
              old_name='parity',
              
              unificated_name=parity,
              unificated_value=numeric)

            SampleAttribute.unify_for_each_old_value(
              sample=sample,
              old_name='gravidity',

              unificated_name=gravidity,
              unificated_value=numeric)

            SampleAttribute.unify_for_each_old_value(
              sample=sample,
              old_name='maternal age yrs',

              unificated_name=maternal_age,
              unificated_value=years)

            SampleAttribute.unify_for_each_old_value(
              sample=sample,
              old_name='gestational age wks',

              unificated_name=age,
              unificated_value=weeks)

            SampleAttribute.unify(
              sample=sample,
              old_name='organism',
              old_value='Homo sapiens',
              unificated_name=organism,
              unificated_value=humans)

            SampleAttribute.unify_for_each_old_value(
              sample=sample,
              old_name='infant weight',

              unificated_name=weight,
              unificated_value=grams)

            SampleAttribute.unify(
              sample=sample,
              old_name='subject status',
              old_value='pre-eclamptic patient',
              unificated_name=diagnosis,
              unificated_value=pre_eclampsia)

            SampleAttribute.unify(
              sample=sample,
              old_name='subject status',
              old_value='normotensive control patient',
              unificated_name=diagnosis,
              unificated_value=health)














        





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
