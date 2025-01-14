from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
# Create your models here.
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.text import slugify

from utility.models import Find_Form, Call_Status,SocialSite,Googlemap_Status


class City(MPTTModel):
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    slug = models.SlugField(unique=True , null=True , blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.title)
        super(City ,self).save(*args , **kwargs)
    
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('city_detail', kwargs={'slug': self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])
    

class Locality(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(unique=True , null=True , blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "_" + self.city
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.title + '--' + self.city.title)
        super(Locality ,self).save(*args , **kwargs)
    
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('locality_detail', kwargs={'slug': self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(unique=True , null=True , blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.title)
        super(Category ,self).save(*args , **kwargs)
    
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

class Company(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    call_status = models.ForeignKey(Call_Status, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    call_comment = models.CharField(max_length=1000,null=True , blank=True)
    followup_meeting = models.DateTimeField(null=True, blank=True)
    
    find_form = models.ForeignKey(Find_Form, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    googlemap_status = models.ForeignKey(Googlemap_Status, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    company_name = models.CharField(max_length=50,unique=False)
    contact_person = models.CharField(max_length=255,null=True , blank=True)
    contact_no = models.CharField(max_length=255,null=True , blank=True)
    email = models.EmailField(null=True,blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand     
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand 
    address = models.CharField(max_length=500,null=True , blank=True)
    keywords = models.CharField(max_length=255,null=True , blank=True)
    website = models.CharField(max_length=255,null=True , blank=True)
    google_map = models.CharField(max_length=1000,null=True , blank=True)
    description = models.CharField(max_length=1000,null=True , blank=True)
    about = RichTextUploadingField(blank=True)

    image=models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=500,null=True,blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(User, related_name='updated_by_user',on_delete=models.CASCADE,null=True,blank=True,)
    created_by=models.ForeignKey(User, related_name='created_by_user',on_delete=models.CASCADE,null=True,blank=True,)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

    def __str__(self):
        return self.company_name+ '   ' + self.contact_no + ' ' +self.address + '--' +self.locality.title
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.category.title + '--' + self.company_name + '--' + self.address + '--' + self.locality.title + '--' + self.city.title)
        super(Company ,self).save(*args , **kwargs)

    class Meta:
        verbose_name_plural='1. Company'

    def get_absolute_url(self):
        return reverse('company_details', kwargs={'slug': self.slug})
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

class Approx(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Brand
    city = models.ForeignKey(City, on_delete=models.CASCADE) #many to one relation with Brand
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE,) #many to one relation with Brand
    title = models.CharField(max_length=50,unique=True)    
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SocialLink(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    socia_site = models.ForeignKey(SocialSite, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    link = models.CharField(max_length=50,unique=True)    
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link
    
class Error(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    title = models.CharField(max_length=500,unique=True)    
    error = models.CharField(max_length=500,unique=True)    
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# -------------------------------------------------------------------------------------------------------------
class Follow_Up(models.Model):
    company = models.ForeignKey(Company,blank=True, null=True , on_delete=models.CASCADE)
    follow_up = models.DateTimeField(blank=True, null=True,)
    comment = models.CharField(max_length=500,blank=True, null=True,)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='2. Follow_Up'

class Images(models.Model):
    product=models.ForeignKey(Company,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title
    
class Faq(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    questions = models.CharField(max_length=500,blank=True)
    answers = models.TextField(blank=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.questions

class Meeting(models.Model):
    company = models.ForeignKey(Company,blank=True, null=True , on_delete=models.CASCADE)
    meeting = models.DateTimeField(null=True, blank=True)
    comment = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='3. Meeting'
    
class Visit(models.Model):
    company = models.ForeignKey(Company,blank=True, null=True , on_delete=models.CASCADE)
    comment = models.CharField(max_length=500,blank=True, null=True,)
    visit_date=models.DateTimeField(auto_now_add=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='4. Visit'
#-------------------------------------------------------------------------------------------------------
