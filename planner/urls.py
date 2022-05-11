from nturl2path import pathname2url
from django import urls
from django.urls import path
from . import views
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,ShoppingList

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(), name = 'task'),
    path('task-create/<day>/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name ='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(), name ='task-delete'),
    # path('list-create/',ShoppingListItemCreate.as_view(),name='list-create'),
    # path('list-create', views.shopping, name = 'list-create'),
    # path('add', views.addItem, name = 'add'),
    # path('complete/<item_id>', views.completeItem, name = 'complete'),
    # path('deleteitem/<item_id>', views.deleteItem, name = 'deleteitem'),
    # path('deleteall', views.deleteAll, name = 'deleteall'),
    path("list/", views.ListListView.as_view(), name="index"),
    path("list/<int:list_id>/", views.ItemListView.as_view(), name="list"),
    path("list/add/", views.ListCreate.as_view(), name="list-add"),
    path(
        "list/<int:pk>/delete/", views.ListDelete.as_view(), name="list-delete"
    ),
    path(
        "list/<int:list_id>/item/add/",
        views.ItemCreate.as_view(),
        name="item-add",
    ),
    path(
        "list/<int:list_id>/item/<int:pk>/",
        views.ItemUpdate.as_view(),
        name="item-update",
    ),
    path(
        "list/<int:list_id>/item/<int:pk>/delete/",
        views.ItemDelete.as_view(),
        name="item-delete",
    ),
]
