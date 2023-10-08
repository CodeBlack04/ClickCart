from django.shortcuts import render
from django.db.models import Q
from item.models import Item, Category

# Create your views here.

def all_items(request):
    items = Item.objects.filter(is_sold = False)
    categories = Category.objects.all().order_by('name',)
    query = request.GET.get('query', '') #get,default
    category_id = request.GET.get('category', 0)

    #if category_id:
        #items: items.filter(category_id=category_id)
    print(category_id)
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        items = items.filter(category__id = category_id)
    
    return render(request=request, template_name='browse/index.html', context={
        'items': items,
        'categories': categories,
        'category_id': int(category_id),
        'query': query,
    })
