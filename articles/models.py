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
    'samples','excluded']
    
    data = hstore.DictionaryField(db_index=True)
    objects = hstore.HStoreManager()
    history = HistoricalRecords()
    microarrays = models.ManyToManyField('Microarray')

    def samples(self):
        return Sample.objects.filter(experiment=self)

    def __unicode__(self):
        to_print = 'accession'
        if to_print in sel.data:
            return self.data[to_print]
        else:
            return 'some experiment'

    def __str__(self):
        return str(self.id)

    def add_or_replace(data):
        obj, some_bool = Experiment.objects.get_or_create(data__contains=
          {'accession':data['accession']})

        obj.data = data
        obj.save()
        return obj


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
    old_name = models.CharField(max_length=255, blank=True)
    old_value = models.CharField(max_length=255, blank=True) 
    
    unificated_name = models.ForeignKey('UnificatedSamplesAttributeName',
                                        blank=True,
                                        null=True)
    unificated_value = models.ForeignKey('UnificatedSamplesAttributeValue', 
                                         blank=True,
                                         null=True)
    sample = models.ForeignKey('Sample')

    def _show(self):
        return " ".join((str(self.unificated_name),
                        str(self.unificated_value)))    

    def __unicode__(self):
        return self._show()
        
    def __str__(self):
        return self._show()


    def add_or_replace(sample, old_name, old_value):
        attribute = SampleAttribute.objects.filter(sample=sample,
                                                   old_name=old_name)
        if attribute.exists():
            attribute_obj = attribute[0]
            attribute_obj.old_value = old_value
        else:
            attribute_obj = SampleAttribute.objects.create(sample=sample, 
                                                           old_name=old_name,
                                                           old_value=old_value)

        attribute_obj.save()
        return attribute_obj
            

