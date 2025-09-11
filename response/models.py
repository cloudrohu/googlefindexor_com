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
    status = models.ForeignKey(Call_Status, blank=True, null=True, on_delete=models.CASCADE)
    meeting_follow = models.DateTimeField(blank=True, null=True, verbose_name="Meeting Date & Time")
    
    contact_no = models.CharField(max_length=16, null=True, blank=True, unique=True)
    comment = models.CharField(max_length=500, null=True, blank=True)
    contact_persone = models.CharField(max_length=500,blank=True, null=True,)
    business_name = models.CharField(max_length=500,blank=True, null=True,)
    business_category = models.ForeignKey(Category,blank=True, null=True , on_delete=models.CASCADE)
    requirement_types = models.ManyToManyField('utility.RequirementType',blank=True,related_name='meetings' )  
    city = models.ForeignKey(City,blank=True, null=True , on_delete=models.CASCADE)
    locality_city= models.ForeignKey(Locality,blank=True, null=True , on_delete=models.CASCADE)


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
        return f"MR{str(self.id).zfill(3)}"


    class Meta:
        verbose_name_plural = '1. Response'

# -------------------------------------------------------------------------------------------------------------
class Meeting(models.Model):
    MEETING_STATUS_CHOICES = [
        ("None", "None"),
        ("New Meeting", "New Meeting"),
        ("Deal Done", "Deal Done"),
        ("Re Meeting", "Re Meeting"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(
        max_length=25,
        choices=MEETING_STATUS_CHOICES,
        default="None",
        verbose_name="Meeting Status"
    )
    response = models.ForeignKey("Response", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Meeting {self.id} - {self.status}"

    class Meta:
        verbose_name_plural = "2. Meeting"


# -------------------------------------------------------------------------------------------------------------
class Followup(models.Model):
    Followup_STATUS_CHOICES = [
        ("None ", "None "),
        ("New ", "New "),
        ("2ND TIME", "2ND TIME"),
        ("HOT", "HOT"),
        ("COOL", "COOL"),
    ]
    status = models.CharField(
        max_length=25,
        choices=Followup_STATUS_CHOICES,
        default="None",
        verbose_name="Followup Status"
    )
    response = models.ForeignKey(Response,blank=True, null=True , on_delete=models.CASCADE)   

    def __str__(self):
        return f"Followup {self.id} - {self.status}"
   
    
    class Meta:
        verbose_name_plural='3.Follow_Up'


 