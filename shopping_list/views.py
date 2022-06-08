from django.views.generic.list import ListView
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from shopping_list.models import ShoppingList,Item


class ListListView(ListView):
    model = ShoppingList
    template_name = "shopping_list/index.html"
    context_object_name = 'lists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lists'] = context['lists'].filter(user=self.request.user)
        return context

class ItemListView(ListView):
    model = Item
    template_name = "shopping_list/shopping_list.html"

    def get_queryset(self):
        return Item.objects.filter(shopping_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["shopping_list"] = ShoppingList.objects.get(id=self.kwargs["list_id"])
        return context


class ListCreate(CreateView):
    model = ShoppingList
    fields = ["title"]

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Add a new list"
        return context

    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super(ListCreate, self).form_valid(form)

class ItemCreate(CreateView):
    model = Item
    fields = [
        "shopping_list",
        "title",
    ]
    
    def get_initial(self):
        initial_data = super().get_initial()
        shopping_list = ShoppingList.objects.get(id=self.kwargs["list_id"])
        initial_data["shopping_list"] = shopping_list
        return initial_data

    def get_context_data(self):
        context = super().get_context_data()
        shopping_list = ShoppingList.objects.get(id=self.kwargs["list_id"])
        context["shopping_list"] = shopping_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.shopping_list_id])


class ListDelete(DeleteView):
    model = ShoppingList
    success_url = reverse_lazy("index")


class ItemDelete(DeleteView):
    model = Item

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shopping_list"] = self.object.shopping_list
        return context


class ItemUpdate(UpdateView):
    model = Item
    fields = [
        "shopping_list",
        "title"
    ]

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self):
        context = super().get_context_data()
        context["shopping_list"] = self.object.shopping_list
        context["title"] = "Edit item"
        return context
