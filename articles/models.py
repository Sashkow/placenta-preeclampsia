from django.db import models
from django.utils import timezone


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


from django.db import models
from django_hstore import hstore

    
class UnificatedSamplesAttributeName(ShowModel):
    name = models.CharField(max_length=255)
    mesh_id = models.CharField(blank=True, max_length=255)
    to_show = 'name'


class SamplesAttributeNameInExperiment(ShowModel):
    old_name = models.CharField(max_length=255)
    unificated_name = models.ForeignKey('UnificatedSamplesAttributeName')
    
    def _show(self):
        return self.unificated_name._show()



class Experiment(models.Model):
    must_have_attributes = ['accession', 'secondaryaccession',
     'name', 'experimenttype', 'releasedate', 'lastupdatedate',
    'samples']
    filter_horizontal = ('sample_attribute_names',)
    data = hstore.DictionaryField(db_index=True)
    objects = hstore.HStoreManager()
    microarrays = models.ManyToManyField('Microarray')
    sample_attribute_names = models.ManyToManyField('SamplesAttributeNameInExperiment')

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
    fictional_field = models.CharField(blank=True, max_length=3)
    experiment = models.ForeignKey('Experiment')

    def _show(self):
        return str(self.id)

    def __unicode__(self):
        return self._show()
        
    def __str__(self):
        return self._show()




    


    def add_or_replace(experiment, data):
        obj, some_bool = \
          Sample.objects.get_or_create(experiment=experiment,
                                           data__contains={'name':data['name']})
        obj.data = data
        # obj.experiment = experiment
        obj.save()
        return obj

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

class SampleAttributeValueInSample(models.Model):
    old_value = models.CharField(max_length=255) 
    unificated_name = models.ForeignKey('SamplesAttributeNameInExperiment')
    unificated_value = models.ForeignKey('UnificatedSamplesAttributeValue')
    sample = models.ForeignKey('Sample')

    def _show(self):
        return str.join(str(self.unificated_name),
                        str(self.unificated_value))

    def __unicode__(self):
        return self._show()
        
    def __str__(self):
        return self._show()

class UnificatedSamplesAttributeValue(models.Model):
    value = models.CharField(max_length=255)
    mesh_id = models.CharField(blank=True,max_length=255)
    #synonyms many to many with OldSampleAttributeValue
    to_show = 'value'
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









