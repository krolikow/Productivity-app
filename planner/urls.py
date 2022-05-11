from nturl2path import pathname2url
from django import urls
from django.urls import path
from . import views
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,TrackerList

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(), name = 'task'),
    path('task-create/<day>/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name ='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(), name ='task-delete'),
    path("trackers/", views.TrackerList.as_view(), name="trackers"),
    path("tracker/", views.TrackerList.as_view(), name="trackers"),
]
