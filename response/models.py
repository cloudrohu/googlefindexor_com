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
# Create your models here.
from utility.models import Find_Form, Call_Status,SocialSite,Googlemap_Status,City,Locality

class Response_From(models.Model):
    name = models.CharField(max_length=100,unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural='4. Response_From'

class Response_Status(models.Model):
    name = models.CharField(max_length=100,unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural='5. Response_Status'

class Response(models.Model):
    response_from = models.ForeignKey(Response_From,blank=True, null=True , on_delete=models.CASCADE)
    locality_city = models.ForeignKey(Locality,blank=True, null=True , on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=False)
    contact_no = models.CharField(max_length=255,null=True , blank=True)
    email_id = models.EmailField(max_length=255,null=True , blank=True)
    description = models.CharField(max_length=500,null=True , blank=True)
    response_status = models.ForeignKey(Response_Status,blank=True, null=True , on_delete=models.CASCADE)
    meeting_follow_up = models.DateTimeField(blank=True, null=True,)
    call_comment = models.CharField(max_length=500,null=True , blank=True)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

    def __str__(self):
        return self.name + ' ' + self.contact_no 
  
    class Meta:
        verbose_name_plural='1. Response'

# -------------------------------------------------------------------------------------------------------------
class Follow_Up(models.Model):
    name = models.ForeignKey(Response,blank=True, null=True , on_delete=models.CASCADE)
    follow_up = models.DateTimeField(blank=True, null=True,)
    comment = models.CharField(max_length=500,blank=True, null=True,)
    locality_city= models.ForeignKey(Locality,blank=True, null=True , on_delete=models.CASCADE)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='2. Follow_Up'
 
class Meeting(models.Model):
    name = models.ForeignKey(Response,blank=True, null=True , on_delete=models.CASCADE)
    meeting = models.DateTimeField(null=True, blank=True)
    comment = models.CharField(max_length=500,blank=True, null=True,)
    locality_city= models.ForeignKey(Locality,blank=True, null=True , on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='3. Meeting'
 