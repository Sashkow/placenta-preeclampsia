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
        excluded_name =StandardName.objects.get(name='(excluded)')





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
        european = StandardValue.objects.get(value='European Continental Ancestry Group')
        asian = StandardValue.objects.get(value='Asian Continental Ancestry Group')
        hispanic = StandardValue.objects.get(value='Hispanic Americans')
        other = StandardValue.objects.get(value='Other')
        excluded_value = StandardValue.objects.get(value='(excluded)')
        





        decidua = StandardValue.objects.get(value='Decidua')
        placenta = StandardValue.objects.get(value='Placenta')

        female = StandardValue.objects.get(value='Female')
        male = StandardValue.objects.get(value='Male')

        spontaneous= StandardValue.objects.get(value='spontaneous')
        induced= StandardValue.objects.get(value='Labor, Induced')
        weeks = StandardValue.objects.get(value='Number in weeks')
        grams = StandardValue.objects.get(value='Number in grams')
        years = StandardValue.objects.get(value='Number in years')
        numeric = StandardValue.objects.get(value='Numeric')

        
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
