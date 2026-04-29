
from django.db.models import Count, Q
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from .models import Enrollment, Participant, Study, Visit, VisitDocument
from .forms import ParticipantForm, EnrollmentForm, VisitForm, StudyForm, ParticipantSelfEditForm, VisitDocumentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# ================= Permission Mixins =================
class CoordinatorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    '''Ensures that the user is a coordinator to access coordinator-specific views.'''
    def test_func(self):
        return hasattr(self.request.user, 'userprofile') and \
               self.request.user.userprofile.role == 'coordinator'

class ParticipantRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    '''Ensures that the user is a participant to access participant-specific views.'''
    def test_func(self):
        return hasattr(self.request.user, 'userprofile') and \
               self.request.user.userprofile.role == 'participant'


# --- VisitDocument Upload ---
class VisitDocumentCreateView(CoordinatorRequiredMixin, CreateView):
    '''Handles uploading a document related to a specific visit with a form.'''
    model = VisitDocument
    form_class = VisitDocumentForm
    template_name = "project/object_form.html"

    def dispatch(self, request, *args, **kwargs):
        '''Overrides dispatch to set the visit object based on the visit_id URL parameter for use in form processing and context.'''
        self.visit = Visit.objects.get(pk=kwargs["visit_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        '''Overrides form_valid to set the visit foreign key on the VisitDocument before saving.'''
        form.instance.visit = self.visit
        return super().form_valid(form)

    def get_success_url(self):
        '''Redirects to the visit detail page after successful document upload.'''
        return reverse("project_visit_detail", kwargs={"visit_id": self.visit.id})

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the visit document upload form.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Upload Visit Document"
        context["cancel_url"] = reverse("project_visit_detail", kwargs={"visit_id": self.visit.id})
        context["submit_label"] = "Upload Document"
        return context


# --- CRUD: Study Create ---
class StudyCreateView(CoordinatorRequiredMixin, CreateView):
    '''Handles creation of a new study record with a form.'''
    model = Study
    form_class = StudyForm
    template_name = "project/object_form.html"

    def get_success_url(self):
        '''Redirects to the study list page after successful creation.'''
        return reverse_lazy("project_study_list")

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the study creation form.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Study"
        context["cancel_url"] = reverse_lazy("project_study_list")
        context["submit_label"] = "Create Study"
        return context

# --- CRUD: Study Update ---
class StudyUpdateView(CoordinatorRequiredMixin, UpdateView):
    '''Handles updating an existing study record with a form.'''
    model = Study
    form_class = StudyForm
    template_name = "project/object_form.html"
    pk_url_kwarg = "study_id"

    def get_success_url(self):
        '''Redirects to the study detail page after successful update.'''
        return reverse_lazy("project_study_detail", kwargs={"study_id": self.object.id})

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the study update form.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Study"
        context["cancel_url"] = reverse_lazy("project_study_detail", kwargs={"study_id": self.object.id})
        context["submit_label"] = "Save Changes"
        return context

# --- CRUD: Study Delete ---
class StudyDeleteView(CoordinatorRequiredMixin, DeleteView):
    '''Handles deletion of a study record with confirmation.'''
    model = Study
    template_name = "project/confirm_delete.html"
    pk_url_kwarg = "study_id"

    def get_success_url(self):
        '''Redirects to the study list view after successful deletion.'''
        return reverse_lazy("project_study_list")

    def get_context_data(self, **kwargs):
        '''Overrides context to include study title and cancel URL for the delete confirmation page.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Study"
        context["object_type"] = "study"
        context["object_name"] = self.object.title
        context["cancel_url"] = reverse_lazy("project_study_detail", kwargs={"study_id": self.object.id})
        return context

# --- CRUD: Enrollment Update ---
class EnrollmentUpdateView(CoordinatorRequiredMixin, UpdateView):
    '''Handles updating an existing enrollment record with a form.'''
    model = Enrollment
    form_class = EnrollmentForm
    template_name = "project/object_form.html"
    pk_url_kwarg = "enrollment_id"

    def get_success_url(self):
        '''Redirects to the participant detail page after successful update.'''
        return reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.participant.id})

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the enrollment edit form. '''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Enrollment"
        context["cancel_url"] = reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.participant.id})
        context["submit_label"] = "Save Changes"
        return context

