from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

from articles.getdata import *


class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        DiseaseState
              infant SGA
              preeclampsia+infant SGA
              normal
              preeclampsia
        Organism
              Homo sapiens
        OrganismPart
              Decidua basalis
        BioSourceProvider
              Bergen
              Trondheim

        labor none

        """
        experiment_id = 'E-TABM-682'


        exp = Experiment.objects.get(data__contains={'accession':experiment_id})
        exp.data['mail sent']= 'true'
        exp.save()

        organism = UnificatedSamplesAttributeName.objects.get(name='Classification')
        organism_part = UnificatedSamplesAttributeName.objects.get(name='Organism Part')
        diagnosis = UnificatedSamplesAttributeName.objects.get(name='Diagnosis')
        onset = UnificatedSamplesAttributeName.objects.get(name='Pre-Eclampsia Onset')
        biosource = UnificatedSamplesAttributeName.objects.get(name='biosource provider')

        humans = UnificatedSamplesAttributeValue.objects.get(value='Humans')
        mice = UnificatedSamplesAttributeValue.objects.get(value='Mice')
        pre_eclampsia = UnificatedSamplesAttributeValue.objects.get(value='Pre-Eclampsia')
        health = UnificatedSamplesAttributeValue.objects.get(value='Health')
        early_onset = UnificatedSamplesAttributeValue.objects.get(value='Early Onset Pre-Ecpampsia (at gestational age <31 weeks)')
        late_onset =  UnificatedSamplesAttributeValue.objects.get(value='Late Onset Pre-Eclampsia ( at gestational age >=31 weeks)')
        fgr = UnificatedSamplesAttributeValue.objects.get(value='Fetal Growth Retardation')
        pre_fgr = UnificatedSamplesAttributeValue.objects.get(value='pre-eclampsia and fgr')
        text = UnificatedSamplesAttributeValue.objects.get(value='Text Value')

        decidua = UnificatedSamplesAttributeValue.objects.get(value='Decidua')
        placenta = UnificatedSamplesAttributeValue.objects.get(value='Placenta')


        for sample in Sample.objects.filter(experiment=exp):
            SampleAttribute.unify(
              sample=sample,
              old_name='DiseaseState',
              old_value='early onset preeclampsia',
              unificated_name=diagnosis,
              unificated_value=early_onset)

            SampleAttribute.unify(
              sample=sample,
              old_name='DiseaseState',
              old_value='normal',
              unificated_name=diagnosis,
              unificated_value=health)

            SampleAttribute.unify(
              sample=sample,
              old_name='DiseaseState',
              old_value='preeclampsia+infant SGA',
              unificated_name=diagnosis,
              unificated_value=pre_fgr)

            # SampleAttribute.unify(
            #   sample=sample,
            #   old_name='DiseaseState',
            #   old_value='late onset preeclampsia',
            #   unificated_name=diagnosis,
            #   unificated_value=late_onset)

            SampleAttribute.unify(
              sample=sample,
              old_name='DiseaseState',
              old_value='infant SGA',

              unificated_name=diagnosis,
              unificated_value=fgr)

            SampleAttribute.unify(
              sample=sample,
              old_name='DiseaseState',
              old_value='preeclampsia',
              unificated_name=diagnosis,
              unificated_value=pre_eclampsia)

            # SampleAttribute.unify(
            #   sample=sample,
            #   old_name='Organism',
            #   old_value='Mus musculus',
            #   unificated_name=organism,
            #   unificated_value=mice)

            SampleAttribute.unify(
              sample=sample,
              old_name='Organism',
              old_value='Homo sapiens',
              unificated_name=organism,
              unificated_value=humans)

            SampleAttribute.unify(
              sample=sample,
              old_name='OrganismPart',
              old_value='Decidua basalis',
              unificated_name=organism_part,
              unificated_value=decidua)

            SampleAttribute.unify(
              sample=sample,
              old_name='BioSourceProvider',
              old_value='Bergen',
              unificated_name=biosource,
              unificated_value=text)

            SampleAttribute.unify(
              sample=sample,
              old_name='BioSourceProvider',
              old_value='Trondheim',
              unificated_name=biosource,
              unificated_value=text)

            SampleAttribute.unify_name(
              sample=sample)


            SampleAttribute.add_or_replace(
              sample=sample,
              unificated_name=UnificatedSamplesAttributeName.objects.get(
                name='Labor, Obstetric'),
              unificated_value=UnificatedSamplesAttributeValue.objects.get(
                value='None'))

            if SampleAttribute.objects.filter(
              sample=sample,
              unificated_name=diagnosis,
              unificated_value=health).exists():
                SampleAttribute.add_or_replace(
                  sample=sample,
                  unificated_name=UnificatedSamplesAttributeName.objects.get(
                    name='Delivery, Obstetric'),
                  unificated_value=UnificatedSamplesAttributeValue.objects.get(
                    value='term'))
            else:
                SampleAttribute.add_or_replace(
                  sample=sample,
                  unificated_name=UnificatedSamplesAttributeName.objects.get(
                    name='Delivery, Obstetric'),
                  unificated_value=UnificatedSamplesAttributeValue.objects.get(
                    value='Premature Birth'))


            SampleAttribute.add_or_replace(
              sample=sample,
              unificated_name=UnificatedSamplesAttributeName.objects.get(
                name='Caesarean Section'),
              unificated_value=UnificatedSamplesAttributeValue.objects.get(
                value='True'))




















            




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