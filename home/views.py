import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, F
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation

from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage,FAQ,Slider,Offer
from googlefindexor_com import settings
from product.models import Category, Product, Images, Comment, Variants,City
from user.models import UserProfile
# Create your views here.


def index(request):
    setting = Setting.objects.all().order_by('-id')[:1]
    category = Category.objects.all()
    city = City.objects.all()
    offer = Offer.objects.filter(featured_project = 'True').order_by('id')[:2]  #first 4 products
    featured_category = Category.objects.filter(featured_category = 'True').order_by('id')[:3]  #first 4 products
    slider = Slider.objects.filter(featured_project = 'True').order_by('id')[:6]  #first 4 products
    products_slider = Product.objects.all().order_by('id')[:4]  #first 4 products
    products_latest = Product.objects.all().order_by('-id')[:8]  # last 4 products
    products_picked = Product.objects.all().order_by('?')[:8]   #Random selected 4 products
    page="home"
    context={
        'offer':offer,
        'city':city,
        'slider':slider,
        'setting':setting,
        'category':category,
        'page':page,
        'products_picked':products_picked,
        'products_slider':products_slider,
        'products_latest':products_latest,
        'featured_category':featured_category,
    }

    return render(request,'index.html',context)

def SERVICES(request):
    #category = categoryTree(0,'',currentlang)
    setting = Setting.objects.all().order_by('-id')[:1]
    category = Category.objects.all()    
    context={
        'setting':setting,
        'category':category
    } 
    return render(request, 'service.html',context)

def furniture(request):
    #category = categoryTree(0,'',currentlang)
    setting = Setting.objects.all().order_by('-id')[:1]
    category = Category.objects.all()    
    context={
        'setting':setting,
        'category':category
    } 
    return render(request, 'furniture.html',context)


def aboutus(request):
    #category = categoryTree(0,'',currentlang)
    setting = Setting.objects.all().order_by('-id')[:1]

    category = Category.objects.all()

    
    context={
        'setting':setting,
        'category':category
    }
 
    return render(request, 'about.html',context)

def contactus(request):
    setting = Setting.objects.all().order_by('-id')[:1]

    category = Category.objects.all()

    if request.method == 'POST': # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request,"Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
    form = ContactForm
    context={
        'setting':setting,
        'form':form ,
        'category':category,
    }    
    return render(request, 'contactus.html',context)

def category_products(request,id,slug):
    setting = Setting.objects.all().order_by('-id')[:1]
    
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id) #default language
    
    context={'products': products,
             'setting':setting,
             #'category':category,
             'category':category }
    return render(request,'category_products.html',context)


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products,
                        'query':query,
                       'category': category }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_detail(request,id,slug):
    query = request.GET.get('q')
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    #defaultlang = settings.LANGUAGE_CODE[0:2] #en-EN
    #currentlang = request.LANGUAGE_CODE[0:2]
    #category = categoryTree(0, '', currentlang)
    category = Category.objects.all()

    product = Product.objects.get(pk=id)

    
    # <<<<<<<<<< M U L T I   L A N G U G A E <<<<<<<<<<<<<<< end
    setting = Setting.objects.all().order_by('-id')[:1]

    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {'product': product,'category': category,
               'images': images, 'comments': comments,
               'setting': setting
               }
    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
    
    return render(request,'product_detail1.html',context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def faq(request):
   
    return render(request, 'faq.html')
