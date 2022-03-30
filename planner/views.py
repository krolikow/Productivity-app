from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy

from .models import Task


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    monday = Task.objects.filter(day ='M')

class TaskDetail(DetailView):
    model = Task
    fields = '__all__'
    context_object_name = 'task' 

class TaskCreate(CreateView):
    model = Task
    fields = ['title','description','complete']

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['day'] = self.kwargs['day']
        return context

    def form_valid(self, form): 
        form.instance.day = self.kwargs['day']
        # context = {'day':self.kwargs['day']} // redundant?
        return super(TaskCreate, self).form_valid(form)

    success_url = reverse_lazy('tasks')

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class DeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')