from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import CategoryForm
from .models import Category


def index(request):
    if request.method == 'GET':
        form = CategoryForm()

    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('category:index'))

    tree_roots = Category.objects.get_roots()
    out = []
    for i in tree_roots:
        out.extend(i.get_nodes())
    return render(request, 'category/index.html', {'form': form, 'out': out})


def detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'GET':
        form = CategoryForm(instance=category)

    elif request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('category:detail',
                        kwargs={'category_id': category_id}))

    return render(request, 'category/detail.html',
                  {'form': form, 'category': category})


def delete(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
        return HttpResponseRedirect(reverse('category:index'))
