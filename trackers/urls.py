from nturl2path import pathname2url
from django import urls
from django.urls import path
from . import views
from .views import DataCreate, DataDelete, TrackerListView,TrackerCreate,TrackerDelete,TrackerListView,DataCreate,DataDelete,DataUpdate,DataListView

urlpatterns = [
    path("", TrackerListView.as_view(), name="trackers"),
    path("<int:tracker_id>/", views.DataListView.as_view(), name="tracker"),
    path("add/", views.TrackerCreate.as_view(), name="tracker-add"),
    path(
        "<int:pk>/delete/", views.TrackerDelete.as_view(), name="tracker-delete"
    ),
    path("<int:tracker_id>/data/add/",views.DataCreate.as_view(),name="data-add"),
    path("<int:tracker_id>/data/<int:pk>/",views.DataUpdate.as_view(),name="data-update"),
    path("<int:tracker_id>/data/<int:pk>/delete/",views.DataDelete.as_view(),name="data-delete"),
]
