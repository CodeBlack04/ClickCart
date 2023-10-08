from django.shortcuts import render, redirect
from item.models import Item, Category
from core.forms import SignupForm

# Create your views here.

def index(request):
    items = Item.objects.filter(is_sold = False)
    categories = Category.objects.all()
    return render(request=request, template_name='core/index.html', context={
        'items': items,
        'categories': categories
    })

def contact(request):
    return render(request=request, template_name='core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request=request, template_name='core/signup.html', context={
        'form': form
    })
