from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

from articles.getdata import *

import xlrd


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        organism part
              Fused Cytotrophoblast cells (syncitiotrophoblast)
              Isolated Cytotrophoblast
        Organism
              Homo sapiens
        """
        experiment_id = 'E-GEOD-54618'

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
        csection = UnificatedSamplesAttributeName.objects.get(name='Caesarean Section')


        humans = UnificatedSamplesAttributeValue.objects.get(value='Humans')
        mice = UnificatedSamplesAttributeValue.objects.get(value='Mice')
        pre_eclampsia = UnificatedSamplesAttributeValue.objects.get(value='Pre-Eclampsia')
        health = UnificatedSamplesAttributeValue.objects.get(value='Health')
        early_onset = UnificatedSamplesAttributeValue.objects.get(value='Early Onset Pre-Ecpampsia (at gestational age <31 weeks)')
        late_onset =  UnificatedSamplesAttributeValue.objects.get(value='Late Onset Pre-Eclampsia ( at gestational age >=31 weeks)')
        fgr = UnificatedSamplesAttributeValue.objects.get(value='Fetal Growth Retardation')
        pre_fgr = UnificatedSamplesAttributeValue.objects.get(value='pre-eclampsia and fgr')
        pre_hellp = UnificatedSamplesAttributeValue.objects.get(value='pre-eclampsia and hellp')
        text = UnificatedSamplesAttributeValue.objects.get(value='Text Value')
        cytotrophoblast = UnificatedSamplesAttributeValue.objects.get(value='Cytotrophoblasts')
        syncitiotrophoblast = UnificatedSamplesAttributeValue.objects.get(value='Syncitiotrophoblasts')
        tr = UnificatedSamplesAttributeValue.objects.get(value='True')
        fl = UnificatedSamplesAttributeValue.objects.get(value='False')
        vaginal = UnificatedSamplesAttributeValue.objects.get(value='vaginal')

        




        decidua = UnificatedSamplesAttributeValue.objects.get(value='Decidua')
        placenta = UnificatedSamplesAttributeValue.objects.get(value='Placenta')

        female = UnificatedSamplesAttributeValue.objects.get(value='Female')
        male = UnificatedSamplesAttributeValue.objects.get(value='Male')

        spontaneous= UnificatedSamplesAttributeValue.objects.get(value='spontaneous')
        induced= UnificatedSamplesAttributeValue.objects.get(value='Labor, Induced')
        weeks = UnificatedSamplesAttributeValue.objects.get(value='Number in weeks')
        grams = UnificatedSamplesAttributeValue.objects.get(value='Number in grams')

        rb = xlrd.open_workbook('E-GEOD-54618.xls',formatting_info=True)
        sheet = rb.sheet_by_index(0)
        samples_in_experiment = exp.samples()
        for rownum in range(1, sheet.nrows):
            row = sheet.row_values(rownum)
            name = row[0]

            # Delivery by C section at 30 weeks + 2 days of gestation
            delivery_age = row[1]
            s = delivery_age[:]
            age_value = round(float(s[s.index('at')+3:s.index('at')+5]) + \
                        float(s[s.index('+')+2:s.index('+')+3])/7, 1)


            diag = row[2]
            
            
            sample = SampleAttribute.objects.get(
              sample__in=samples_in_experiment,
              old_value=name).sample

            if "C section" in delivery_age:
                SampleAttribute.add_or_replace(
                  sample=sample,
                  unificated_name=csection,
                  unificated_value=tr)

            if "Vaginal" in delivery_age:
                SampleAttribute.add_or_replace(
                  sample=sample,
                  unificated_name=labor,
                  unificated_value=vaginal)

            SampleAttribute.add_or_replace(
                  sample=sample,
                  old_name="gestational age",
                  old_value=age_value)

            SampleAttribute.unify_for_each_old_value(
              sample=sample,
              old_name="gestational age",
              unificated_name=age,
              unificated_value=weeks)

            if 'pregnancy complicated with preeclampsia and HELLP syndrome' in diag:
                SampleAttribute.add_or_replace(
                  sample=sample,
                  unificated_name=diagnosis,
                  unificated_value=pre_hellp)
            elif 'pregnancy complicated with preeclampsia' in diag:
                SampleAttribute.add_or_replace(
                  sample=sample,
                  unificated_name=diagnosis,
                  unificated_value=pre_eclampsia)
            elif 'normotensive pregnancy' in diag:
                SampleAttribute.add_or_replace(
                  sample=sample,
                  unificated_name=diagnosis,
                  unificated_value=health)














