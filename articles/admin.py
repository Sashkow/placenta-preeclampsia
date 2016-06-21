from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .forms import ArticleForm
from .models import Article, Attribute

def _lookup_f(attr_name):
        def f(obj):
            if Attribute.objects.filter(article=obj,
                                        attribute_name=attr_name).exists():
                return Attribute.objects.get(article=obj,
                                             attribute_name=attr_name).attribute_value
            else:
                return None
        f.short_description = attr_name
        return f

def _lookup_f_tuple():
    lst = []
    for attr_name in Attribute.attribute_names:
        lst.append(_lookup_f(attr_name))
    return tuple(lst)

class ArticleAdmin(ModelAdmin):
    form = ArticleForm
    fieldsets = (
        (None, {
            'fields': Attribute.attribute_names,
        }),
    )

    list_display = _lookup_f_tuple()

admin.site.register(Article, ArticleAdmin)

class AttributeAdmin(ModelAdmin):

    exclude = []
    list_display = ('article',
                    'attribute_name',
                    'attribute_value',
    )
admin.site.register(Attribute, AttributeAdmin)