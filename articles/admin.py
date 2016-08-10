from django.contrib import admin
from django.contrib.admin import ModelAdmin

# from .forms import ArticleForm
from .models import Article, Attribute, Experiment, Sample, Microarray

from django.http import HttpResponseRedirect

import ast

from articles.getdata import get_experiment_attributes

from django.core.urlresolvers import reverse

def _lookup_f(ModelClass, attr_name):
        def f(obj):
            if ModelClass.objects.filter(id=obj.id, data__contains=[attr_name]).exists():
                return dict(ModelClass.objects.get(id=obj.id).data)[attr_name]
            else:
                return None
        f.short_description = attr_name
        return f
        
def _list_display(ModelClass):
    f_lst = []

    for attr_name in ModelClass.must_have_attributes:
        f_lst.append(_lookup_f(ModelClass, attr_name))
    return f_lst


class AttributeInline(admin.TabularInline):
    model = Attribute
    extra = 0

def _article_lookup_f(attr_name):
    def f(obj):
        if Attribute.objects.filter(article=obj,
                                    attribute_name=attr_name).exists():
            return Attribute.objects.get(article=obj,
                                         attribute_name=attr_name).attribute_value
        else:
            return None
    f.short_description = attr_name
    return f

def _article_list_display():
    lst = []
    for attr_name in Attribute.attribute_names:
        lst.append(_article_lookup_f(attr_name))
    return tuple(lst)
    
class ArticleAdmin(ModelAdmin):
    # form = ArticleForm
    '''fieldsets = (
        (None, {
            'fields': Attribute.attribute_names,
        }),
    )'''
    inlines = [AttributeInline,]

    list_display = _article_list_display()

admin.site.register(Article, ArticleAdmin)


class AttributeAdmin(ModelAdmin):
    exclude = []
    list_display = ('article',
                    'attribute_name',
                    'attribute_value',
    )
admin.site.register(Attribute, AttributeAdmin)


def _experiment_extra_display():
    def f(obj):
        exists = Experiment.objects.filter(id=obj.id).exists()
        if exists:
            exp_data = Experiment.objects.get(id=obj.id).data
            extra_data = {item:exp_data[item] for item in exp_data 
                            if not(item in Experiment.must_have_attributes)}
            return str(extra_data)
        else:
            return None

    f.short_description = 'other data'
    return [f]

def _experiment_microarrays_display():
    def f(obj):
        show_field = 'name'
        names = ""
        exists = Experiment.objects.filter(id=obj.id).exists()
        if exists:
            microarrays = Experiment.objects.get(id=obj.id).microarrays.all()

            for microarray in microarrays:
                if show_field in microarray.data:
                    names += microarray.data[show_field] + ', '
        return names
    f.short_description = 'platform'
    return [f]


class MicroarrayInline(admin.TabularInline):
    model = Experiment.microarrays.through
    extra = 0


class ExperimentAdmin(ModelAdmin):
    inlines = [MicroarrayInline,]    
    list_display = _list_display(Experiment) + \
                   _experiment_microarrays_display() + \
                   _experiment_extra_display()
    exclude = ['microarrays']


    def response_change(self, request, obj):
        if '_autofillbutton' in request.POST:
            data = ast.literal_eval(dict(request.POST)['data'][0])
            if 'accession' in data:
                accession = data['accession']
                exp_attrs, arrays_attrs = get_experiment_attributes(accession)
                experiment = Experiment.add_or_replace(exp_attrs) # obj.save() is here
                print("microarrays:::", arrays_attrs)
                for array_attrs in arrays_attrs:
                    microarray = Microarray.add_or_replace(array_attrs) # obj.save() is here
                    if not(experiment.microarrays.filter(id=microarray.id).exists()):
                        experiment.microarrays.add(microarray)
                
                return HttpResponseRedirect(reverse("admin:articles_experiment_change", args=[experiment.id]))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return super(ExperimentAdmin, self).response_change(request, obj)

admin.site.register(Experiment, ExperimentAdmin)



class MicroarrayAdmin(ModelAdmin):
    list_display = _list_display(Microarray)



admin.site.register(Microarray, MicroarrayAdmin)
admin.site.register(Sample)