from django import forms
from .models import (
    Company, Comment, VoiceRecording,
    Follow_Up, Faq, Meeting, Visit,
    Approx, SocialLink, Error, Images
)


# ======================================================
# COMPANY FORM
# ======================================================
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "category", "company_name", "contact_person", "contact_no",
            "city", "locality", "address", "website", "google_map",
            "description", "image", "call_status", "call_comment",
            "googlemap_status", "find_form", "assigned_to"
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Company Name"}),
            "contact_person": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact Person"}),
            "contact_no": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact Number"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Address"}),
            "website": forms.TextInput(attrs={"class": "form-control", "placeholder": "Website URL"}),
            "google_map": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Google Map URL"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Short Description"}),
            "call_comment": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Call Remarks"}),
        }


# ======================================================
# COMMENT FORM
# ======================================================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Write a comment..."}),
        }


# ======================================================
# VOICE RECORDING FORM
# ======================================================
class VoiceRecordingForm(forms.ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ["file", "note"]
        widgets = {
            "note": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional note"}),
        }


# ======================================================
# FOLLOW UP FORM
# ======================================================
class FollowUpForm(forms.ModelForm):
    class Meta:
        model = Follow_Up
        fields = ["follow_up", "comment"]
        widgets = {
            "follow_up": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Follow-up remarks"}),
        }


# ======================================================
# FAQ FORM
# ======================================================
class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ["questions", "answers"]
        widgets = {
            "questions": forms.TextInput(attrs={"class": "form-control", "placeholder": "Question"}),
            "answers": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Answer"}),
        }


# ======================================================
# MEETING FORM
# ======================================================
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ["meeting", "comment"]
        widgets = {
            "meeting": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Meeting comments"}),
        }


# ======================================================
# VISIT FORM
# ======================================================
class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Visit remarks"}),
        }


# ======================================================
# APPROX FORM
# ======================================================
class ApproxForm(forms.ModelForm):
    class Meta:
        model = Approx
        fields = ["category", "city", "locality", "title"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Approx Title"}),
        }


# ======================================================
# SOCIAL LINK FORM
# ======================================================
class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ["company", "socia_site", "link"]
        widgets = {
            "link": forms.TextInput(attrs={"class": "form-control", "placeholder": "Social link URL"}),
        }


# ======================================================
# ERROR FORM
# ======================================================
class ErrorForm(forms.ModelForm):
    class Meta:
        model = Error
        fields = ["title", "error"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Error Title"}),
            "error": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Error Details"}),
        }


# ======================================================
# IMAGES FORM
# ======================================================
class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ["title", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Image Title"}),
        }
