from django.shortcuts import render
from django.shortcuts import render,redirect

from adsrepoting.models import Campaign
from django.shortcuts import render, get_object_or_404


# Create your views here.

from business.models import City, Category,Company

def index(request):
    #category = categoryTree(0,'',currentlang)
    city = City.objects.all()
    category = Category.objects.all()


    context={
        'category':category,
        'city':city,
        
    }
    return render(request, 'index.html',context)


def company(request):

    city = City.objects.all()
    category = Category.objects.all()
    company = Company.objects.all()

    context={
        'category':category,
        'city':city,        
        'company':company,        
    }        
    return render(request, 'company.html', context)



def company_details(request,slug):
    
    company = Company.objects.filter(slug = slug)

    if company.exists():
        company = Company.objects.get(slug = slug)
    else:
        return redirect('404')    
    
    context = {
        'company': company,
    }   

    return render(request, 'company_details.html',context )




def metarepoting(request):

    campaigns = Campaign.objects.all()
    context={
        'campaigns':campaigns,             
    }        
    return render(request, 'adsrepoting/meta.html', context)