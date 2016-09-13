from articles.models import *


def sample_attribute_name_experiment_value():
    """
    for each sample attribute name print in which experiments it appears add
    which values it takes in those experiments
    """
    attributes = SampleAttribute.objects.all()

    names = attributes.order_by().values_list(
      'old_name', flat=True).distinct()

    with open("names_values.txt", "w") as text_file:
        for name in names:
            print(name, file=text_file)
            values = SampleAttribute.objects.filter(
              old_name=name).order_by().values_list(
                'old_value', flat=True).distinct()
            for value in values:
                print("     ", value, file=text_file)
            

