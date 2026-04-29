
# file: project/forms.py
# Author: Jerry Teixeira (jerrybt@bu.edu), 04/20/2026
# Description: Model forms for create/update operations for Study, Participant, Enrollment, Visit

from django import forms
from .models import Study, Participant, Enrollment, Visit, VisitDocument

class VisitDocumentForm(forms.ModelForm):
    '''Form for uploading a document related to a specific visit. Includes fields for title, file upload, and description.'''
    class Meta:
        model = VisitDocument
        fields = ["title", "file", "description"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class StudyForm(forms.ModelForm):
    '''Form for creating or updating a study. Includes fields for title, protocol number, description, and status.'''
    class Meta:
        model = Study
        fields = ["title", "protocol_number", "description", "status"]

class ParticipantForm(forms.ModelForm):
    '''Form for creating or updating a participant. Includes fields for name, date'''
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
    '''Form for creating or updating an enrollment. Includes fields for participant, study, consent date, screening status, and enrollment date.'''
    class Meta:
        model = Enrollment
        fields = ["participant", "study", "consent_date", "screening_status", "enrollment_date"]

class VisitForm(forms.ModelForm):
    '''Form for creating or updating a visit. Includes fields for enrollment, visit date, visit type, status, and notes.'''
    class Meta:
        model = Visit
        fields = ["enrollment", "visit_date", "visit_type", "status", "notes"]

class ParticipantSelfEditForm(forms.ModelForm):
    '''Form for participants to edit their own profile information. Only includes phone and email fields.'''
    class Meta:
        model = Participant
        fields = ["phone", "email"]
