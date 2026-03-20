"""
File: voter_analytics/views.py
author: Jerry Teixeira (jerrybt@bu.edu), 03/20/26
Description: Class-based views and filtering logic for voter listing, detail, and graphs.
"""

from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

# Shared filtering + rendering helpers used by list and graph views.
class VoterFilterMixin:
    '''Provide shared filtering behavior for Voter list and graph views.'''

    def get_base_queryset(self):
        return Voter.objects.all()

    def get_filtered_queryset(self):
        # Start from all voters and apply each optional query parameter
        # only when the user supplied that filter.
        voters = self.get_base_queryset()

        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                voters = voters.filter(party_affiliation=party)

        if 'min_birth_year' in self.request.GET:
            min_birth_year = self.request.GET['min_birth_year']
            if min_birth_year:
                voters = voters.filter(date_of_birth__gte=f'{min_birth_year}-01-01')

        if 'max_birth_year' in self.request.GET:
            max_birth_year = self.request.GET['max_birth_year']
            if max_birth_year:
                voters = voters.filter(date_of_birth__lte=f'{max_birth_year}-12-31')

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voters = voters.filter(voter_score=voter_score)

        if 'v20state' in self.request.GET:
            if self.request.GET['v20state'] == '1':
                voters = voters.filter(v20state=True)

        if 'v21town' in self.request.GET:
            if self.request.GET['v21town'] == '1':
                voters = voters.filter(v21town=True)

        if 'v21primary' in self.request.GET:
            if self.request.GET['v21primary'] == '1':
                voters = voters.filter(v21primary=True)

        if 'v22general' in self.request.GET:
            if self.request.GET['v22general'] == '1':
                voters = voters.filter(v22general=True)

        if 'v23town' in self.request.GET:
            if self.request.GET['v23town'] == '1':
                voters = voters.filter(v23town=True)

        return voters

    def add_filter_context(self, context, search_action):
        '''Prepare filter options, selected values, and querystring helpers for templates.'''

        # Build dynamic filter choices from the current database values.
        parties = sorted(Voter.objects.values_list('party_affiliation', flat=True).distinct())
        voter_scores = sorted(Voter.objects.values_list('voter_score', flat=True).distinct())

        # Extract birth years from date_of_birth strings to populate year dropdowns.
        birth_years = []
        for item in Voter.objects.values_list('date_of_birth', flat=True):
            if item and len(item) >= 4:
                birth_years.append(item[:4])
        birth_years = sorted(set(birth_years))

        # Pass choices into the template context.
        context['parties'] = parties
        context['voter_scores'] = voter_scores
        context['birth_years'] = birth_years

        # Preserve selected filter values across form submits/pagination.
        context['selected_party_affiliation'] = self.request.GET.get('party_affiliation', '')
        context['selected_min_birth_year'] = self.request.GET.get('min_birth_year', '')
        context['selected_max_birth_year'] = self.request.GET.get('max_birth_year', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')
    
        # Keep current filters when paginating (except the page parameter itself).
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['querystring'] = query_params.urlencode()
        context['search_action_url'] = reverse(search_action)

        return context


class VotersListView(VoterFilterMixin, ListView):
    '''View to list voters with filtering and pagination.'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        '''for quering the DB'''
        # Apply filters and sort for stable, readable list output.
        voters = self.get_filtered_queryset().order_by('last_name', 'first_name')
        return voters

    def get_context_data(self, **kwargs):
        '''For form options and keeping filter selections on page.'''
        context = super().get_context_data(**kwargs)
        context = self.add_filter_context(context, 'voters')
        return context


class VoterGraphsView(VoterFilterMixin, ListView):
    '''View to display aggregate graphs of voter records.'''

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        '''filtered queryset used for graphing'''
        # Use the same filter rules as list view for consistent results.
        return self.get_filtered_queryset()

    def get_context_data(self, **kwargs):
        '''build Plotly graph divs from filtered voter data'''
        # Convert queryset to list so we can traverse once for all aggregates.
        context = super().get_context_data(**kwargs)
        context = self.add_filter_context(context, 'graphs')

        voters = list(self.get_queryset())

        # graph 1: by birth year
        by_birth_year = {}
        by_party = {}
        election_counts = {
            'v20state': 0,
            'v21town': 0,
            'v21primary': 0,
            'v22general': 0,
            'v23town': 0,
        }

        for v in voters:
            # Aggregate counts for each requested chart.
            # date_of_birth stored as text YYYY-MM-DD
            year = v.date_of_birth[:4]
            by_birth_year[year] = by_birth_year.get(year, 0) + 1
            by_party[v.party_affiliation] = by_party.get(v.party_affiliation, 0) + 1
            if v.v20state:
                election_counts['v20state'] += 1
            if v.v21town:
                election_counts['v21town'] += 1
            if v.v21primary:
                election_counts['v21primary'] += 1
            if v.v22general:
                election_counts['v22general'] += 1
            if v.v23town:
                election_counts['v23town'] += 1

        # by birth year histogram
        years = sorted(by_birth_year.keys())
        y_vals = [by_birth_year[y] for y in years]
        fig_by_year = go.Bar(x=years, y=y_vals)
        context['graph_div_birth_year'] = plotly.offline.plot({
            'data': [fig_by_year],
            'layout': {'title': 'Voter Distribution by Year of Birth'}
        }, auto_open=False, output_type='div')

        # by party pie chart
        parties = sorted(by_party.keys())
        party_values = [by_party[p] for p in parties]
        fig_by_party = go.Pie(labels=parties, values=party_values)
        context['graph_div_party'] = plotly.offline.plot({
            'data': [fig_by_party],
            'layout': {'title': 'Voter Distribution by Party'}
        }, auto_open=False, output_type='div')

        # participation in each election
        election_labels = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_values = [election_counts['v20state'], election_counts['v21town'], election_counts['v21primary'], election_counts['v22general'], election_counts['v23town']]
        fig_election = go.Bar(x=election_labels, y=election_values)
        context['graph_div_elections'] = plotly.offline.plot({
            'data': [fig_election],
            'layout': {'title': 'Voters by Election Participation'}
        }, auto_open=False, output_type='div')

        return context


class VoterDetailView(DetailView):
    '''View to show detail page for one voter record.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'

    def get_context_data(self, **kwargs):
        '''for detail template context'''
        # Prepare a printable full address string for the Google Maps link.
        context = super().get_context_data(**kwargs)
        v = context['v']
        full_address = f'{v.residential_address_street_number} {v.residential_address_street_name} '
        if v.residential_address_apartment_number:
            full_address += f'{v.residential_address_apartment_number}, '
        full_address += f'{v.residential_address_zip_code}'
        context['full_address'] = full_address
        return context
