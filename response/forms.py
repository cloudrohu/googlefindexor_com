from django import forms
from .models import Response, Meeting, Followup
from utility.models import RequirementType


# ------------------------------
#  Response Form (Create / Update)
# ------------------------------
class ResponseCreateForm(forms.ModelForm):
    requirement_types = forms.ModelMultipleChoiceField(
        queryset=RequirementType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="आवश्यकता के प्रकार",
        required=False
    )

    class Meta:
        model = Response
        fields = [
            'business_name', 'contact_persone', 'contact_no',
            'business_category', 'city', 'locality_city',
            'requirement_types', 'status', 'comment', 'voice_recording'
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_persone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={
                'placeholder': '10 अंकों का नंबर',
                'class': 'form-control'
            }),
            'business_category': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'locality_city': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'voice_recording': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ------------------------------
#  Meeting Form
# ------------------------------
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['status', 'meeting_date', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'meeting_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }


# ------------------------------
#  Followup Form
# ------------------------------
class FollowupForm(forms.ModelForm):
    class Meta:
        model = Followup
        fields = ['status', 'follow', 'response']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'follow': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'response': forms.Select(attrs={'class': 'form-control'}),
        }
