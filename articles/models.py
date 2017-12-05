from django.db import models
from django.utils import timezone

from django_hstore import hstore
from simple_history.models import HistoricalRecords

from django.utils.functional import cached_property

from django.db.models import Q



class ShowModel(models.Model):
    """
    Abstract class that overrides standard printed value for Model classes
    """
    to_show = 'name'

    def _show(self):
            if hasattr(self,self.to_show):
                return str(getattr(self, self.to_show))
            elif hasattr(self, 'id'):
                return str(getattr(self, 'id'))
            else:
                return str(self)

    def __unicode__(self):
        return self._show()
        
    def __str__(self):
        return self._show()

    class Meta:
        abstract = True


class Article(ShowModel):
    pass


class Attribute(ShowModel):
    attribute_names = ['title',
                       'geo_id', 'geo_link',
                       'arr_id', 'arr_link',
                       'platform', 
                       'samples']

    article = models.ForeignKey('Article')
    attribute_name = models.CharField(blank=True, max_length=200)
    attribute_value = models.CharField(blank=True, max_length=200)
    to_show = 'attribute_name'


class StandardName(ShowModel):
    """

    """
    name = models.CharField(max_length=255)
    additional_info = hstore.DictionaryField(db_index=True, blank=True, null=True)
    synonyms = models.ManyToManyField('self', symmetrical=False)
    to_show = 'name'

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)

    def save(self, *args, **kwargs):
        super(StandardName, self).save(*args, **kwargs)
        if not(ColumnOrder.objects.filter(unificated_name=self).exists()):
            ColumnOrder.objects.create(unificated_name=self)
        



class StandardValue(ShowModel):
    unificated_name = models.ForeignKey('StandardName')
    value = models.CharField(max_length=255)
    additional_info = hstore.DictionaryField(db_index=True, blank=True, null=True)
    synonyms = models.ManyToManyField('self', symmetrical=False)
    to_show = 'value'

    objects = hstore.HStoreManager()

    @staticmethod
    def autocomplete_search_fields():
        return "id__iexact", "value__icontains"


