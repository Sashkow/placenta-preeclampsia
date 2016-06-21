from django import forms
from django.forms import ModelForm
from .models import Article, Attribute


class ArticleForm(ModelForm):
    geo_id = forms.CharField(max_length=30, required=False)
    geo_link = forms.CharField(required=False)
    arr_id = forms.CharField(max_length=30, required=False)
    arr_link = forms.CharField(required=False)
    title = forms.CharField()
    platform = forms.CharField(max_length=300, required=False)
    samples = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs['instance']
            initial = kwargs.get('initial', {})
            attrs = Attribute.objects.filter(article=instance)
            for attr_name in Attribute.attribute_names:
                if attrs.filter(attribute_name=attr_name).exists():
                    initial[attr_name] = \
                      attrs.get(attribute_name=attr_name).attribute_value
            kwargs['initial'] = initial
        super(ArticleForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        #todo if instance exists, load values into fields
        instance = super(ArticleForm, self).save(commit=commit)
        instance.save()

        for attr_name in Attribute.attribute_names:
            attr_value = self.cleaned_data.get(attr_name, None)
            if attr_value!=None:
                if Attribute.objects.filter(article=instance,
                                            attribute_name=attr_name).exists():
                    entry = Attribute.objects.get(article=instance,
                                                  attribute_name=attr_name)
                    entry.attribute_value = attr_value
                else:
                    entry = Attribute(article=instance,
                                  attribute_name=attr_name,
                                  attribute_value=attr_value)
                entry.save()   
        return instance