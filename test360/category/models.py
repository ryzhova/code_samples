# coding: utf8

from __future__ import unicode_literals

from django.db import models


class CategoryManager(models.Manager):

    def get_roots(self):
        object_dict = {}
        root_list = []
        all_objects = self.all()
        for object_ in all_objects:
            object_dict[object_.id] = object_

        for object_ in all_objects:
            if object_.parent_id is not None:
                object_.parent_node = object_dict[object_.parent_id]
                object_.parent_node.children.append(object_)
            else:
                root_list.append(object_)
        return root_list


class Category(models.Model):
    name = models.CharField('Название', max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, verbose_name='Категория')
    objects = CategoryManager()

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.children = []
        self.parent_node = None

    def __str__(self):
        return self.name

    __unicode__ = __str__

    @property
    def depth(self):
        depth = 0
        category = self
        while category.parent_node:
            category = category.parent_node
            depth += 1
        return depth

    def get_bread_crumbs(self):
        category = self
        out = []
        while category.parent:
            category = category.parent
            out.insert(0, category)
        return out

    def get_nodes(self):
        yield self
        for i in self.children:
            for j in i.get_nodes():
                yield j
