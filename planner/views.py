from pyexpat import model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.contrib import messages
from django.utils.timezone import localtime
from users.models import Profile
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Sum
import xlwt
import pandas as pd
import datetime
from datetime import datetime as datetime_custom
from django.db.models import Q

from .models import Task,Data,Tracker
from .forms import ShoppingForm


################ TASKS ##############################


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



class TrackerList(ListView):   
    model = Tracker
    template_name = "planner/trackers.html"


@login_required(login_url='login')
def tracker_page(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    data_set =  Data.objects.filter(
        user = request.user
    ).order_by('-date')

    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                data_set = data_set.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            else:
                data_set = data_set.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            data_set = data_set.filter(
                date__lte = date_to
            ).order_by('-date')
    
    except:
        messages.error(request,'Something went wrong')
        return redirect('trackers')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(data_set,5)
    page_number = request.GET.get('page')
    page_expenses = Paginator.get_page(paginator,page_number)

    return render(request,'expense_app/expense.html',{
        'page_expenses':page_expenses,
        'expenses':expenses,
        'filter_context':filter_context,
        'base_url':base_url
    })