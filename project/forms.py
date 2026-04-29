
# file: project/forms.py
# Author: Jerry Teixeira (jerrybt@bu.edu), 04/20/2026
# Description: Model forms for create/update operations for Study, Participant, Enrollment, Visit

from django import forms
from .models import Study, Participant, Enrollment, Visit, VisitDocument

class VisitDocumentForm(forms.ModelForm):
    class Meta:
        model = VisitDocument
        fields = ["title", "file", "description"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ["title", "protocol_number", "description", "status"]

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["first_name", "last_name", "date_of_birth", "sex", "phone", "email", "status"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["participant", "study", "consent_date", "screening_status", "enrollment_date"]

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ["enrollment", "visit_date", "visit_type", "status", "notes"]

class ParticipantSelfEditForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["phone", "email"]
