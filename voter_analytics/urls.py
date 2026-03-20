"""
File: voter_analytics/urls.py
author: Jerry Teixeira (jerrybt@bu.edu), 03/20/26
Description: URL routes for voter list, detail and graphs views.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Voter list page (default page for this app).
    path(r'', views.VotersListView.as_view(), name='voters'),
    # Aggregate graph page for filtered voter statistics.
    path(r'graphs', views.VoterGraphsView.as_view(), name='graphs'),
    # Single voter detail page.
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
]
