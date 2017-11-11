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
        csection = StandardName.objects.get(name='Caesarean Section')


        humans = StandardValue.objects.get(value='Humans')
        mice = StandardValue.objects.get(value='Mice')
        pre_eclampsia = StandardValue.objects.get(value='Pre-Eclampsia')
        health = StandardValue.objects.get(value='Health')
        early_onset = StandardValue.objects.get(value='Early Onset Pre-Ecpampsia (at gestational age <31 weeks)')
        late_onset =  StandardValue.objects.get(value='Late Onset Pre-Eclampsia ( at gestational age >=31 weeks)')
        fgr = StandardValue.objects.get(value='Fetal Growth Retardation')
        pre_fgr = StandardValue.objects.get(value='pre-eclampsia and fgr')
        pre_hellp = StandardValue.objects.get(value='pre-eclampsia and hellp')
        text = StandardValue.objects.get(value='Text Value')
        cytotrophoblast = StandardValue.objects.get(value='Cytotrophoblasts')
        syncitiotrophoblast = StandardValue.objects.get(value='Syncitiotrophoblasts')
        tr = StandardValue.objects.get(value='True')
        fl = StandardValue.objects.get(value='False')
        vaginal = StandardValue.objects.get(value='vaginal')

        




        decidua = StandardValue.objects.get(value='Decidua')
        placenta = StandardValue.objects.get(value='Placenta')

        female = StandardValue.objects.get(value='Female')
        male = StandardValue.objects.get(value='Male')

        spontaneous= StandardValue.objects.get(value='spontaneous')
        induced= StandardValue.objects.get(value='Labor, Induced')
        weeks = StandardValue.objects.get(value='Number in weeks')
        grams = StandardValue.objects.get(value='Number in grams')

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