class Experiment(models.Model):

    must_have_attributes = ['accession', 'secondaryaccession',
     'name', 'releasedate', 'lastupdatedate',
    'samples']

    must_have_attributes_map = {
            'accession':'accession',
            'secondaryaccession':'secondary accession',
            'name':'name',
            'experimenttype':'experiment type',
            'releasedate':'release date',
            'lastupdatedate':'last update date',
            'samples':'samples'}



    extra_attributes = ['microarrays','status']

    data = hstore.DictionaryField(db_index=True)
    objects = hstore.HStoreManager()
    history = HistoricalRecords()
    samples = models.ManyToManyField('Sample')

    microarrays = models.ManyToManyField('Microarray')

    def find(exp):
        return Experiment.objects.filter(data__contains={'accession':exp}).first()

    def samples(self):
        return Sample.objects.filter(experiment=self)

    def sample_attributes(self):
        """get all attributes for all samples in experiment"""
        return SampleAttribute.objects.filter(sample__experiment=self)






    def __unicode__(self):
        to_print = 'accession'
        if to_print in self.data:
            return self.data[to_print]
        else:
            return 'some experiment'

    def __str__(self):
        to_print = 'accession'
        if to_print in self.data:
            # print("self data",type(self.data))
            return self.data[to_print]
        else:
            return 'some experiment'

    def to_dict(self, pretty_attributes = True):
        """
        Create dict of all meaningful characteristics of the Experiment
        """
        attributes = {}
        for attribute in self.must_have_attributes:
            if attribute in self.data:
                if pretty_attributes:
                    attributes[self.must_have_attributes_map[attribute]] = \
                            self.data[attribute]
                else:
                    attributes[attribute] = self.data[attribute]
        attributes['microarrays'] = self.get_microarrays_lst()
        attributes['status'] = self.cached_status()




        return attributes

    def to_list_of_dicts(pretty_attributes = True):
        exps = Experiment.objects.all()
        list_of_dicts = []
        for exp in exps:
            list_of_dicts.append(exp.to_dict(pretty_attributes))
        return list_of_dicts




    def add_or_replace(data):
        obj, some_bool = Experiment.objects.get_or_create(data__contains=
          {'accession':data['accession']})

        obj.data = data
        obj.save()
        return obj

    def get_microarrays_lst(self):
        lst = [m.data['name'] for m in self.microarrays.all()]
        return ', '.join(lst)



    def is_excluded(self):
        return 'excluded' in self.data

    def is_mail_received():
        return 'mail received' in self.data


    def is_unified(self):
        exp_samples = self.samples()
        has_empty_name = SampleAttribute.objects.filter(
          sample__in=exp_samples,
          unificated_name=None).exists()

        has_empty_value = SampleAttribute.objects.filter(
          sample__in=exp_samples,
          unificated_value=None).exists()
        if has_empty_name or has_empty_value:
            return False
        else:
            return True

    def set_has_minimal(self):
        if self.has_minimal():
            self.data['has minimal'] = 'true'
        else:
            self.data['has minimal'] = 'false'
        self.save()

    def get_has_minimal(self):
        if 'has minimal' in self.data:
            if self.data['has minimal'] == 'true':
                return True
            else:
                return False
        return False


    def has_minimal(self):
        """
        check whether experiment has minimal sample data,
        needed for sample comparison
        """
        # import time
        # timestart = time.time()
        # print(self, "start")

        bspecimen = StandardName.objects.get(name="Biological Specimen").id
        diagnosis = StandardName.objects.get(name="Diagnosis").id
        age = StandardName.objects.get(name="Gestational Age").id
        age_exp = StandardName.objects.get(name="Gestational Age at Time of Sampling").id
        age_avg = StandardName.objects.get(name="Average Gestational Age").id
        age_cat = StandardName.objects.get(name= "Gestational Age Category").id



        attributes = SampleAttribute.objects.filter(
                Q(unificated_name=bspecimen) |
                Q(unificated_name=diagnosis) |
                Q(unificated_name=age) |
                Q(unificated_name=age_avg) |
                Q(unificated_name=age_exp) |
                Q(unificated_name=age_cat)
        )

        # timeq1 = time.time()
        # print(timeq1-timestart)

        samples = self.samples()
        # timeq2 = time.time()
        # print(timeq2-timestart)



        for sample in samples:

            sample_attributes = attributes.filter(
                    sample=sample).values_list("unificated_name", flat=True)

            if not (bspecimen in sample_attributes and \
                    diagnosis in sample_attributes and \
                    (age in sample_attributes or
                    age_exp in sample_attributes or
                    age_avg in sample_attributes or
                    age_cat in sample_attributes)):
                for attr in sample_attributes:
                    print(StandardName.objects.get(id=attr))
                # timeq3 = time.time()
                # print(timeq3-timestart)
                # print("end-")
                return False

        # timeq3 = time.time()
        # print(timeq3-timestart)
        # print("end+")


        return True


    def is_cell_line(self):
        if SampleAttribute.objects.filter(
          sample__in=self.samples(),
          unificated_name__name="Cells, Cultured").exists():
            return True
        return False


    def status(self):
        status = []
        # if 'status' in self.data:
        #     status.append(self.data['status'])
        if self.is_unified():
            status.append('Unified')
        if 'mail sent' in self.data:
            status.append('Mail Sent')
        if 'mail received' in self.data:
            status.append('Mail Received')
        if self.is_cell_line():
            status.append('Cell Сulture')

        if self.has_minimal():
            status.append('Has minimal sample data')
        if 'excluded' in self.data:
            status.append('Excluded')
        return ", ".join(status)

    def update_status(self):
        self.data['status'] = self.status()
        self.save()

    def cached_status(self):
        if 'status' not in self.data:
            self.update_status()
        return self.data['status']



