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
from django.db.models.signals import pre_save
from utility.models import Find_Form, Call_Status,SocialSite


from django.utils.text import slugify


class City(models.Model):
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

    def get_absolute_url(self):
        return reverse('city_detail', kwargs={'slug': self.slug})
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))



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
    featured_category = models.BooleanField(default=False)
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


class Product(models.Model):
   
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    call_status = models.ForeignKey(Call_Status, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    find_form = models.ForeignKey(Find_Form, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    title = models.CharField(max_length=250,unique=True)
    contact_person = models.CharField(max_length=255,null=True , blank=True)
    contact_no = models.CharField(max_length=255,null=True , blank=True)
    email = models.EmailField(null=True,blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE) #many to one relation with Brand     
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE) #many to one relation with Brand 
    address = models.CharField(max_length=500,null=True , blank=True)
    keywords = models.CharField(max_length=255,null=True , blank=True)
    website = models.CharField(max_length=255,null=True , blank=True)
    google_map = models.CharField(max_length=1000,null=True , blank=True)
    description = models.TextField(max_length=5000,null=True , blank=True)
    image=models.ImageField(upload_to='images/')
    slug = models.SlugField(unique=True , null=True , blank=True)
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(User, related_name='updated_by_user',on_delete=models.CASCADE,null=True,blank=True,)
    created_by=models.ForeignKey(User, related_name='created_by_user',on_delete=models.CASCADE,null=True,blank=True,)
    def __str__(self):
        return self.title


    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def save(self , *args , **kwargs):
        self.slug = slugify(self.title + '--' + self.locality.title + '--' + self.city.title)
        super(Product ,self).save(*args , **kwargs)


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def avaregereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt


class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']

class Approx(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    city = models.ForeignKey(City, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    title = models.CharField(max_length=50,unique=True)    
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SocialLink(models.Model):
    company = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    socia_site = models.ForeignKey(SocialSite, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    link = models.CharField(max_length=50,unique=True)    
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link
    
class Error(models.Model):
    company = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True) #many to one relation with Brand
    title = models.CharField(max_length=500,unique=True)    
    error = models.CharField(max_length=500,unique=True)    
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Follow_Up(models.Model):
    company = models.ForeignKey(Product,blank=True, null=True , on_delete=models.CASCADE)
    follow_up = models.DateTimeField(blank=True, null=True,)
    comment = models.CharField(max_length=500,blank=True, null=True,)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='2. Follow_Up'

class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""

class Faq(models.Model):
    company=models.ForeignKey(Product,on_delete=models.CASCADE)
    questions = models.CharField(max_length=500,blank=True)
    answers = models.TextField(blank=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.questions

class Meeting(models.Model):
    company = models.ForeignKey(Product,blank=True, null=True , on_delete=models.CASCADE)
    meeting = models.DateTimeField(null=True, blank=True)
    comment = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='3. Meeting'
    
class Visit(models.Model):
    company = models.ForeignKey(Product,blank=True, null=True , on_delete=models.CASCADE)
    comment = models.CharField(max_length=500,blank=True, null=True,)
    visit_date=models.DateTimeField(auto_now_add=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='4. Visit'

class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""

