from django.conf.urls import url
from .models import Faculty
from . import views

app_name = 'StudentPoll'

urlpatterns = [
    #Actual Views
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^vote/$', views.Vote_View.as_view(), name='Vote'),
    url(r'^statistics/$', views.Statistics.as_view(), name='Statistics'),
    url(r'^login/$', views.Login.as_view(), name='Login'),
    url(r'^poll/admin/$', views.PollAdmin.as_view(), name='PollAdmin'),

    #Some Functions
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^pollAdd/$', views.pollAdd_view, name='pollAdd'),
    url(r'^categoryAdd/$', views.categoryAdd_view, name='categoryAdd'),
    url(r'^editState/$', views.editState_view, name='editState'),

    #Ajax Requests
    url(r'^ajax/filterGroups/$', views.filterGroups_view, name='filterGroups'),
    url(r'^ajax/getSubjects/$', views.getSubjects_view, name='getSubjects'),

]