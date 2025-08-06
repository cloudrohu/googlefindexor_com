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
from utility.models import  Call_Status,City,Locality,Response_Status,RequirementType
from business.models import Category

class Response(models.Model):
    call_status = models.ForeignKey(Call_Status, blank=True, null=True, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=15, null=True, blank=True, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User, related_name='responses_created',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User, related_name='responses_updated',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        # Remove spaces from contact_no
        if self.contact_no:
            self.contact_no = self.contact_no.replace(" ", "")

        # Set created_by / updated_by manually from view or admin signal
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.contact_no or ''} {self.description or ''}"

    class Meta:
        verbose_name_plural = '1. Response'

# -------------------------------------------------------------------------------------------------------------
class Meeting_Follow_Up(models.Model):
    Type = (
        ('Meeting', 'Meeting'),
        ('Follow_Up', 'Follow_Up'),        
    )

    type = models.CharField(max_length=25, choices=Type,null=True, blank=True)

    Meeting_follow_up = models.DateTimeField(blank=True, null=True,)
    contact_persone = models.CharField(max_length=500,blank=True, null=True,)
    email_id = models.EmailField(max_length=255,null=True , blank=True)

    business_name = models.CharField(max_length=500,blank=True, null=True,)

    business_category = models.ForeignKey(Category,blank=True, null=True , on_delete=models.CASCADE)
    response_status = models.ForeignKey(Response_Status,blank=True, null=True , on_delete=models.CASCADE)
    requirement_type = models.ForeignKey(
    'utility.RequirementType',
    on_delete=models.SET_NULL,
    null=True, blank=True
)
    
    city = models.ForeignKey(City,blank=True, null=True , on_delete=models.CASCADE)
    locality_city= models.ForeignKey(Locality,blank=True, null=True , on_delete=models.CASCADE)
    response = models.ForeignKey(Response,blank=True, null=True , on_delete=models.CASCADE)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    
    created_by = models.ForeignKey(
        User, related_name='meeting_followups_created',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User, related_name='meeting_followups_updated',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.Meeting_follow_up 
    
    class Meta:
        verbose_name_plural='2. Meeting Follow_Up'

 