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
from trackers.forms import DataForm
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
from datetime import date, datetime as datetime_custom
from django.db.models import Q
from chartjs.views.lines import BaseLineChartView
from django.http import JsonResponse
import datetime
import itertools
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput,DateTimePickerInput

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


class TrackerListView(ListView):
    model = Tracker
    template_name = "trackers/trackers.html"

class DataListView(ListView):
    model = Data
    template_name = "trackers/tracker.html"

    labels = []
    data = []

    # queryset = 
    # for entry in queryset:
    #     labels.append(entry.date)
    #     data.append(entry.amount)
    # items = Data.objects.all()

    def get_queryset(self):
        return Data.objects.filter(tracker_id=self.kwargs["tracker_id"]).order_by('-date')

    def get_context_data(self,**kwargs):
        context = super(DataListView,self).get_context_data(**kwargs)
        context["tracker"] = Tracker.objects.get(id=self.kwargs["tracker_id"])
        context["items"] = Data.objects.all()
        context["labels"] = [x[0] for x in list(Data.objects.values_list("date"))]
        context["data"] = [x[0] for x in list(Data.objects.values_list("amount"))]
        return context

from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

class TrackerCreate(CreateView):
    model = Tracker
    fields = ["title"]

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Add a new tracker"
        return context

class DateInput(forms.DateInput):
    input_type: 'date'
# class DataCreate(CreateView):
#     model = Data
#     fields = [
#         "tracker",
#         "title",
#         "amount",
#         "date",
#         "description"
#     ]

#     widgets= {"date":DateField()}
#     def get_initial(self):
#         initial_data = super().get_initial()
#         tracker = Tracker.objects.get(id=self.kwargs["tracker_id"])
#         initial_data["tracker"] = tracker
#         return initial_data

#     def get_context_data(self):
#         context = super().get_context_data()
#         tracker = Tracker.objects.get(id=self.kwargs["tracker_id"])
#         context["tracker"] = tracker
#         context["title"] = "Create a new data"
#         return context

#     def get_success_url(self):
#         return reverse("tracker", args=[self.object.tracker_id])

class DataCreate(CreateView):
    model = Data
    form_class= DataForm
    # fields = [
    #     "tracker",
    #     "title",
    #     "date",
    #     "amount",
    #     "description"
    # ]

    # date = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'],
    #     widget=forms.DateTimeInput(attrs={
    #         'class': 'form-control datetimepicker-input',
    #         'data-target': '#datetimepicker1'
    #     })
    # )

    # def get_form(self):
    #     form = super().get_form()
    #     form.fields["date"].widget = forms.DateInput(attrs={'type':'date'})
    #     return form


    def get_initial(self):
        initial_data = super().get_initial()
        tracker = Tracker.objects.get(id=self.kwargs["tracker_id"])
        initial_data["tracker"] = tracker
        return initial_data

    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        tracker = Tracker.objects.get(id=self.kwargs["tracker_id"])
        context["tracker"] = tracker
        context["title"] = "Create a new data"
        return context

    def get_success_url(self):
        return reverse("tracker", args=[self.object.tracker_id])

class TrackerDelete(DeleteView):
    model = Tracker
    success_url = reverse_lazy("trackers")


class DataDelete(DeleteView):
    model = Data

    def get_success_url(self):
        return reverse_lazy("tracker", args=[self.kwargs["tracker_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tracker"] = self.object.tracker
        return context


class DataUpdate(UpdateView):
    model = Data
    fields = [
        "tracker",
        "title"
    ]

    def get_success_url(self):
        return reverse_lazy("tracker", args=[self.kwargs["tracker_id"]])

    def get_context_data(self):
        context = super().get_context_data()
        context["tracker"] = self.object.tracker
        context["title"] = "Edit data"
        return context

