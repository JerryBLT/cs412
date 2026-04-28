# file: project/models.py
# author: Jerry Teixeira (jerrybt@bu.edu), 04/17/26
# description: Models for Clinical Research Project app. Defines Study, Participant, Enrollment, and Visit data structures for research operations.


from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Study(models.Model):
    """Stores information about a research study."""
    title = models.CharField(max_length=200)  # Study title
    protocol_number = models.CharField(max_length=50)  # Unique protocol identifier
    description = models.TextField()  # Study description
    STUDY_STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('paused', 'Paused'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STUDY_STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        """String representation of the Study."""
        return self.title



class Participant(models.Model):
    """Stores participant information for a study."""
    first_name = models.CharField(max_length=100)  # Participant's first name
    last_name = models.CharField(max_length=100)  # Participant's last name
    date_of_birth = models.DateField()  # Date of birth
    age = models.PositiveIntegerField(null=True, blank=True)  # Age (optional, can be calculated from DOB)
    sex = models.CharField(
        max_length=20,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not_to_say', 'Prefer not to say')],
        default='prefer_not_to_say',
    )  # Sex
    phone = models.CharField(max_length=20, blank=True)  # Phone number
    email = models.EmailField(max_length=254, blank=True)  # Email address
    # contact_info = models.CharField(max_length=200)  # Deprecated: use phone/email
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('withdrawn', 'Withdrawn'),
        ('completed', 'Completed'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        """String representation of the Participant."""
        return f"{self.first_name} {self.last_name}"



class Enrollment(models.Model):
    """Represents a participant's enrollment in a study."""
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)  # Link to participant
    study = models.ForeignKey(Study, on_delete=models.CASCADE)  # Link to study
    consent_date = models.DateField()  # Date consent was given
    SCREENING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('eligible', 'Eligible'),
        ('ineligible', 'Ineligible'),
        ('screen_failed', 'Screen Failed'),
    ]
    screening_status = models.CharField(
        max_length=20,
        choices=SCREENING_STATUS_CHOICES,
        default='pending'
    )
    enrollment_date = models.DateField()  # Date of enrollment

    def __str__(self):
        """String representation of the Enrollment."""
        return f"{self.participant} in {self.study}"



class Visit(models.Model):
    """Represents a scheduled study visit for an enrollment."""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)  # Link to enrollment
    visit_date = models.DateTimeField()  # Date and time of visit
    visit_type = models.CharField(max_length=100)  # e.g., 'screening', 'follow-up'
    VISIT_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('missed', 'Missed'),
    ]
    status = models.CharField(
        max_length=20,
        choices=VISIT_STATUS_CHOICES,
        default='scheduled'
    )
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
        return self.title

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('coordinator', 'Coordinator'),
        ('participant', 'Participant'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    participant = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"