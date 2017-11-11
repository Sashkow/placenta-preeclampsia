from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

from articles.getdata import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        organism part
              Fused Cytotrophoblast cells (syncitiotrophoblast)
              Isolated Cytotrophoblast
        Organism
              Homo sapiens
        """
        experiment_id = 'E-GEOD-41336'


        exp = Experiment.objects.get(data__contains={'accession':experiment_id})
        # exp.data['mail sent']
        # exp.save()

        organism = StandardName.objects.get(name='Classification')
        organism_part = StandardName.objects.get(name='Organism Part')
        diagnosis = StandardName.objects.get(name='Diagnosis')
        onset = StandardName.objects.get(name='Pre-Eclampsia Onset')
        biosource = StandardName.objects.get(name='biosource provider')
        sex = StandardName.objects.get(name='Sex')
        labor = StandardName.objects.get(name='Labor, Obstetric')
        batch = StandardName.objects.get(name='batch')
        age = StandardName.objects.get(name='Gestational Age')
        cultured = StandardName.objects.get(name='Cells, Cultured')


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



        decidua = StandardValue.objects.get(value='Decidua')
        placenta = StandardValue.objects.get(value='Placenta')

        female = StandardValue.objects.get(value='Female')
        male = StandardValue.objects.get(value='Male')

        spontaneous= StandardValue.objects.get(value='spontaneous')
        induced= StandardValue.objects.get(value='Labor, Induced')
        weeks = StandardValue.objects.get(value='Number in weeks')


        for sample in Sample.objects.filter(experiment=exp):
            SampleAttribute.unify(
              sample=sample,
              old_name='organism part',
              old_value='Fused Cytotrophoblast cells (syncitiotrophoblast)',
              unificated_name=cultured,
              unificated_value=syncitiotrophoblast)

            SampleAttribute.unify(
              sample=sample,
              old_name='organism part',
              old_value='Isolated Cytotrophoblast',
              unificated_name=cultured,
              unificated_value=cytotrophoblast)

            SampleAttribute.unify(
              sample=sample,
              old_name='Organism',
              old_value='Homo sapiens',
              unificated_name=organism,
              unificated_value=humans)
          
            SampleAttribute.unify_name(
              sample=sample)

            # if SampleAttribute.objects.filter(
            #   sample=sample,
            #   unificated_name=diagnosis,
            #   unificated_value=health).exists():
            #     SampleAttribute.add_or_replace(
            #       sample=sample,
            #       unificated_name=StandardName.objects.get(
            #         name='Delivery, Obstetric'),
            #       unificated_value=StandardValue.objects.get(
            #         value='term'))
            # else:
            #     SampleAttribute.add_or_replace(
            #       sample=sample,
            #       unificated_name=StandardName.objects.get(
            #         name='Delivery, Obstetric'),
            #       unificated_value=StandardValue.objects.get(
            #         value='Premature Birth'))


            # SampleAttribute.add_or_replace(
            #   sample=sample,
            #   unificated_name=StandardName.objects.get(
            #     name='Caesarean Section'),
            #   unificated_value=StandardValue.objects.get(
            #     value='True'))


















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