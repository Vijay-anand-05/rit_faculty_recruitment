from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.utils import IntegrityError
from applications.models import Degree, Department, Designation, LevelOfEducation


def organizations(request):
    return render(request, "faculty_requirement/admin/organizations.html")


def degree(request):
    if request.method == "POST":
        op = request.POST.get("operation")
        try:
            if op == "create":
                name = (request.POST.get("name") or "").strip()
                if not name:
                    messages.error(request, "Name is required.")
                else:
                    Degree.objects.create(name=name)
                    messages.success(request, "Degree created successfully.")
            elif op == "edit":
                obj = get_object_or_404(Degree, id=request.POST.get("id"))
                name = (request.POST.get("name") or "").strip()
                if not name:
                    messages.error(request, "Name is required.")
                else:
                    obj.name = name
                    obj.save()
                    messages.success(request, "Degree updated successfully.")
            elif op == "delete":
                obj = get_object_or_404(Degree, id=request.POST.get("id"))
                obj.delete()
                messages.success(request, "Degree deleted successfully.")
        except IntegrityError:
            messages.error(request, "Name must be unique.")
        return redirect("degree")

    degrees = Degree.objects.all().order_by("name")
    return render(request, "faculty_requirement/admin/degree.html", {"degrees": degrees})


def department(request):
    if request.method == "POST":
        op = request.POST.get("operation")
        try:
            if op == "create":
                name = (request.POST.get("name") or "").strip()
                code = (request.POST.get("code") or "").strip().upper()
                degree_id = request.POST.get("degree_id")
                if not name or not code or not degree_id:
                    messages.error(request, "Name, Code and Degree are required.")
                else:
                    Department.objects.create(name=name, code=code, degree_id=degree_id)
                    messages.success(request, "Department created successfully.")
            elif op == "edit":
                obj = get_object_or_404(Department, id=request.POST.get("id"))
                name = (request.POST.get("name") or "").strip()
                code = (request.POST.get("code") or "").strip().upper()
                degree_id = request.POST.get("degree_id")
                if not name or not code or not degree_id:
                    messages.error(request, "Name, Code and Degree are required.")
                else:
                    obj.name = name
                    obj.code = code
                    obj.degree_id = degree_id
                    obj.save()
                    messages.success(request, "Department updated successfully.")
            elif op == "delete":
                obj = get_object_or_404(Department, id=request.POST.get("id"))
                obj.delete()
                messages.success(request, "Department deleted successfully.")
        except IntegrityError:
            messages.error(request, "Name and Code must be unique.")
        return redirect("department")

    departments = Department.objects.select_related("degree").all().order_by("name")
    degrees = Degree.objects.all().order_by("name")
    return render(
        request,
        "faculty_requirement/admin/departments.html",
        {"departments": departments, "degrees": degrees},
    )


def designation(request):
    if request.method == "POST":
        op = request.POST.get("operation")
        try:
            if op == "create":
                name = (request.POST.get("name") or "").strip()
                if not name:
                    messages.error(request, "Name is required.")
                else:
                    Designation.objects.create(name=name)
                    messages.success(request, "Designation created successfully.")
            elif op == "edit":
                obj = get_object_or_404(Designation, id=request.POST.get("id"))
                name = (request.POST.get("name") or "").strip()
                if not name:
                    messages.error(request, "Name is required.")
                else:
                    obj.name = name
                    obj.save()
                    messages.success(request, "Designation updated successfully.")
            elif op == "delete":
                obj = get_object_or_404(Designation, id=request.POST.get("id"))
                obj.delete()
                messages.success(request, "Designation deleted successfully.")
        except IntegrityError:
            messages.error(request, "Name must be unique.")
        return redirect("designation")

    designations = Designation.objects.all().order_by("name")
    return render(request, "faculty_requirement/admin/designation.html", {"designations": designations})


def level_of_education(request):
    if request.method == "POST":
        op = request.POST.get("operation")
        try:
            if op == "create":
                name = (request.POST.get("name") or "").strip()
                if not name:
                    messages.error(request, "Name is required.")
                else:
                    LevelOfEducation.objects.create(name=name)
                    messages.success(request, "Level created successfully.")
            elif op == "edit":
                obj = get_object_or_404(LevelOfEducation, id=request.POST.get("id"))
                name = (request.POST.get("name") or "").strip()
                if not name:
                    messages.error(request, "Name is required.")
                else:
                    obj.name = name
                    obj.save()
                    messages.success(request, "Level updated successfully.")
            elif op == "delete":
                obj = get_object_or_404(LevelOfEducation, id=request.POST.get("id"))
                obj.delete()
                messages.success(request, "Level deleted successfully.")
        except IntegrityError:
            messages.error(request, "Name must be unique.")
        return redirect("level_of_education")

    levels = LevelOfEducation.objects.all().order_by("name")
    return render(request, "faculty_requirement/admin/level_of_education.html", {"levels": levels})
