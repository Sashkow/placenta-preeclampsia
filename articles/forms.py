from django import forms
from django.forms import ModelForm
from .models import Article, Attribute, SampleAttribute, Sample, UnificatedSamplesAttributeValue


# class ArticleForm(ModelForm):
#     geo_id = forms.CharField(max_length=30, required=False)
#     geo_link = forms.CharField(required=False)
#     arr_id = forms.CharField(max_length=30, required=False)
#     arr_link = forms.CharField(required=False)
#     title = forms.CharField()
#     platform = forms.CharField(max_length=300, required=False)
#     samples = forms.IntegerField(required=False)

#     def __init__(self, *args, **kwargs):
#         if 'instance' in kwargs:
#             instance = kwargs['instance']
#             initial = kwargs.get('initial', {})
#             attrs = Attribute.objects.filter(article=instance)
#             for attr_name in Attribute.attribute_names:
#                 if attrs.filter(attribute_name=attr_name).exists():
#                     initial[attr_name] = \
#                       attrs.get(attribute_name=attr_name).attribute_value
#             kwargs['initial'] = initial
#         super(ArticleForm, self).__init__(*args, **kwargs)

#     def save(self, commit=True):
#         #todo if instance exists, load values into fields
#         instance = super(ArticleForm, self).save(commit=commit)
#         instance.save()

#         for attr_name in Attribute.attribute_names:
#             attr_value = self.cleaned_data.get(attr_name, None)
#             if attr_value!=None:
#                 if Attribute.objects.filter(article=instance,
#                                             attribute_name=attr_name).exists():
#                     entry = Attribute.objects.get(article=instance,
#                                                   attribute_name=attr_name)
#                     entry.attribute_value = attr_value
#                 else:
#                     entry = Attribute(article=instance,
#                                   attribute_name=attr_name,
#                                   attribute_value=attr_value)
#                 entry.save()   
#         return instance

class SampleAttributeInlineForm(ModelForm):
    name_for_each = forms.BooleanField(required=False,
                                         label='for each sample')
    value_for_each = forms.BooleanField(required=False,
                                         label='for each sample')

    def __init__(self, *args, **kwargs):
        super(SampleAttributeInlineForm, self).__init__(*args, **kwargs)

        # self.fields['unificated_value'].queryset = \
        #   UnificatedSamplesAttributeValue.objects.filter(
        #     unificated_name=self.instance.unificated_name)
        

    def _get_all_with_same_old_name(self, instance):
        experiment = instance.sample.experiment
        old_name = instance.old_name
        
        samples_in_experiment = Sample.objects.filter(
          experiment=experiment)

        sample_attributes = SampleAttribute.objects.filter(
          sample__in=samples_in_experiment,
          old_name=old_name)

        return sample_attributes

    def _get_all_with_same_old_name_value(self, instance):
        if instance.unificated_value.unificated_name.name == 'Common':
            sample_attributes = self._get_all_with_same_old_name(instance)
            return sample_attributes
        else:
            sample_attributes = \
              self._get_all_with_same_old_name(instance).filter(
                old_value=instance.old_value)
            return sample_attributes

    def save(self, commit=True):
        
        instance = super(SampleAttributeInlineForm, self).save(commit=False)
        instance.save() # don't know if needed

        if self.cleaned_data['name_for_each']:
            sample_attributes = self._get_all_with_same_old_name(instance)            
            unificated_name = instance.unificated_name
            for attribute in sample_attributes:
                attribute.unificated_name = unificated_name
                attribute.save()

        if self.cleaned_data['value_for_each']:
            sample_attributes = self._get_all_with_same_old_name_value(instance)
            unificated_value = instance.unificated_value
            for attribute in sample_attributes:
                attribute.unificated_value = unificated_value
                attribute.save()

        instance.unificated_name.old_name = \
          self.cleaned_data['old_name']

        instance.unificated_name.save()

        return instance