# --- CRUD: Enrollment Create ---
class EnrollmentCreateView(CoordinatorRequiredMixin, CreateView):
    '''Handles creation of a new enrollment record with a form.'''
    model = Enrollment
    form_class = EnrollmentForm
    template_name = "project/object_form.html"

    def get_success_url(self):
        '''Redirects to the participant detail page after successful creation.'''
        return reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.participant.id})

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the enrollment creation form.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Enrollment"
        context["cancel_url"] = reverse_lazy("project_participant_list")
        context["submit_label"] = "Create Enrollment"
        return context

# --- CRUD: Visit Create ---
class VisitCreateView(CoordinatorRequiredMixin, CreateView):
    '''Handles creation of a new visit record with a form.'''
    model = Visit
    form_class = VisitForm
    template_name = "project/object_form.html"

    def get_success_url(self):
        '''Redirects to the visit detail page after successful creation.'''
        return reverse_lazy("project_visit_detail", kwargs={"visit_id": self.object.id})

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the visit creation form.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Visit"
        context["cancel_url"] = reverse_lazy("project_visit_calendar")
        context["submit_label"] = "Create Visit"
        return context

# --- CRUD: Visit Update ---
class VisitUpdateView(CoordinatorRequiredMixin, UpdateView):
    '''Handles updating an existing visit record with a form.'''
    model = Visit
    form_class = VisitForm
    template_name = "project/object_form.html"
    pk_url_kwarg = "visit_id"

    def get_success_url(self):
        '''Redirects to the visit detail page after successful update.'''
        return reverse_lazy("project_visit_detail", kwargs={"visit_id": self.object.id})

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the visit edit form.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Visit"
        context["cancel_url"] = reverse_lazy("project_visit_detail", kwargs={"visit_id": self.object.id})
        context["submit_label"] = "Save Changes"
        return context

# --- CRUD: Participant Update ---
class ParticipantUpdateView(CoordinatorRequiredMixin, UpdateView):
    '''Handles updating an existing participant record with a form.'''
    model = Participant
    form_class = ParticipantForm
    template_name = "project/object_form.html"
    pk_url_kwarg = "participant_id"

    def get_success_url(self):
        '''Redirects to the participant detail page after successful update.'''
        return reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.id})

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the participant edit form. '''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Participant"
        context["cancel_url"] = reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.id})
        context["submit_label"] = "Save Changes"
        return context

# --- CRUD: Participant Create ---
class ParticipantCreateView(CoordinatorRequiredMixin, CreateView):
    '''Handles creation of a new participant record with a form.'''
    model = Participant
    form_class = ParticipantForm
    template_name = "project/object_form.html"

    def get_success_url(self):
        '''Redirects to the participant detail page after successful creation.'''
        return reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.id})

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the participant creation form.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Participant"
        context["cancel_url"] = reverse_lazy("project_participant_list")
        context["submit_label"] = "Create Participant"
        return context

# -- CRUD: Participant Delete ---
class ParticipantDeleteView(CoordinatorRequiredMixin, DeleteView):
    '''Handles deletion of a participant record with confirmation.'''
    model = Participant
    template_name = "project/confirm_delete.html"
    pk_url_kwarg = "participant_id"

    def get_success_url(self):
        '''Redirects to the participant list view after successful deletion.'''
        return reverse_lazy("project_participant_list")

    def get_context_data(self, **kwargs):
        '''Overrides context to include participant name and cancel URL for the delete confirmation page.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Participant"
        context["object_type"] = "participant"
        context["object_name"] = f"{self.object.first_name} {self.object.last_name}"
        context["cancel_url"] = reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.id})
        return context

# --- Dashboard ---
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "project/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        '''Redirects participants to their profile page if they try to access the dashboard, otherwise allows coordinators to view the dashboard.'''
        if hasattr(request.user, 'userprofile'):
            if request.user.userprofile.role == 'participant':
                return redirect('my_profile')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        '''Overrides context to include key metrics and recent activity for the dashboard view.'''
        context = super().get_context_data(**kwargs)
        studies = Study.objects.annotate(enrollment_count=Count("enrollment"))
        participants = Participant.objects.order_by("last_name", "first_name")
        visits = Visit.objects.select_related(
            "enrollment",
            "enrollment__participant",
            "enrollment__study",
        ).order_by("visit_date")
        context.update({
            "metrics": [
                {"label": "Studies", "value": studies.count(), "detail": "Tracked protocols"},
                {"label": "Participants", "value": participants.count(), "detail": "Participant records"},
                {"label": "Enrollments", "value": Enrollment.objects.count(), "detail": "Study assignments"},
                {"label": "Visits", "value": visits.count(), "detail": "Scheduled visits"},
            ],
            "recent_visits": visits[:5],
            "recent_participants": participants[:5],
            "studies": studies[:6],
        })
        return context

