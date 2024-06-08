from django.shortcuts import render

# Create your views here.

from business.models import City, Category


def index(request):
    #category = categoryTree(0,'',currentlang)
    city = City.objects.all()
    category = Category.objects.all()


    context={
        'category':category,
        'city':city,
        
    }

    return render(request, 'index.html',context)
