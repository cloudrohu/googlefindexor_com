from django import forms
from .models import Company, Comment, VoiceRecording, Visit


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['company', 'comment']


class VoiceRecordingForm(forms.ModelForm):  # ✅ This must exist
    class Meta:
        model = VoiceRecording
        fields = ['company', 'file']


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['company', 'visit_for', 'visit_type', 'visit_status', 'comment']