class StudyListView(CoordinatorRequiredMixin, ListView):
    model = Study
    template_name = "project/study_list.html"
    context_object_name = "studies"

    def get_queryset(self):
        '''Returns a queryset of studies annotated with enrollment count, ordered by title for the study list view.'''
        return Study.objects.annotate(enrollment_count=Count("enrollment")).order_by("title")

class StudyDetailView(CoordinatorRequiredMixin, DetailView):
    model = Study
    template_name = "project/study_detail.html"
    context_object_name = "study"
    pk_url_kwarg = "study_id"

    def get_context_data(self, **kwargs):
        '''Overrides context to include enrollments and visits for the study detail view.'''
        context = super().get_context_data(**kwargs)
        study = self.object
        context["enrollments"] = (
            Enrollment.objects.filter(study=study)
            .select_related("participant")
            .order_by("participant__last_name", "participant__first_name")
        )
        context["visits"] = (
            Visit.objects.filter(enrollment__study=study)
            .select_related("enrollment", "enrollment__participant")
            .order_by("visit_date")
        )
        return context

class ParticipantListView(CoordinatorRequiredMixin, ListView):
    model = Participant
    template_name = "project/participant_list.html"
    context_object_name = "participants"

    def get_queryset(self):
        '''Returns a filtered queryset of participants based on search query, study filter, and screening status filter for the participant list view.'''
        queryset = Participant.objects.all()
        search_query = self.request.GET.get('search', '')
        study_id = self.request.GET.get('study', '')
        screening_status = self.request.GET.get('screening_status', '')

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
            )
        if study_id:
            queryset = queryset.filter(enrollment__study_id=study_id)
        if screening_status:
            queryset = queryset.filter(enrollment__screening_status=screening_status)
        return queryset.distinct().order_by("last_name", "first_name")

    def get_context_data(self, **kwargs):
        '''Overrides context to include enrollments, studies, screening status choices, and current filter values for the participant list view.'''
        context = super().get_context_data(**kwargs)
        context["enrollments"] = Enrollment.objects.select_related("participant", "study")
        context["studies"] = Study.objects.all()
        context["screening_status_choices"] = Enrollment.SCREENING_STATUS_CHOICES
        context["search_query"] = self.request.GET.get('search', '')
        context["selected_study"] = self.request.GET.get('study', '')
        context["selected_screening_status"] = self.request.GET.get('screening_status', '')
        return context

class ParticipantDetailView(CoordinatorRequiredMixin, DetailView):
    model = Participant
    template_name = "project/participant_detail.html"
    context_object_name = "participant"
    pk_url_kwarg = "participant_id"

    def get_context_data(self, **kwargs):
        '''Overrides context to include enrollments and visits for the participant detail view.'''
        context = super().get_context_data(**kwargs)
        participant = self.object
        context["enrollments"] = (
            Enrollment.objects.filter(participant=participant)
            .select_related("study")
            .order_by("-enrollment_date", "-consent_date")
        )
        context["visits"] = (
            Visit.objects.filter(enrollment__participant=participant)
            .select_related("enrollment", "enrollment__study")
            .order_by("visit_date")
        )
        return context

class VisitCalendarView(CoordinatorRequiredMixin, ListView):
    '''Displays a calendar view of all visits, with related enrollment, participant, and study data for context.'''
    model = Visit
    template_name = "project/visit_calendar.html"
    context_object_name = "visits"

    def get_queryset(self):
        '''Returns all visits ordered by visit date, with related enrollment, participant, and study data for efficient access in the calendar view.'''
        return Visit.objects.select_related(
            "enrollment",
            "enrollment__participant",
            "enrollment__study",
        ).order_by("visit_date")

