from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from utility.models import Category, City, Locality, RequirementType


# =======================
#  Staff
# =======================
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# =======================
#  Response
# =======================
class Response(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("Follow_Up", "Follow_Up"),
        ("Not_received", "Not Received"),
        ("Software_company", "Software Company"),
        ("For_job", "For Job"),
        ("Training", "Training"),
        ("Fake_lead", "Fake Lead"),
        ("Deal_close", "Deal Close"),
    ]

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Response Status"
    )
    contact_no = models.CharField(max_length=16, null=True, blank=True, unique=True)
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    contact_persone = models.CharField(max_length=500, blank=True, null=True)
    meeting_follow = models.DateTimeField(blank=True, null=True, verbose_name="Meeting Date & Time")

    business_name = models.CharField(max_length=500, blank=True, null=True)
    business_category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    requirement_types = models.ManyToManyField(
        RequirementType,
        blank=True,
        related_name='meetings'
    )
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.CASCADE)
    locality_city = models.ForeignKey(Locality, blank=True, null=True, on_delete=models.CASCADE)

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
        if self.contact_no:
            self.contact_no = self.contact_no.replace(" ", "")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"MR{str(self.id).zfill(3)}"+ '--' + self.contact_no

    class Meta:
        verbose_name_plural = '1. Responses'


# =======================
#  Meeting
# =======================
class Meeting(models.Model):
    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='meetings')
    status = models.CharField(max_length=25, choices=MEETING_STATUS_CHOICES, verbose_name="Meeting Status")
    meeting_date = models.DateTimeField(blank=True, null=True, verbose_name="Meeting Date & Time")
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Meeting {self.id} - {self.status}"

    class Meta:
        verbose_name_plural = "2. Meetings"


# =======================
#  Comment
# =======================
class Comment(models.Model):
    response = models.ForeignKey(Response, blank=True, null=True, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=500, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='comments_created',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User, related_name='comments_updated',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Comment {self.id} - {self.comment[:25] if self.comment else ''}"

    class Meta:
        verbose_name_plural = "3. Comments"


# =======================
#  Voice Recording
# =======================
class VoiceRecording(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='voice_recordings')
    file = models.FileField(upload_to='call_recordings/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Voice Recording for {self.response} ({self.uploaded_at.strftime('%d-%m-%Y %H:%M')})"

    class Meta:
        verbose_name_plural = "4. Voice Recordings"
