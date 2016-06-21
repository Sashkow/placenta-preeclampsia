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