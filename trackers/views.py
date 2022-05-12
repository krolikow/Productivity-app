from sqlite3 import Date
from xmlrpc.client import DateTime
from django.shortcuts import render
from pyexpat import model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.contrib import messages
from django.utils.timezone import localtime
from trackers.models import Data, Tracker
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
from chartjs.views.lines import BaseLineChartView
from django.http import JsonResponse
import datetime
import itertools



class TrackerList(ListView):   
    model = Tracker
    template_name = "trackers/trackers.html"


class TrackerView(ListView):
    model = Data
    template_name = "trackers/tracker.html"

    def get_queryset(self):
        return Data.objects.filter(tracker_id=self.kwargs["tracker_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["tracker"] = Data.objects.get(id=self.kwargs["tracker_id"])
        return context


class ChartView(BaseLineChartView):
    def get_labels(self):
        labels = []
        data_set =  Data.objects.order_by('-date')

        queryset = Data.objects.values('date').order_by('-date')
        for entry in queryset:
            labels.append(entry['date'])
        return 

    def get_data(self):
        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


@login_required(login_url='login')
def tracker_page(request,tracker_id):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    labels = []
    data = []

    queryset = Data.objects.order_by('-date')
    for entry in queryset:
        labels.append(entry.date)
        data.append(entry.amount)
    items = Data.objects.all()

    # try:

    #     if 'date_from' in request.GET and request.GET['date_from'] != '':
    #         date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
    #         filter_context['date_from'] = request.GET['date_from']
    #         date_from_html = request.GET['date_from']

    #         if 'date_to' in request.GET and request.GET['date_to'] != '':

    #             date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
    #             filter_context['date_to'] = request.GET['date_to']
    #             date_to_html = request.GET['date_to']
    #             data_set = data_set.filter(
    #                 Q(date__gte = date_from )
    #                 &
    #                 Q(date__lte = date_to)
    #             ).order_by('-date')

    #         else:
    #             data_set = data_set.filter(
    #                 date__gte = date_from
    #             ).order_by('-date')

    #     elif 'date_to' in request.GET and request.GET['date_to'] != '':

    #         date_to_html = request.GET['date_to']
    #         date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
    #         filter_context['date_from'] = request.GET['date_to']
    #         data_set = data_set.filter(
    #             date__lte = date_to
    #         ).order_by('-date')
    
    # except:
    #     messages.error(request,'Something went wrong')
    #     return redirect('trackers')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    # paginator = Paginator(data_set,5)
    page_number = request.GET.get('page')

    # return render(request,'./trackers/tracker.html',{
    #     'data_set':data_set,
    #     'filter_context':filter_context,
    #     'base_url':base_url
    # })
    return render(request,'./trackers/tracker.html',{
        'items' : items,
        'labels': labels,
        'data': data,
    })


# todo
@login_required(login_url='login')
def add_data(request,tracker_id):
        
    data = Data.objects.filter(user=request.user)

    context = {
        'data' : data,
        'values':request.POST
    }

    if request.method == 'GET':
         return render(request,'trackers/add_data.html',context)

    if request.method == 'POST':
        amount = request.POST.get('amount','')
        description = request.POST.get('description','')
        date = request.POST.get('date','')
        tracker = request.POST.get('tracker','')

        if amount== '':
            messages.error(request,'Amount cannot be empty')
            return render(request,'trackers/add_data.html',context)
            
        amount = float(amount)
        if amount <= 0:
            messages.error(request,'Amount should be greater than zero')
            return render(request,'trackers/add_data.html',context)

        if description == '':
            messages.error(request,'Description cannot be empty')
            return render(request,'trackers/add_data.html',context)

        if tracker == '':
            messages.error(request,'ExpenseCategory cannot be empty')
            return render(request,'trackers/add_data.html',context)

        if date == '':
            date = localtime()

        created_at = localtime()
        tracker_object = Tracker.objects.get()
        # data_obj = ExpenseCategory.objects.get(user=request.user,name =category)
        Data.objects.create(
            user=request.user,
            amount=amount,
            date=date,
            description=description,
            tracker = tracker_object
    ).save()

    messages.success(request,'Data Saved Successfully')
    return redirect('tracker')