class Microarray(models.Model):
    must_have_attributes = ['accession', 'name']
    data = hstore.DictionaryField(db_index=True, blank=True)
    objects = hstore.HStoreManager()

    def _show(self):
        to_print = 'name'
        if to_print in self.data:
            return str(self.data[to_print])
        else:
            return str(self.id)

    def __unicode__(self):
        return self._show()

    def __str__(self):
        return self._show()

    def __repr__(self):
        return self._show()

    def add_or_replace(data):
        obj, some_bool = Microarray.objects.get_or_create(data__contains=
          {'accession':data['accession']})
        obj.data = data
        obj.save()
        return obj

    def to_dict(self):
        d = {}
        for item in Microarray.must_have_attributes:
            d[item] = str(self.data[item])
        return d

    def to_list_of_dicts():
        arrays = Microarray.objects.all()
        list_of_dicts = []
        for array in arrays:
            list_of_dicts.append(array.to_dict())
        return list_of_dicts


class Sample(models.Model):
    must_have_attributes = ['name']
    experiment = models.ForeignKey('Experiment', db_index=True)

    def _show(self):
        return str(self.id)

    def __unicode__(self):
        return self._show()

    def __str__(self):
        return self._show()

    def to_dict():
        """
        creates list of dicts for samples and sample attributes respectively
        """

        exps = Experiment.objects.all()
        exps = [exp for exp in exps if not exp.is_excluded()]
        samples = Sample.objects.filter(experiment__in=
                exps).select_related("experiment__data")

        attributes = SampleAttribute.objects.filter(sample__in=samples).values_list(
                'sample',
                'unificated_value__unificated_name__name',
                'unificated_name__name',
                'unificated_value__value',
                'old_value')



        # print(attributes)
        # print(samples)


        sample_dicts = {}

        for sample in samples:
            sample_dicts[str(sample.id)] = \
                    {'Experiment':str(sample.experiment)}

        # for sample in samples:
        #     sample_attributes = attributes.filter(sample=sample)
        #     print(sample_attributes)
        #     sample_dicts[str(sample.id)]['Gestational Age Category'] = \
        #             str(sample.get_gestational_age_category())



        for attribute in attributes:
            sample = str(attribute[0])
            # quantitative
            if attribute[1] == "Common" and attribute[3]!='True' and attribute[3]!='False':
                sample_dicts[sample].update(
                        {attribute[2] : \
                            str(attribute[4]) })
            # qualitative
            else:
                sample_dicts[sample].update(
                        {attribute[2] :
                        str(attribute[3])})


        list_of_dicts = []
        for sample_dict in sorted(sample_dicts):
            list_of_dicts.append(sample_dicts[sample_dict])

        # # merge average gestational age +- deviation
        # # into gestational age
        # for sample in list_of_dicts:
        #     if not 'Gestational Age' in sample:
        #         if 'Average Gestational Age' in sample and \
        #                 'Deviation Gestational Age' in sample:
        #             sample['Gestational Age'] = \
        #                     sample['Average Gestational Age'] + \
        #                     '+-' + \
        #                     sample['Deviation Gestational Age']



        # exclude None
        for d in list_of_dicts:
            to_delete =[]
            for item in d:
                if type(d[item])!=str:
                    d[item]=str(d[item])
                if type(item)!=str:
                    to_delete.append(item)
            for item in to_delete:
                del d[item]


        short_list_of_dicts=[]
        # for d in list_of_dicts:



        return list_of_dicts


    def attributes(self):
        return SampleAttribute.objects.filter(sample=self)

    def has_old_name(self, old_name):
        sample_attributes = SampleAttribute.objects.filter(
                            sample=self)
        name_attribute = sample_attributes.filter(old_name=old_name)
        return name_attribute.exists()

    def get_old_value(self, old_name):
        sample_attributes = SampleAttribute.objects.filter(
                            sample=self)
        name_attribute = sample_attributes.filter(
                         old_name=old_name)
        if name_attribute.exists():
            return name_attribute[0].old_value
        else:
            return None

    def get_gestational_age(self):

        """

        """
        attributes = self.attributes()

        age = attributes.filter(
          unificated_name__name='Gestational Age at Time of Sampling')
        if age.exists():
            return age[0].old_value

        age = attributes.filter(
          unificated_name__name='Gestational Age')
        if age.exists():
            return age[0].old_value

        age = attributes.filter(
          unificated_name__name='Average Gestational Age')
        if age.exists():
            return age[0].old_value

        return None

    def get_gestational_age_category(self):
        """
        since not all samples have exact Gestational Age value
        but sometimes only approximate ones it makes sence to
        introduce Age Category attribute of 5 possible values
            first Trimester
            second Trimester
            early preterm
            late preterm
            term
        since existing data on Gestational age suggests that
        """


        # 0 5 15 20 30 37 45 categories["Late Preterm"][0]
        categories = {
            "First Trimester":  [0,12],
            "Second Trimester": [12,20],
            "Early Preterm":    [20,30],
            "Late Preterm":     [30,37],
            "Term":             [37,42],
        }
        #get attributes for this sample
        # atributes = SampleAttribute.objects.filter(sample=self)
        # if exact age exists get exact age into variable
        age = self.get_gestational_age()

        if age:
            age = float(age)
            # print('gestational age:', age)
            for category in categories:
                if categories[category][0] <= age <= categories[category][1]:
                    return StandardValue.objects.get(value=category)
        else:
            attributes = self.attributes()
            gestation = attributes.filter(unificated_name__name = 'Gestation').first()
            if gestation:
                gestation_value = gestation.unificated_value.value
                if gestation_value == 'Premature Birth':
                    return StandardValue.objects.get(value='Late Preterm')
                else:
                    return StandardValue.objects.get(value='Term')



        return StandardValue.objects.get(
                    value="Unknown Gestational Category")

    def get_attribute_value(self, unificated_name):
        if SampleAttribute.objects.filter(
                sample=self,
                unificated_name__name=unificated_name).exists():
            attribute = SampleAttribute.objects.get(
                sample=self,
                unificated_name__name=unificated_name
            )
            if attribute.unificated_value.unificated_name.name == "Common":
                return attribute.old_value
            else:
                return attribute.unificated_value.value



    def add_or_replace(experiment, sample_data):
        """
        add or replace sample with given data in an experiment
        """
        sample_obj = None
        if 'name' in sample_data:
            samples_in_experiment = Sample.objects.filter(
                                      experiment=experiment)
            name_attribute = SampleAttribute.objects.filter(
                    sample__in=samples_in_experiment,
                    old_name='name',
                    old_value=sample_data['name'])

            if len(name_attribute) > 1:
                print("Multiple instances of", sample_data['name'], "in", experiment)
                return

            elif len(name_attribute) == 1:
                sample_obj = name_attribute[0].sample
            elif not name_attribute:
                sample_obj = Sample.objects.create(experiment=experiment)

            for old_name, old_value in sample_data.items():
                if old_value == None or old_value == '':
                    SampleAttribute.add_or_replace(sample_obj, old_name, '<empty>')
                else:
                    SampleAttribute.add_or_replace(sample_obj, old_name, old_value)

            sample_obj.save()
            return sample_obj


    # def _show(self):
    #     to_print = 'name'
    #     if to_print in self.data:
    #         return str(self.data[to_print])
    #     else:
    #         return str(self.id)

    # def __unicode__(self):
    #     return self._show()

    # def __str__(self):
    #     return self._show()


