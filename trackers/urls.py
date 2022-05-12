from nturl2path import pathname2url
from django import urls
from django.urls import path
from . import views
from .views import TrackerList,TrackerView,tracker_page,add_data

urlpatterns = [
    path("", TrackerList.as_view(), name="trackers"),
    path("<int:tracker_id>/", tracker_page, name="tracker"),
    path("<int:tracker_id>/add/", add_data, name="add_data"),
]
