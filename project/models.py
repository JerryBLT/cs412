# file: project/models.py
# author: Jerry Teixeira (jerrybt@bu.edu), 04/17/26
# description: Models for Clinical Research Project app. Defines Study, Participant, Enrollment, and Visit data structures for research operations.


from django.db import models

# Create your models here.


class Study(models.Model):
    """Stores information about a research study."""
    title = models.CharField(max_length=200)  # Study title
    protocol_number = models.CharField(max_length=50)  # Unique protocol identifier
    description = models.TextField()  # Study description
    status = models.CharField(max_length=50)  # e.g., 'active', 'completed'

    def __str__(self):
        """String representation of the Study."""
        return self.title



class Participant(models.Model):
    """Stores participant information for a study."""
    first_name = models.CharField(max_length=100)  # Participant's first name
    last_name = models.CharField(max_length=100)  # Participant's last name
    date_of_birth = models.DateField()  # Date of birth
    contact_info = models.CharField(max_length=200)  # Email or phone
    status = models.CharField(max_length=50)  # e.g., 'active', 'withdrawn'

    def __str__(self):
        """String representation of the Participant."""
        return f"{self.first_name} {self.last_name}"



class Enrollment(models.Model):
    """Represents a participant's enrollment in a study."""
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)  # Link to participant
    study = models.ForeignKey(Study, on_delete=models.CASCADE)  # Link to study
    consent_date = models.DateField()  # Date consent was given
    screening_status = models.CharField(max_length=50)  # e.g., 'eligible', 'ineligible'
    enrollment_date = models.DateField()  # Date of enrollment

    def __str__(self):
        """String representation of the Enrollment."""
        return f"{self.participant} in {self.study}"



class Visit(models.Model):
    """Represents a scheduled study visit for an enrollment."""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)  # Link to enrollment
    visit_date = models.DateTimeField()  # Date and time of visit
    visit_type = models.CharField(max_length=100)  # e.g., 'screening', 'follow-up'
    status = models.CharField(max_length=50)  # e.g., 'scheduled', 'completed', 'canceled'
    notes = models.TextField()  # Staff notes

    def __str__(self):
        """String representation of the Visit."""
        return f"{self.visit_type} on {self.visit_date}"


# Might Delete this model later!!
class VisitDocument(models.Model):
    """Stores files or records related to a visit."""
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)  # Link to visit
    title = models.CharField(max_length=200)  # Document title
    file = models.FileField(upload_to='documents/')  # Uploaded file
    description = models.TextField()  # Description of the document

    def __str__(self):
        """String representation of the VisitDocument."""
        return self.title