from pyexpat import model
from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task,ShoppingList,Item
from .forms import ShoppingForm

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['tasks'] = context['tasks'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    fields = '__all__'
    context_object_name = 'task' 

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description','complete']

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['day'] = self.kwargs['day']
        return context

    def form_valid(self, form): 
        form.instance.day = self.kwargs['day']
        return super(TaskCreate, self).form_valid(form)

    success_url = reverse_lazy('tasks')

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')



# class ListListView(ListView):
#     model = ShoppingList
#     template_name = "shopping_list\\shopping.html"


# class ItemListView(ListView):
#     model = Item
#     template_name = "shopping_list\\shopping.html"

#     def get_queryset(self):
#         return Item.objects.filter(shopping_list_id=self.kwargs["list_id"])

#     def get_context_data(self):
#         context = super().get_context_data()
#         context["shopping_list"] = ShoppingList.objects.get(id=self.kwargs["list_id"])
#         return context



# def shopping(request):
#     all_lists = ShoppingList.objects.all()
#     list = ShoppingList.objects.order_by("id")
#     form = ShoppingForm()

#     context ={"list":list,"all_lists" : all_lists, "form": form}
#     return render (request, "shopping_list\\shopping.html" , context)

# @require_POST
# def addItem(request):
#     form = ShoppingForm(request.POST)

#     if form.is_valid():
#         new_item = ShoppingList(text = request.POST['text'])
#         new_item.save()

#     return (redirect('list-create'))

# def completeItem(request, item_id):
#     item = ShoppingList.objects.get(pk=item_id)
#     item.complete = True
#     item.save()

#     return (redirect('list-create'))


# def deleteItem(request, item_id):
#     item = ShoppingList.objects.get(pk=item_id)
#     item.delete()
#     return redirect('list-create')

# def deleteAll(request):
#     ShoppingList.objects.all().delete()
#     return redirect('list-create')





class ListListView(ListView):
    model = ShoppingList
    template_name = "shopping_list/index.html"


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


class ItemUpdate(UpdateView):
    model = Item
    fields = [
        "shopping_list",
        "title"
    ]

    def get_context_data(self):
        context = super().get_context_data()
        context["shopping_list"] = self.object.shopping_list
        context["title"] = "Edit item"
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