from django.shortcuts import render
from django.http import HttpResponse


def planner_view(request,*args, **kwargs):
    return render(request,"planner.html",{})
