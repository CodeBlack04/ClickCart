from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import NewItemForm, EditItemForm

# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)

    return render(request=request, template_name='item/detail.html', context={
        "item": item,
        "related_items": related_items
    })

@login_required
def newitem(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', item.id)
    else:
        form = NewItemForm()

    return render(request=request, template_name='item/form.html', context={
        'form': form,
        'title': 'New Item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance = item)

        if form.is_valid():
            form.save()
            return redirect('item:detail', item.id)
    else:
        form = EditItemForm(instance = item)

    return render(request=request, template_name='item/form.html', context={
        'form': form,
        'title': 'Edit Item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user)
    item.delete()
    return redirect('dashboard:index')