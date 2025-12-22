from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

def organizations(request):
    return render(request, "faculty_requirement/admin/organizations.html")



