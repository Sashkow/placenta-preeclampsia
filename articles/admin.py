from django.contrib import admin
from django.contrib.admin import ModelAdmin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from .forms import SampleAttributeInlineForm
from .models import *

from django.http import HttpResponseRedirect

import ast

from articles.getdata import get_experiment_attributes
from articles.getdata import get_experiment_samples_attributes

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
    pass
    # # form = ArticleForm
    # '''fieldsets = (
    #     (None, {
    #         'fields': Attribute.attribute_names,
    #     }),
    # )'''
    # inlines = [AttributeInline,]

    # list_display = _article_list_display()

admin.site.register(Article)


class AttributeAdmin(ModelAdmin):
    exclude = []
    list_display = ('article',
                    'attribute_name',
                    'attribute_value',
    )
# admin.site.register(Attribute, AttributeAdmin)


def _extra_display(ModelClass):
    def f(obj):
        exists = ModelClass.objects.filter(id=obj.id).exists()
        if exists:
            exp_data = ModelClass.objects.get(id=obj.id).data
            extra_data = {item:exp_data[item] for item in exp_data 
                            if not(item in ModelClass.must_have_attributes)}
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


class MicroarrayInline(SuperInlineModelAdmin, admin.TabularInline):
    model = Experiment.microarrays.through
    extra = 0

class SampleAttributeInline(SuperInlineModelAdmin, admin.TabularInline):
    form = SampleAttributeInlineForm
    fields = (
              'old_name',
              'old_value',
              'unificated_name',
              'name_for_each',
              'unificated_value',
              'value_for_each'
              )

    raw_id_fields = ('unificated_name','unificated_value',)
    # define the related_lookup_fields
    autocomplete_lookup_fields = {
        'fk': ['unificated_name', 'unificated_value']
    }

    model = SampleAttribute
    extra = 0


    def formfield_for_dbfield(self, db_field, **kwargs):
        
        formfield = super(SampleAttributeInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'unificated_name':
            # dirty trick so queryset is evaluated and cached in .choices
            formfield.choices = formfield.choices
        return formfield

class SampleInline(SuperInlineModelAdmin, admin.StackedInline):
    
    model = Sample
    inlines = [SampleAttributeInline,]   
    extra = 0



class ExperimentAdmin(SuperModelAdmin):
    inlines = [MicroarrayInline, SampleInline]    
    list_display = _list_display(Experiment) + \
                   _experiment_microarrays_display() + \
                   _extra_display(Experiment)
    exclude = ['microarrays']
    fields = ('data',)

    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)
    #     for instance in instances: 
    #         instance.save()
    #     formset.save_m2m()

    def response_change(self, request, obj):
        if '_autofillbutton' in request.POST:
            data = ast.literal_eval(dict(request.POST)['data'][0])
            if 'accession' in data:
                accession = data['accession']
                exp_attrs, arrays_attrs = get_experiment_attributes(accession)
                samples_attrs = get_experiment_samples_attributes(accession)
                experiment = Experiment.add_or_replace(exp_attrs) # obj.save() is here
                print("microarrays:::", arrays_attrs)

                # add microarrays
                for array_attrs in arrays_attrs:
                    microarray = Microarray.add_or_replace(array_attrs) # obj.save() is here
                    if not(experiment.microarrays.filter(id=microarray.id).exists()):
                        experiment.microarrays.add(microarray)

                # add samples
                for sample_attrs in samples_attrs:
                    sample_obj = Sample.add_or_replace(experiment=experiment, data=sample_attrs)

                return HttpResponseRedirect(reverse("admin:articles_experiment_change", args=[experiment.id]))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return super(ExperimentAdmin, self).response_change(request, obj)

admin.site.register(Experiment, ExperimentAdmin)



class MicroarrayAdmin(ModelAdmin):
    list_display = _list_display(Microarray)



class SampleAdmin(SuperModelAdmin):
    inlines = [SampleAttributeInline,]

    # list_display = ['data', 'experiment']
    # list_editable = ['data', 'experiment']
    # list_display = _list_display(Sample)+_extra_display(Sample)
    # list_editable = _list_display(Sample)+_extra_display(Sample)


class SampleAttributeAdmin(ModelAdmin):
    list_display = ['id','sample', 'unificated_name', 'unificated_value' ]

class UnificatedSamplesAttributeNameAdminInline(admin.TabularInline):

    model = UnificatedSamplesAttributeName.synonyms.through
    fk_name = 'from_unificatedsamplesattributename'
    extra = 0


class UnificatedSamplesAttributeNameAdmin(ModelAdmin):
    inlines = [UnificatedSamplesAttributeNameAdminInline,]
    exclude = ('synonyms',)

admin.site.register(Microarray, MicroarrayAdmin)
admin.site.register(Sample, SampleAdmin)


admin.site.register(UnificatedSamplesAttributeName, UnificatedSamplesAttributeNameAdmin)


admin.site.register(SampleAttribute,SampleAttributeAdmin)

admin.site.register(UnificatedSamplesAttributeValue)