from nturl2path import pathname2url
from django import urls
from django.urls import path,include
from . import views

urlpatterns = [
    path('planner/', include('planner.urls'), name='planner'),
    path("", views.ListListView.as_view(), name="index"),
    path("<int:list_id>/", views.ItemListView.as_view(), name="list"),
    path("add/", views.ListCreate.as_view(), name="list-add"),
    path(
        "<int:pk>/delete/", views.ListDelete.as_view(), name="list-delete"
    ),
    path(
        "<int:list_id>/item/add/",
        views.ItemCreate.as_view(),
        name="item-add",
    ),
    path(
        "<int:list_id>/item/<int:pk>/",
        views.ItemUpdate.as_view(),
        name="item-update",
    ),
    path(
        "<int:list_id>/item/<int:pk>/delete/",
        views.ItemDelete.as_view(),
        name="item-delete",
    ),
]

