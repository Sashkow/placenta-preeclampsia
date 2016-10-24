from django.db import models
from django.utils import timezone

from django_hstore import hstore
from simple_history.models import HistoricalRecords


class ShowModel(models.Model):
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

    
class UnificatedSamplesAttributeName(ShowModel):
    name = models.CharField(max_length=255)
    additional_info = hstore.DictionaryField(db_index=True, blank=True, null=True)
    synonyms = models.ManyToManyField('self', symmetrical=False)
    to_show = 'name'




    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)



class UnificatedSamplesAttributeValue(ShowModel):
    unificated_name = models.ForeignKey('UnificatedSamplesAttributeName')
    value = models.CharField(max_length=255)
    additional_info = hstore.DictionaryField(db_index=True, blank=True, null=True)
    synonyms = models.ManyToManyField('self', symmetrical=False)
    to_show = 'value'

    objects = hstore.HStoreManager()

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "value__icontains",)


class Experiment(models.Model):
    must_have_attributes = ['accession', 'secondaryaccession',
     'name', 'experimenttype', 'releasedate', 'lastupdatedate',
    'samples']
    
    data = hstore.DictionaryField(db_index=True)
    objects = hstore.HStoreManager()
    history = HistoricalRecords()
    microarrays = models.ManyToManyField('Microarray')

    def samples(self):
        return Sample.objects.filter(experiment=self)

    def __unicode__(self):
        to_print = 'accession'
        if to_print in self.data:
            return self.data[to_print]
        else:
            return 'some experiment'

    def __str__(self):
        to_print = 'accession'
        if to_print in self.data:
            return self.data[to_print]
        else:
            return 'some experiment'

    def add_or_replace(data):
        obj, some_bool = Experiment.objects.get_or_create(data__contains=
          {'accession':data['accession']})

        obj.data = data
        obj.save()
        return obj

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

    def has_minimal(self):
        """
        check whether experiment has minimal sample data,
        needed for sample comparison
        """
        samples = self.samples()
        for sample in samples:
            attributes = SampleAttribute.objects.filter(sample=sample)
            if not(attributes.filter(
              unificated_name__name="Organism Part").exists() and \
               attributes.filter(unificated_name__name="Gestational Age").exists()):
                return False
        return True

    def is_cell_line(self):
        if SampleAttribute.objects.filter(
          sample__in=self.samples(),
          unificated_name__name="Cells, Cultured").exists():
            return True
        return False

        
    def status(self):
        status = []
        if 'status' in self.data:
            status.append(self.data['status'])
        if self.is_unified():
            status.append('Unified')
        if 'mail sent' in self.data:
            status.append('Mail Sent')
        if 'mail received' in self.data:
            status.append('Mail Received')
        
        if self.has_minimal():
            status.append('Has minimal sample data')
        if 'excluded' in self.data:
            status.append('Excluded')
        return ", ".join(status)


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

    def add_or_replace(data):
        obj, some_bool = Microarray.objects.get_or_create(data__contains=
          {'accession':data['accession']})
        obj.data = data
        obj.save()
        return obj


class Sample(models.Model):
    must_have_attributes = ['name']
    experiment = models.ForeignKey('Experiment')

    def _show(self):
        return str(self.id)

    def __unicode__(self):
        return self._show()
        
    def __str__(self):
        return self._show()

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

    def add_or_replace(experiment, data):
        sample_obj = None
        if 'name' in data:
            samples_in_experiment = Sample.objects.filter(
                                      experiment=experiment)
            for sample in samples_in_experiment:
                if sample.has_old_name('name'):
                    if sample.get_old_value('name')==data['name']:
                        sample_obj = sample
        if sample_obj == None:
            sample_obj = Sample.objects.create(experiment=experiment)
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
    
    unificated_name = models.ForeignKey('UnificatedSamplesAttributeName',
                                        blank=True,
                                        null=True)
    unificated_value = models.ForeignKey('UnificatedSamplesAttributeValue', 
                                         blank=True,
                                         null=True)
    sample = models.ForeignKey('Sample')

    def _show(self):
        return " ".join((
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
            # print("no such attribute",sample,old_name,old_value)
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
            attribute.unificated_name = UnificatedSamplesAttributeName.objects.get(name='name')
            attribute.unificated_value = UnificatedSamplesAttributeValue.objects.get(value='Text Value')
            attribute.save()
        else:
            # print("no such attribute",sample,old_name,old_value)
            return






    def add_or_replace(sample,
                       old_name=None,
                       old_value=None,
                       unificated_name=None,
                       unificated_value=None):

        if old_name and old_value:
            search = {'sample':sample,
                      'old_name':old_name}
            create = search.copy()
            create['old_value'] = old_value
            value_name = "old_value"
            value = old_value

        elif unificated_name and unificated_value:
            search = {'sample':sample,
                      'unificated_name':unificated_name}
            create = search.copy()
            create['unificated_value'] = unificated_value
            value_name = "unificated_value"
            value = unificated_value
            

        attribute = SampleAttribute.objects.filter(**search)
        
        if attribute.exists():
            attribute_obj = attribute[0]
            setattr(attribute_obj, value_name, value)
        else:
            attribute_obj = SampleAttribute.objects.create(**create)
        attribute_obj.save()
        return attribute_obj
