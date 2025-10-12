from django import forms
from django.forms import ModelForm
from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Follow_Up, Images,
    Faq, Meeting
)

# ============================================================
# COMPANY FORM ✅ (Fixed)
# ============================================================
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            'category', 'status', 'followup_meeting',
            'find_form', 'googlemap_status', 'company_name', 'contact_person',
            'contact_no', 'city', 'locality', 'address', 'website',
            'google_map', 'description', 'image', 'assigned_to',
            'created_by', 'updated_by'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'google_map': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'followup_meeting': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

# ============================================================
# COMMENT FORM
# ============================================================
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['company', 'comment', 'created_by', 'updated_by']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment...'}),
        }

# ============================================================
# VOICE RECORDING FORM
# ============================================================
class VoiceRecordingForm(ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ['company', 'file', 'note', 'uploaded_by']
        widgets = {
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a note'}),
        }

# ============================================================
# VISIT FORM
# ============================================================
class VisitForm(ModelForm):
    class Meta:
        model = Visit
        fields = ['company', 'visit_for', 'visit_type', 'visit_status', 'comment', 'uploaded_by']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# ============================================================
# APPROX FORM
# ============================================================
class ApproxForm(ModelForm):
    class Meta:
        model = Approx
        fields = ['category', 'city', 'locality', 'title']

# ============================================================
# SOCIAL LINK FORM
# ============================================================
class SocialLinkForm(ModelForm):
    class Meta:
        model = SocialLink
        fields = ['company', 'socia_site', 'link']

# ============================================================
# ERROR FORM
# ============================================================
class ErrorForm(ModelForm):
    class Meta:
        model = Error
        fields = ['company', 'title', 'error']

# ============================================================
# FOLLOW UP FORM
# ============================================================
class FollowUpForm(ModelForm):
    class Meta:
        model = Follow_Up
        fields = ['company', 'follow_up', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'follow_up': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

# ============================================================
# IMAGES FORM
# ============================================================
class ImagesForm(ModelForm):
    class Meta:
        model = Images
        fields = ['product', 'title', 'image']

# ============================================================
# FAQ FORM
# ============================================================
class FaqForm(ModelForm):
    class Meta:
        model = Faq
        fields = ['company', 'questions', 'answers']
        widgets = {
            'questions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Question'}),
            'answers': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# ============================================================
# MEETING FORM
# ============================================================
class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['company', 'meeting', 'comment']
        widgets = {
            'meeting': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
