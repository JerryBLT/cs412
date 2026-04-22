from django.db.models import Count
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Enrollment, Participant, Study, Visit
from .forms import ParticipantForm, EnrollmentForm, VisitForm, StudyForm

# --- CRUD: Study Create ---
class StudyCreateView(CreateView):
    model = Study
    form_class = StudyForm
    template_name = "project/object_form.html"

    def get_success_url(self):
        return reverse_lazy("project_study_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Study"
        context["cancel_url"] = reverse_lazy("project_study_list")
        context["submit_label"] = "Create Study"
        return context

# --- CRUD: Study Update ---
class StudyUpdateView(UpdateView):
    model = Study
    form_class = StudyForm
    template_name = "project/object_form.html"
    pk_url_kwarg = "study_id"

    def get_success_url(self):
        return reverse_lazy("project_study_detail", kwargs={"study_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Study"
        context["cancel_url"] = reverse_lazy("project_study_detail", kwargs={"study_id": self.object.id})
        context["submit_label"] = "Save Changes"
        return context

# --- CRUD: Study Delete ---
class StudyDeleteView(DeleteView):
    model = Study
    template_name = "project/confirm_delete.html"
    pk_url_kwarg = "study_id"

    def get_success_url(self):
        return reverse_lazy("project_study_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Study"
        context["object_type"] = "study"
        context["object_name"] = self.object.title
        context["cancel_url"] = reverse_lazy("project_study_detail", kwargs={"study_id": self.object.id})
        return context

# --- CRUD: Enrollment Update ---
class EnrollmentUpdateView(UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = "project/object_form.html"
    pk_url_kwarg = "enrollment_id"

    def get_success_url(self):
        return reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.participant.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Enrollment"
        context["cancel_url"] = reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.participant.id})
        context["submit_label"] = "Save Changes"
        return context

# --- CRUD: Enrollment Create ---
class EnrollmentCreateView(CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = "project/object_form.html"

    def get_success_url(self):
        return reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.participant.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Enrollment"
        context["cancel_url"] = reverse_lazy("project_participant_list")
        context["submit_label"] = "Create Enrollment"
        return context

# --- CRUD: Visit Create ---
class VisitCreateView(CreateView):
    model = Visit
    form_class = VisitForm
    template_name = "project/object_form.html"

    def get_success_url(self):
        return reverse_lazy("project_visit_detail", kwargs={"visit_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Visit"
        context["cancel_url"] = reverse_lazy("project_visit_calendar")
        context["submit_label"] = "Create Visit"
        return context

# --- CRUD: Visit Update ---
class VisitUpdateView(UpdateView):
    model = Visit
    form_class = VisitForm
    template_name = "project/object_form.html"
    pk_url_kwarg = "visit_id"

    def get_success_url(self):
        return reverse_lazy("project_visit_detail", kwargs={"visit_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Visit"
        context["cancel_url"] = reverse_lazy("project_visit_detail", kwargs={"visit_id": self.object.id})
        context["submit_label"] = "Save Changes"
        return context

# --- CRUD: Participant Update ---
class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "project/object_form.html"
    pk_url_kwarg = "participant_id"

    def get_success_url(self):
        return reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Participant"
        context["cancel_url"] = reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.id})
        context["submit_label"] = "Save Changes"
        return context


# --- CRUD: Participant Create ---
class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "project/object_form.html"

    def get_success_url(self):
        return reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Participant"
        context["cancel_url"] = reverse_lazy("project_participant_list")
        context["submit_label"] = "Create Participant"
        return context

# -- CRUD: Participant Delete ---
class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = "project/confirm_delete.html"
    pk_url_kwarg = "participant_id"

    def get_success_url(self):
        return reverse_lazy("project_participant_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Participant"
        context["object_type"] = "participant"
        context["object_name"] = f"{self.object.first_name} {self.object.last_name}"
        context["cancel_url"] = reverse_lazy("project_participant_detail", kwargs={"participant_id": self.object.id})
        return context




# --- Dashboard ---
class DashboardView(TemplateView):
    template_name = "project/dashboard.html"

    def get_context_data(self, **kwargs):
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
    


class StudyListView(ListView):
    model = Study
    template_name = "project/study_list.html"
    context_object_name = "studies"

    def get_queryset(self):
        return Study.objects.annotate(enrollment_count=Count("enrollment")).order_by("title")

class StudyDetailView(DetailView):
    model = Study
    template_name = "project/study_detail.html"
    context_object_name = "study"
    pk_url_kwarg = "study_id"

    def get_context_data(self, **kwargs):
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

class ParticipantListView(ListView):
    model = Participant
    template_name = "project/participant_list.html"
    context_object_name = "participants"

    def get_queryset(self):
        return Participant.objects.order_by("last_name", "first_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enrollments"] = Enrollment.objects.select_related("participant", "study")
        return context

class ParticipantDetailView(DetailView):
    model = Participant
    template_name = "project/participant_detail.html"
    context_object_name = "participant"
    pk_url_kwarg = "participant_id"

    def get_context_data(self, **kwargs):
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

class VisitCalendarView(ListView):
    model = Visit
    template_name = "project/visit_calendar.html"
    context_object_name = "visits"

    def get_queryset(self):
        return Visit.objects.select_related(
            "enrollment",
            "enrollment__participant",
            "enrollment__study",
        ).order_by("visit_date")

class VisitDetailView(DetailView):
    model = Visit
    template_name = "project/visit_detail.html"
    context_object_name = "visit"
    pk_url_kwarg = "visit_id"

    def get_queryset(self):
        return Visit.objects.select_related(
            "enrollment",
            "enrollment__participant",
            "enrollment__study",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["documents"] = self.object.visitdocument_set.order_by("title")
        return context

class SchedulingHubView(TemplateView):
    template_name = "project/scheduling_hub.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["visits"] = Visit.objects.select_related(
            "enrollment",
            "enrollment__participant",
            "enrollment__study",
        ).order_by("visit_date")[:8]
        context["studies"] = Study.objects.order_by("title")[:8]
        return context
    
