from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

from django.db import models
from django.utils.html import mark_safe
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from utility.models import Find_Form, Call_Status, SocialSite, Googlemap_Status, City, Locality,Category
from response.models import Staff



# ============================================================
# COMPANY MODEL
# ============================================================
class Company(models.Model):

    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("Follow_Up", "Follow_Up"),
        ("Not_received", "Not Received"),
        ("Not Interested", "Not Interested"),
        ("They Will Connect", "They Will Connect"),
        ("Call later", "Call later"),
        ("Call Tomorrow", "Call Tomorrow"),
        ("Switched Off", "Switched Off"),
        ("Invalid Number Off", "Invalid Number"),
    ]

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Company Status"
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    followup_meeting = models.DateTimeField(null=True, blank=True)
    find_form = models.ForeignKey(Find_Form, on_delete=models.CASCADE, null=True, blank=True)
    googlemap_status = models.ForeignKey(Googlemap_Status, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    contact_no = models.CharField(max_length=255, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    
    website = models.CharField(max_length=255, null=True, blank=True)
    google_map = models.CharField(max_length=1000, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='company_images/', null=True, blank=True)
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    slug = models.SlugField(max_length=500, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_by_user', on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='created_by_user', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = '1. Company'
        ordering = ['-create_at']

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        """Fixed: Save company correctly + auto-slug update."""
        # Step 1: Normal save (always run first)
        super().save(*args, **kwargs)

        # Step 2: Generate slug safely (only if needed)
        category_title = self.category.title if self.category else ''
        locality_name = str(self.locality) if self.locality else ''
        city_name = str(self.city) if self.city else ''
        base_slug = slugify(f"{category_title} {self.company_name} {locality_name} {city_name}")
        new_slug = f"{base_slug}-{self.id}"

        # Step 3: Update slug if changed
        if self.slug != new_slug:
            self.slug = new_slug
            super().save(update_fields=['slug'])

    def get_absolute_url(self):
        return reverse("company_details", kwargs={'id': self.id, 'slug': self.slug})

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return ""
    image_tag.short_description = 'Image'


# ============================================================
# COMMENT MODEL
# ============================================================
class Comment(models.Model):
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=500, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name='business_comments_created',   # 👈 unique
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='business_comments_updated',   # 👈 unique
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = "3. Comments"
        ordering = ['-create_at']

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            # Comment inline ke liye
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
            if hasattr(obj, 'updated_by'):
                obj.updated_by = request.user

            # VoiceRecording inline ke liye
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user

            # Visit inline ke liye
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user

            obj.save()
        formset.save_m2m()


    def __str__(self):
        return f"Comment {self.id} - {self.comment[:25] if self.comment else ''}"


# ============================================================
# VOICE RECORDING MODEL
# ============================================================
class VoiceRecording(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='voice_recordings')
    file = models.FileField(upload_to='call_recordings/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User,
        related_name='business_voice_uploaded',    # 👈 unique
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = "4. Voice Recordings"
        ordering = ['-uploaded_at']


    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            # Comment inline ke liye
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
            if hasattr(obj, 'updated_by'):
                obj.updated_by = request.user

            # VoiceRecording inline ke liye
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user

            # Visit inline ke liye
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user

            obj.save()
        formset.save_m2m()


    def __str__(self):
        return f"Voice Recording for {self.company} ({self.uploaded_at.strftime('%d-%m-%Y %H:%M')})"




class Visit(models.Model):
    VISIT_FOR_CHOICES = [
        ("Telling Meeting", "Telling Meeting"),
        ("Door To Door", "Door To Door"),
        ("Site Visit", "Site Visit"),
        ("Follow Up", "Follow Up"),
        ("Negotiation", "Negotiation"),
    ]

    VISIT_TYPE_CHOICES = [
        ("1st Visit", "1st Visit"),
        ("2nd Visit", "2nd Visit"),
        ("3rd Visit", "3rd Visit"),
        ("4th Visit", "4th Visit"),
        ("5th Visit", "5th Visit"),
        ("6th Visit", "6th Visit"),
        ("7th Visit", "7th Visit"),
        ("8th Visit", "8th Visit"),
        ("9th Visit", "9th Visit"),
        ("10th Visit", "10th Visit"),
    ]

    VISIT_STATUS_CHOICES = [
        ("Deal_Close", "Deal Close"),
        ("Meeting", "Meeting"),
        ("Follow_Up", "Follow Up"),
        ("Owner not In Office", "Owner not In Office"),
        ("Interested", "Interested"),
        ("Not Interested", "Not Interested"),
    ]

    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="visits")
    visit_for = models.CharField(max_length=50, choices=VISIT_FOR_CHOICES)
    visit_type = models.CharField(max_length=50, choices=VISIT_TYPE_CHOICES)
    visit_status = models.CharField(max_length=50, choices=VISIT_STATUS_CHOICES)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    uploaded_by = models.ForeignKey(
        User,
        related_name="visits_uploaded_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "5. Visits"
        ordering = ['-uploaded_at']


    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            # Comment inline ke liye
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
            if hasattr(obj, 'updated_by'):
                obj.updated_by = request.user

            # VoiceRecording inline ke liye
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user

            # Visit inline ke liye
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user

            obj.save()
        formset.save_m2m()


    def __str__(self):
        return f"{self.company.company_name} - {self.visit_type} ({self.visit_status})"


# ============================================================
# APPROX MODEL
# ============================================================
class Approx(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ============================================================
# SOCIAL LINK MODEL
# ============================================================
class SocialLink(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    socia_site = models.ForeignKey(SocialSite, on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=50, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link


# ============================================================
# ERROR MODEL
# ============================================================
class Error(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=500, unique=True)
    error = models.CharField(max_length=500, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



# ============================================================
# IMAGES MODEL
# ============================================================
class Images(models.Model):
    product = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.title


# ============================================================
# FAQ MODEL
# ============================================================
class Faq(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    questions = models.CharField(max_length=500, blank=True)
    answers = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.questions

class Followup(models.Model):
    FOLLOWUP_STATUS_CHOICES = [
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='followups'
    )
    status = models.CharField(max_length=25, choices=FOLLOWUP_STATUS_CHOICES, verbose_name="Followup Status")
    followup_date = models.DateTimeField(blank=True, null=True, verbose_name="Followup Date & Time")

    # 👇 FIXED: give a unique related_name
    assigned_to = models.ForeignKey(
        Staff,
        related_name='business_followup_assigned',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name='business_followup_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='business_followup_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Followup {self.id} - {self.status}"

    class Meta:
        verbose_name_plural = "3. Followups"

class Meeting(models.Model):
    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='meetings'
    )
    status = models.CharField(max_length=25, choices=MEETING_STATUS_CHOICES, verbose_name="Meeting Status")
    meeting_date = models.DateTimeField(blank=True, null=True, verbose_name="Meeting Date & Time")

    # 👇 FIXED: give a unique related_name
    assigned_to = models.ForeignKey(
        Staff,
        related_name='business_meeting_assigned',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name='business_meeting_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='business_meeting_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Meeting {self.id} - {self.status}"

    class Meta:
        verbose_name_plural = "2. Meetings"
