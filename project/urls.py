
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

# URL patterns for all main project views (CRUD + navigation)
urlpatterns = [
    # VisitDocument upload
    path("visits/<int:visit_id>/documents/add/", VisitDocumentCreateView.as_view(), name="visit_document_create"),
    # Homepage and Dashboard
    path("", HomeView.as_view(), name="project_home"),
    path("dashboard/", DashboardView.as_view(), name="project_dashboard"),

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
    path("participants/<int:participant_id>/delete/", ParticipantDeleteView.as_view(), name="project_participant_delete"),

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

    # Participant-only views
    path("my/profile/", MyProfileView.as_view(), name="my_profile"),
    path("my/profile/edit/", MyProfileUpdateView.as_view(), name="my_profile_edit"),
    path("my/enrollments/", MyEnrollmentsView.as_view(), name="my_enrollments"),
    path("my/visits/", MyVisitsView.as_view(), name="my_visits"),

    # Authentication views
    path("login/", auth_views.LoginView.as_view(template_name="project/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="logout_confirmation"), name="logout"),
    path("logout_confirmation/", TemplateView.as_view(template_name="project/logged_out.html"), name="logout_confirmation"),
]
