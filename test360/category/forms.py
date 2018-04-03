# coding: utf8

from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'parent']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.fields['parent'].required = False
            self.fields['parent'].choices = self.choice_tuple()
        else:
            self.fields.pop('parent')

    def choice_tuple(self):
        tree_roots = Category.objects.get_roots()
        out_list = [(None, '-------')]
        for i in tree_roots:
            for j in i.get_nodes():
                out_list.append((j.id, u'··' * j.depth + j.name))
        return out_list
