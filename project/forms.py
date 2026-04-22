# file: project/forms.py
# Author: Jerry Teixeira (jerrybt@bu.edu), 04/20/2026
# Description: Model forms for create/update operations for Study, Participant, Enrollment, Visit

from django import forms
from .models import Study, Participant, Enrollment, Visit

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ["title", "protocol_number", "description", "status"]

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["first_name", "last_name", "date_of_birth", "contact_info", "status"]

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["participant", "study", "consent_date", "screening_status", "enrollment_date"]

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ["enrollment", "visit_date", "visit_type", "status", "notes"]
