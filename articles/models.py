from django.db import models
from django.utils import timezone


class Article(models.Model):
    def __str__(self):
        return str(self.id)


class Attribute(models.Model):
    attribute_names = ['title',
                       'geo_id', 'geo_link',
                       'arr_id', 'arr_link',
                       'platform', 
                       'samples']

    article = models.ForeignKey('Article')
    attribute_name = models.CharField(blank=True, max_length=200)
    attribute_value = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return str.join(" ", [str(self.article),
                             str(self.attribute_name),
                             str(self.attribute_value),]
               )

from django.db import models
from django_hstore import hstore

class Experiment(models.Model):
    must_have_attributes = ['accession', 'secondaryaccession',
     'name', 'experimenttype', 'releasedate', 'lastupdatedate',
    'samples']
    
    data = hstore.DictionaryField(db_index=True)
    objects = hstore.HStoreManager()
    microarrays = models.ManyToManyField('Microarray')

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
    data = hstore.DictionaryField(db_index=True)
    objects = hstore.HStoreManager()

    def add_or_replace(experiment, data):
        obj, some_bool = \
          Sample.objects.get_or_create(experiment=experiment,
                                           data__contains={'name':data['name']})
        obj.data = data
        # obj.experiment = experiment
        obj.save()
        return obj

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