class VisitDetailView(CoordinatorRequiredMixin, DetailView):
    '''Displays detailed information about a specific visit, including related enrollment, participant, study, and associated documents.'''
    model = Visit
    template_name = "project/visit_detail.html"
    context_object_name = "visit"
    pk_url_kwarg = "visit_id"

    def get_queryset(self):
        '''Overrides the default queryset to include related enrollment, participant, and study data for efficient access in the visit detail view.'''
        return Visit.objects.select_related(
            "enrollment",
            "enrollment__participant",
            "enrollment__study",
        )

    def get_context_data(self, **kwargs):
        '''Overrides context to include related documents for the visit detail view.'''
        context = super().get_context_data(**kwargs)
        context["documents"] = self.object.visitdocument_set.order_by("title")
        return context

class SchedulingHubView(CoordinatorRequiredMixin, TemplateView):
    template_name = "project/scheduling_hub.html"

    def get_context_data(self, **kwargs):
        '''Overrides context to include upcoming visits and recent studies for the scheduling hub dashboard.'''
        context = super().get_context_data(**kwargs)
        context["visits"] = Visit.objects.select_related(
            "enrollment",
            "enrollment__participant",
            "enrollment__study",
        ).order_by("visit_date")[:8]
        context["studies"] = Study.objects.order_by("title")[:8]
        return context

# ================= Participant-Specific Views =================
class MyProfileView(ParticipantRequiredMixin, DetailView):
    model = Participant
    template_name = "project/my_profile.html"

    def get_object(self):
        '''Returns the Participant object associated with the logged-in user.'''
        return self.request.user.userprofile.participant

    def get_context_data(self, **kwargs):
        '''Overrides context to include counts of enrollments and visits for the participant.'''
        context = super().get_context_data(**kwargs)
        participant = self.get_object()
        context["enrollments_count"] = Enrollment.objects.filter(participant=participant).count()
        context["visits_count"] = Visit.objects.filter(enrollment__participant=participant).count()
        return context

class MyEnrollmentsView(ParticipantRequiredMixin, ListView):
    model = Enrollment
    template_name = "project/my_enrollments.html"
    context_object_name = "enrollments"

    def get_queryset(self):
        '''Returns enrollments for the logged-in participant, annotated with study title for display.'''
        participant = self.request.user.userprofile.participant
        return Enrollment.objects.filter(participant=participant).select_related("study").order_by("-enrollment_date")

class MyVisitsView(ParticipantRequiredMixin, ListView):
    model = Visit
    template_name = "project/my_visits.html"
    context_object_name = "visits"

    def get_queryset(self):
        '''Returns visits for the logged-in participant, annotated with study title and related documents for display.'''
        participant = self.request.user.userprofile.participant
        return Visit.objects.filter(
            enrollment__participant=participant
        ).select_related(
            "enrollment",
            "enrollment__study"
        ).order_by("visit_date")

    def get_context_data(self, **kwargs):
        '''Overrides context to annotate visits with study title and related documents for template display.'''
        context = super().get_context_data(**kwargs)
        # Annotate each visit with study_title and documents for template use
        for visit in context["visits"]:
            visit.study_title = visit.enrollment.study.title if visit.enrollment and visit.enrollment.study else ""
            visit.documents = visit.visitdocument_set.all().order_by("title")
        return context

class HomeView(TemplateView):
    '''Public homepage view that redirects authenticated users to the dashboard, otherwise shows a welcome page.'''
    template_name = "project/home.html"

    def dispatch(self, request, *args, **kwargs):
        '''Redirect authenticated users to dashboard, otherwise show homepage.'''
        if request.user.is_authenticated:
            return redirect("project_dashboard")
        return super().dispatch(request, *args, **kwargs)

class MyProfileUpdateView(ParticipantRequiredMixin, UpdateView):
    '''Allows participants to update their own profile information (phone and email) with a form.'''
    model = Participant
    form_class = ParticipantSelfEditForm
    template_name = "project/object_form.html"

    def get_object(self):
        '''Returns the Participant object associated with the logged-in user.'''
        return self.request.user.userprofile.participant

    def get_success_url(self):
        '''Redirect back to the profile page after successful update.'''
        return reverse_lazy("my_profile")

    def get_context_data(self, **kwargs):
        '''Overrides context to set page title and button labels for the profile edit form.'''
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit My Profile"
        context["cancel_url"] = reverse_lazy("my_profile")
        context["submit_label"] = "Save Changes"
        return context

