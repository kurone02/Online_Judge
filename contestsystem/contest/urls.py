from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index),
    path('problems', views.problems, name = "problems"),
    path('problems/<slug:codename>', views.problemsList, name = "problemsList"),
    path('submit', views.submit, name = 'submit'),
    path('submissions', views.submissions, name = 'submissions'),
    path('standings', views.standings, name = "standings"),
]
