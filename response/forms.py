from django import forms
from .models import Response, Meeting, Comment, VoiceRecording
from utility.models import RequirementType


# =================================================================
#  Response Form (Create / Update)
# =================================================================
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
            'business_name',
            'contact_persone',
            'contact_no',
            'business_category',
            'city',
            'locality_city',
            'requirement_types',
            'status'
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
        }

    def clean_contact_no(self):
        """
        ✅ Contact number ko clean kare (spaces remove)
        """
        contact_no = self.cleaned_data.get('contact_no', '')
        return contact_no.replace(" ", "") if contact_no else contact_no


# =================================================================
#  Meeting Form
# =================================================================
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['status', 'meeting_date', 'assigned_to', 'comment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'meeting_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


# =================================================================
#  Comment Form
# =================================================================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Add your comment here...'
            }),
        }


# =================================================================
#  Voice Recording Form
# =================================================================
class VoiceRecordingForm(forms.ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ['file', 'note']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional note (e.g. Call with client)'
            }),
        }
