from django.core.management.base import BaseCommand, CommandError
from articles.getdata import *
from articles.models import Experiment, Microarray



class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        """
        """


        print("Receiving incomming transmission...")

        three_column_tsv_to_db()

        # print(SampleAttribute.objects.filter(old_value = "GSM594041_Cont_1_HuGene.1_0.st.v1_.CEL").first())


        # for sample in Experiment.find("E-GEOD-36083").samples():
        #     print("__")
        #     for attribute in sample.attributes():
        #         print(attribute)


        # for attribute in SampleAttribute.objects.filter(unificated_name__name='Scan Date'):
        #     print(attribute)




        # three_column_tsv_to_db()

        # exp = 'E-GEOD-25906'
        # exp_to_db(exp)
        # unify_exp(exp)

        # exps = Experiment.objects.all()
        #
        # exp_to_db(exps[2].data['accession'])

        # i=0
        # start = False
        # for exp in Experiment.objects.all():
        #     i+=1
        #     accession = exp.data['accession']
        #     if start == True:
        #         exp_to_db(accession)
        #     if accession == 'E-GEOD-25906':
        #         print('Skipping E-GEOD-25906')
        #         start= True
        # i = 0
        # for exp in Experiment.objects.all():
        #     i+=1
        #     accession = exp.data['accession']
        #     print(i, accession)
        #     exp_to_db(accession)






        # standard_name = StandardName.objects.get(name = 'Array Data File')
        # standard_value = StandardValue.objects.get(value = 'Text Value')

        # for attribute in SampleAttribute.objects.filter(old_name ='array data file'):
        #     print(attribute)
        #     attribute.unificated_name = standard_name
        #     attribute.unificated_value = standard_value
        #     attribute.save()

            # SampleAttribute.unify(
            #     sample=attribute.sample,
            #     old_name=attribute.old_name,
            #     old_value=attribute.old_value,
            #     unificated_name=standard_name,
            #     unificated_value=standard_value
            # )



        # experiment = Experiment.objects.get(data__contains = {'accession':exp})
        # samples=Sample.objects.filter(experiment=experiment)
        # for sample in samples:
        #     print(sample)
        #     attributes = SampleAttribute.objects.filter(sample=sample)
        #     for attribute in attributes:
        #         print("     ", attribute)

        
        # lst = get_placenta_accession()
        # experiment_id = lst[0]
        # # get_experiment_attributes(experiment_id)
        # print(get_experiment_samples_attributes(experiment_-``
        #