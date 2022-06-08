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
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class TrackerListView(LoginRequiredMixin,ListView):
    model = Tracker
    context_object_name = 'trackers'
    template_name = "trackers/trackers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trackers'] = context['trackers'].filter(user=self.request.user)
        return context


class DataListView(LoginRequiredMixin,ListView):
    model = Data
    template_name = "trackers/tracker.html"

    def get_queryset(self):
        return Data.objects.filter(tracker_id=self.kwargs["tracker_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["tracker"] = Tracker.objects.get(id=self.kwargs["tracker_id"])
        context["items"] = Data.objects.filter(tracker_id=self.kwargs["tracker_id"]).order_by('-date')[::-1]
        context["labels"] = [x[0] for x in list(Data.objects.values_list("date").filter(tracker_id=self.kwargs["tracker_id"]).order_by('-date')[::-1])]
        context["data"] = [x[0] for x in list(Data.objects.values_list("amount").filter(tracker_id=self.kwargs["tracker_id"]).order_by('-date')[::-1])]
        return context


class TrackerCreate(LoginRequiredMixin,CreateView):
    model = Tracker
    fields = ["title"]
    
    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super(TrackerCreate, self).form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Add a new tracker"
        return context

class DataCreate(LoginRequiredMixin,CreateView):
    model = Data
    form_class= DataForm

    def get_initial(self):
        initial_data = super().get_initial()
        tracker = Tracker.objects.get(id=self.kwargs["tracker_id"])
        initial_data["tracker"] = tracker
        return initial_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tracker = Tracker.objects.get(id=self.kwargs["tracker_id"])
        context["tracker"] = tracker
        context["title"] = "Create a new data"
        return context

    def get_success_url(self):
        return reverse("tracker", args=[self.object.tracker_id])

class TrackerDelete(LoginRequiredMixin,DeleteView):
    model = Tracker
    success_url = reverse_lazy("trackers")


class DataDelete(LoginRequiredMixin,DeleteView):
    model = Data

    def get_success_url(self):
        return reverse_lazy("tracker", args=[self.kwargs["tracker_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tracker"] = self.object.tracker
        return context


class DataUpdate(LoginRequiredMixin,UpdateView):
    model = Data
    form_class= DataForm

    def get_success_url(self):
        return reverse_lazy("tracker", args=[self.kwargs["tracker_id"]])

    def get_context_data(self):
        context = super().get_context_data()
        context["tracker"] = self.object.tracker
        context["title"] = "Edit data"
        return context

