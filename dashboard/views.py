from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from item.models import Item

# Create your views here.

@login_required
def my_items(request):
    items = Item.objects.filter(created_by = request.user)
    return render(request=request, template_name='dashboard/index.html', context={
        'items': items
    })