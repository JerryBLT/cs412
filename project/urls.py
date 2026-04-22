from django.urls import path
from .views import *

# URL patterns for all main project views (CRUD + navigation)
urlpatterns = [
    # Dashboard
    path("", DashboardView.as_view(), name="project_dashboard"),

    # Study CRUD
    path("studies/", StudyListView.as_view(), name="project_study_list"),
    path("studies/<int:study_id>/", StudyDetailView.as_view(), name="project_study_detail"),
    path("studies/add/", StudyCreateView.as_view(), name="project_study_add"),
    path("studies/<int:study_id>/edit/", StudyUpdateView.as_view(), name="project_study_edit"),
    path("studies/<int:study_id>/delete/", StudyDeleteView.as_view(), name="project_study_delete"),

    # Participant CRUD
    path("participants/", ParticipantListView.as_view(), name="project_participant_list"),
    path("participants/<int:participant_id>/", ParticipantDetailView.as_view(), name="project_participant_detail"),
    path("participants/add/", ParticipantCreateView.as_view(), name="project_participant_add"),
    path("participants/<int:participant_id>/edit/", ParticipantUpdateView.as_view(), name="project_participant_edit"),

    # Visit CRUD and calendar
    path("calendar/", VisitCalendarView.as_view(), name="project_visit_calendar"),
    path("visits/<int:visit_id>/", VisitDetailView.as_view(), name="project_visit_detail"),
    path("visits/add/", VisitCreateView.as_view(), name="project_visit_add"),
    path("visits/<int:visit_id>/edit/", VisitUpdateView.as_view(), name="project_visit_edit"),

    # Enrollment CRUD
    path("enrollments/add/", EnrollmentCreateView.as_view(), name="project_enrollment_add"),
    path("enrollments/<int:enrollment_id>/edit/", EnrollmentUpdateView.as_view(), name="project_enrollment_edit"),

    # Scheduling workspace
    path("scheduling/", SchedulingHubView.as_view(), name="project_scheduling_hub"),
]
