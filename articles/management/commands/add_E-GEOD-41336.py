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

        organism = UnificatedSamplesAttributeName.objects.get(name='Classification')
        organism_part = UnificatedSamplesAttributeName.objects.get(name='Organism Part')
        diagnosis = UnificatedSamplesAttributeName.objects.get(name='Diagnosis')
        onset = UnificatedSamplesAttributeName.objects.get(name='Pre-Eclampsia Onset')
        biosource = UnificatedSamplesAttributeName.objects.get(name='biosource provider')
        sex = UnificatedSamplesAttributeName.objects.get(name='Sex')
        labor = UnificatedSamplesAttributeName.objects.get(name='Labor, Obstetric')
        batch = UnificatedSamplesAttributeName.objects.get(name='batch')
        age = UnificatedSamplesAttributeName.objects.get(name='Gestational Age')
        cultured = UnificatedSamplesAttributeName.objects.get(name='Cells, Cultured')


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



        decidua = UnificatedSamplesAttributeValue.objects.get(value='Decidua')
        placenta = UnificatedSamplesAttributeValue.objects.get(value='Placenta')

        female = UnificatedSamplesAttributeValue.objects.get(value='Female')
        male = UnificatedSamplesAttributeValue.objects.get(value='Male')

        spontaneous= UnificatedSamplesAttributeValue.objects.get(value='spontaneous')
        induced= UnificatedSamplesAttributeValue.objects.get(value='Labor, Induced')
        weeks = UnificatedSamplesAttributeValue.objects.get(value='Number in weeks')


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
            #       unificated_name=UnificatedSamplesAttributeName.objects.get(
            #         name='Delivery, Obstetric'),
            #       unificated_value=UnificatedSamplesAttributeValue.objects.get(
            #         value='term'))
            # else:
            #     SampleAttribute.add_or_replace(
            #       sample=sample,
            #       unificated_name=UnificatedSamplesAttributeName.objects.get(
            #         name='Delivery, Obstetric'),
            #       unificated_value=UnificatedSamplesAttributeValue.objects.get(
            #         value='Premature Birth'))


            # SampleAttribute.add_or_replace(
            #   sample=sample,
            #   unificated_name=UnificatedSamplesAttributeName.objects.get(
            #     name='Caesarean Section'),
            #   unificated_value=UnificatedSamplesAttributeValue.objects.get(
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