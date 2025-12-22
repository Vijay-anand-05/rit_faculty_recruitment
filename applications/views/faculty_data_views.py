from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from applications.models import *

def faculty_data(request):
    return render(request, "faculty_requirement/admin/faculty/faculty_data.html")



def update_faculty_data(request):

    return render(request, "faculty_requirement/admin/faculty/update_faculty_data.html")

