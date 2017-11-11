from django.core.management.base import BaseCommand, CommandError
from articles.queries import *
from articles.models import *

def replace_csection():
    """
    find all Samples that contain SampleAttributes with both
    Caesarean Section (True) and and Labor, Obstetric (None)
    delete Caesarean section, replace None with Caesarean Section
    """
    csection = StandardName.objects.get(name='Caesarean Section')
    csection_val = StandardValue.objects.get(value='Caesarean Section')
    tru = StandardValue.objects.get(value='True')
    labor = StandardName.objects.get(name='Labor, Obstetric')
    non = StandardValue.objects.get(value='None')
    count = 0
    for sample in Sample.objects.all():
        attributes = sample.attributes()

        if attributes.filter(unificated_name=csection, unificated_value=tru).exists() and \
          attributes.filter(unificated_name=labor, unificated_value=non).exists():
            print("here")
            SampleAttribute.add_or_replace(
              sample,
              unificated_name=labor,
              unificated_value=csection_val)
            SampleAttribute.objects.get(
              sample=sample,
              unificated_name=csection,
              unificated_value=tru).delete()

def replace_csection2():
    """
    almost as replace_csection
    """
    csection = StandardName.objects.get(name='Caesarean Section')
    csection_val = StandardValue.objects.get(value='Caesarean Section')
    tru = StandardValue.objects.get(value='True')
    labor = StandardName.objects.get(name='Labor, Obstetric')
    non = StandardValue.objects.get(value='None')
    count = 0
    for sample in Sample.objects.all():
        attributes = sample.attributes()

        if attributes.filter(unificated_name=csection, unificated_value=tru).exists():
            # if attributes.filter(unificated_name=labor).exists():
            #     SampleAttribute.objects.get(
            #       sample=sample,
            #       unificated_name=csection,
            #       unificated_value=tru).delete()
            # else:
            #     SampleAttribute.objects.get(
            #       sample=sample,
            #       unificated_name=csection,
            #       unificated_value=tru).delete()
            #     SampleAttribute.add_or_replace(
            #       sample,
            #       unificated_name=labor,
            #       unificated_value=csection_val)

            print("here")
            # print(sample, attributes.filter(unificated_name=labor))

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        command's hande method
        """        
        replace_csection2()