class SampleAttribute(models.Model):
    old_name = models.CharField(max_length=255, blank=True, null=True)
    old_value = models.CharField(max_length=255, blank=True, null=True)

    # standard attribute name according to MeSH terms or other ontologies
    unificated_name = models.ForeignKey('StandardName',
                                        blank=True,
                                        null=True,
                                        db_index=True)
    unificated_value = models.ForeignKey('StandardValue',
                                         blank=True,
                                         null=True)
    sample = models.ForeignKey('Sample', db_index=True)

    def _show(self):
        return " | ".join((
                        str(self.old_name),
                        str(self.old_value),
                        str(self.unificated_name),
                        str(self.unificated_value),
                        ))

    def __unicode__(self):
        return self._show()

    def __str__(self):
        return self._show()

    def unify(sample, old_name, old_value, unificated_name, unificated_value):
        attribute = SampleAttribute.objects.filter(
          sample=sample,
          old_name=old_name,
          old_value=old_value)

        if attribute.exists():
            if len(attribute)>1:
                print("attribute duplicates in sample", sample)
                return
            attribute = attribute[0]
            attribute.unificated_name = unificated_name
            attribute.unificated_value = unificated_value
            attribute.save()
        else:
            print("no such attribute",sample,old_name,old_value)
            return

    def unify_for_each_old_value(sample, old_name, unificated_name, unificated_value):

        attribute = SampleAttribute.objects.filter(
          sample=sample,
          old_name=old_name)

        if attribute.exists():
            if len(attribute)>1:
                print("attribute duplicates in sample", sample)
                return
            attribute = attribute[0]
            attribute.unificated_name = unificated_name
            attribute.unificated_value = unificated_value
            attribute.save()
        else:
            # print("no such attribute",sample,old_name,old_value)
            return

    def unify_name(sample):
        attribute = SampleAttribute.objects.filter(
          sample=sample, old_name='name')

        if attribute.exists():
            if len(attribute)>1:
                print("attribute duplicates in sample", sample)
                return
            attribute = attribute[0]
            attribute.unificated_name =  \
                    StandardName.objects.get(name='name')
            attribute.unificated_value = \
                    StandardValue.objects.get(value='Text Value')
            attribute.save()
        else:
            # print("no such attribute",sample,old_name,old_value)
            return

    def add_or_replace(sample,
                       old_name=None,
                       old_value=None,
                       unificated_name=None,
                       unificated_value=None):
        """
        sample - sample object
        """
        if not (old_name or unificated_name) or not (old_value or unificated_value):
            print("Not enough data for attribute add_or_replace")
            return

        if old_name:
            search = {'sample':sample,
                      'old_name':old_name}
            create = search.copy()
        elif unificated_name:
            search = {'sample':sample,
                      'unificated_name':unificated_name}
            create = search.copy()

        if old_value:
            create['old_value'] = old_value
            value_name = "old_value"
            value = old_value
        elif unificated_value:
            create['unificated_value'] = unificated_value
            value_name = "unificated_value"
            value = unificated_value

        attribute = SampleAttribute.objects.filter(**search)

        if attribute.exists():
            if len(attribute) == 1:
                attribute_obj = attribute[0]
                setattr(attribute_obj, value_name, value)
                print("Replacing", value_name, "with", value, "in attribute:", attribute_obj, "in sample:", sample)
            else:
                print("Multiple replace spots in", sample, "Retrun None")
                return
        else:

            attribute_obj = SampleAttribute.objects.create(**create)
            print("Creating new attribute", create, "in sample:", sample)
        attribute_obj.save()
        return attribute_obj


    def add_or_replace_numeric(sample, unificated_name, unificated_value, old_value):
        """
        add or replace quantitative attributes for a given sample
        """
        # try to find attribute of given name e.g. Average Gestational Age
        attribute = SampleAttribute.objects.filter(sample=sample,
                                                   unificated_name=unificated_name)
        # if it exists
        if attribute.exists():

            # get first element as .filter() method returns list
            attribute_obj = attribute[0]
            # set old_value to a new old_value
            attribute_obj.old_value = old_value
            attribute_obj.unificated_value = unificated_value

        else:
            # if not found, create new attribute of given properties
            attribute_obj = SampleAttribute.objects.create(
                    sample=sample,
                    unificated_name=unificated_name,
                    unificated_value=unificated_value,
                    old_value=old_value)
        attribute_obj.save() # very important! save to database


class ColumnOrder(models.Model):
    unificated_name = models.ForeignKey('StandardName')
    column_order = models.IntegerField(default=99)
    show_by_default = models.BooleanField(default=False)
    show_at_all = models.BooleanField(default=True)




