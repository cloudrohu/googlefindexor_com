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

class Find_Form(models.Model):    
    title = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name_plural='1. Find_Form'



class Call_Status(models.Model):
    title = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='2. Call_Status'



class SocialSite(models.Model):
    title = models.CharField(max_length=50,unique=True)   
    code = models.CharField(max_length=50,unique=True,null=True , blank=True)   
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='3. SocialSite'