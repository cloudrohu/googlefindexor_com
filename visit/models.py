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
from utility.models import Find_Form, Call_Status,SocialSite,Googlemap_Status


class Today_Visit(models.Model):
    image=models.ImageField(upload_to='images/')
    title = models.CharField(max_length=50,unique=True)
    contact_person = models.CharField(max_length=255,null=True , blank=True)
    contact_no = models.CharField(max_length=255,null=True , blank=True)
    description = models.CharField(max_length=500,null=True , blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

    def __str__(self):
        return self.title + '--' + self.contact_person + '--' + self.contact_no 

    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    

    class Meta:
        verbose_name_plural='1. Today Visit'

# -------------------------------------------------------------------------------------------------------------
class Follow_Up(models.Model):
    company = models.ForeignKey(Today_Visit,blank=True, null=True , on_delete=models.CASCADE)
    follow_up = models.DateTimeField(blank=True, null=True,)
    comment = models.CharField(max_length=500,blank=True, null=True,)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='2. Follow_Up'
 
class Meeting(models.Model):
    company = models.ForeignKey(Today_Visit,blank=True, null=True , on_delete=models.CASCADE)
    meeting = models.DateTimeField(null=True, blank=True)
    comment = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 
    
    class Meta:
        verbose_name_plural='3. Meeting'
 