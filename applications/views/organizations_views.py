from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.utils import IntegrityError
from applications.models import Degree, Department, Designation, LevelOfEducation, Document_Type, Certificate_Permission


def organizations(request):
    return render(request, "faculty_requirement/admin/organizations.html")


def degree(request):
    if request.method == "POST":
        op = request.POST.get("operation")

        try:
            if op == "create":
                degree_code = (request.POST.get("degree_code") or "").strip()
                degree_name = (request.POST.get("degree") or "").strip()

                if not degree_code or not degree_name:
                    messages.error(request, "Degree Code and Degree Name are required.")
                else:
                    Degree.objects.create(
                        degree_code=degree_code,
                        degree=degree_name
                    )
                    messages.success(request, "Degree created successfully.")

            elif op == "edit":
                obj = get_object_or_404(Degree, id=request.POST.get("id"))

                degree_code = (request.POST.get("degree_code") or "").strip()
                degree_name = (request.POST.get("degree") or "").strip()

                if not degree_code or not degree_name:
                    messages.error(request, "Degree Code and Degree Name are required.")
                else:
                    obj.degree_code = degree_code
                    obj.degree = degree_name
                    obj.save()
                    messages.success(request, "Degree updated successfully.")

            elif op == "delete":
                obj = get_object_or_404(Degree, id=request.POST.get("id"))
                obj.delete()
                messages.success(request, "Degree deleted successfully.")

        except IntegrityError:
            messages.error(request, "Degree Code or Degree Name must be unique.")

        return redirect("degree")

    degrees = Degree.objects.all().order_by("degree")
    return render(
        request,
        "faculty_requirement/admin/degree.html",
        {"degrees": degrees}
    )

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

    departments = Department.objects.select_related("degree").all().order_by("degree")
    degrees = Degree.objects.all().order_by("degree")
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


def document_type(request):
    if request.method == "POST":
        op = request.POST.get("operation")

        try:
            if op == "create":
                document_type = (request.POST.get("document_type") or "").strip()

                if not document_type:
                    messages.error(request, "Document Type is required.")
                else:
                    Document_Type.objects.create(document_type=document_type)
                    messages.success(request, "Document Type created successfully.")

            elif op == "edit":
                obj = get_object_or_404(Document_Type, id=request.POST.get("id"))
                document_type = (request.POST.get("document_type") or "").strip()

                if not document_type:
                    messages.error(request, "Document Type is required.")
                else:
                    obj.document_type = document_type
                    obj.save()
                    messages.success(request, "Document Type updated successfully.")

            elif op == "delete":
                obj = get_object_or_404(Document_Type, id=request.POST.get("id"))
                obj.delete()
                messages.success(request, "Document Type deleted successfully.")

        except IntegrityError:
            messages.error(request, "Document Type must be unique.")

        return redirect("document_type")

    document_types = Document_Type.objects.all().order_by("document_type")
    return render(
        request,
        "faculty_requirement/admin/document_type.html",
        {"document_types": document_types}
    )


def certificate_permission(request):
    if request.method == "POST":
        op = request.POST.get("operation")

        try:
            if op == "create":
                department_id = request.POST.get("department")
                document_type_id = request.POST.get("document_type")
                is_required = request.POST.get("is_required") == "on"

                if not department_id or not document_type_id:
                    messages.error(request, "Department and Document Type are required.")
                else:
                    Certificate_Permission.objects.create(
                        department_id=department_id,
                        document_type_id=document_type_id,
                        is_required=is_required
                    )
                    messages.success(request, "Certificate permission assigned successfully.")

            elif op == "edit":
                obj = get_object_or_404(Certificate_Permission, id=request.POST.get("id"))

                department_id = request.POST.get("department")
                document_type_id = request.POST.get("document_type")
                is_required = request.POST.get("is_required") == "on"

                if not department_id or not document_type_id:
                    messages.error(request, "Department and Document Type are required.")
                else:
                    obj.department_id = department_id
                    obj.document_type_id = document_type_id
                    obj.is_required = is_required
                    obj.save()
                    messages.success(request, "Certificate permission updated successfully.")

            elif op == "delete":
                obj = get_object_or_404(Certificate_Permission, id=request.POST.get("id"))
                obj.delete()
                messages.success(request, "Certificate permission deleted successfully.")

        except IntegrityError:
            messages.error(
                request,
                "This document type is already assigned to this department."
            )

        return redirect("certificate_permission")

    context = {
        "departments": Department.objects.all().order_by("name"),
        "document_types": Document_Type.objects.all().order_by("document_type"),
        "permissions": Certificate_Permission.objects.select_related(
            "department", "document_type"
        ).order_by("department__name"),
    }

    return render(
        request,
        "faculty_requirement/admin/certificate_permission.html",
        context
    )
