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

        organism = StandardName.objects.get(name='Classification')
        organism_part = StandardName.objects.get(name='Organism Part')
        diagnosis = StandardName.objects.get(name='Diagnosis')
        onset = StandardName.objects.get(name='Pre-Eclampsia Onset')
        biosource = StandardName.objects.get(name='biosource provider')
        sex = StandardName.objects.get(name='Fetus Sex')
        labor = StandardName.objects.get(name='Labor, Obstetric')
        batch = StandardName.objects.get(name='batch')
        age = StandardName.objects.get(name='Gestational Age')
        cultured = StandardName.objects.get(name='Cells, Cultured')
        fetal_weight = StandardName.objects.get(name='Fetal Weight')
        ancestry = StandardName.objects.get(name='Continental Population Groups')
        parity = StandardName.objects.get(name='Parity')
        gravidity = StandardName.objects.get(name='Gravidity')
        maternal_age =StandardName.objects.get(name='Maternal Age')




        humans = StandardValue.objects.get(value='Humans')
        mice = StandardValue.objects.get(value='Mice')
        pre_eclampsia = StandardValue.objects.get(value='Pre-Eclampsia')
        health = StandardValue.objects.get(value='Health')
        early_onset = StandardValue.objects.get(value='Early Onset Pre-Ecpampsia (at gestational age <31 weeks)')
        late_onset =  StandardValue.objects.get(value='Late Onset Pre-Eclampsia ( at gestational age >=31 weeks)')
        fgr = StandardValue.objects.get(value='Fetal Growth Retardation')
        pre_fgr = StandardValue.objects.get(value='pre-eclampsia and fgr')
        text = StandardValue.objects.get(value='Text Value')
        cytotrophoblast = StandardValue.objects.get(value='Cytotrophoblasts')
        syncitiotrophoblast = StandardValue.objects.get(value='Syncitiotrophoblasts')
        african = StandardValue.objects.get(value='African Continental Ancestry Group')
        american = StandardValue.objects.get(value='American Native Continental Ancestry Group')
        




        decidua = StandardValue.objects.get(value='Decidua')
        placenta = StandardValue.objects.get(value='Placenta')

        female = StandardValue.objects.get(value='Female')
        male = StandardValue.objects.get(value='Male')

        spontaneous= StandardValue.objects.get(value='spontaneous')
        induced= StandardValue.objects.get(value='Labor, Induced')
        weeks = StandardValue.objects.get(value='Number in weeks')
        grams = StandardValue.objects.get(value='Number in grams')
        years = StandardValue.objects.get(value='Number in years')

        
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
