from django.shortcuts import render, redirect
from applications.models import *

# 1. Candidate Personal Information
def candidate_personal_information(request):
    if request.method == "POST":
        request.session["candidate"] = request.POST.dict()
        return redirect("position_and_employment")

    return render(request, "faculty_requirement/faculty/candidate_personal_information.html", {
        "data": request.session.get("candidate", {})
    })


# 2. Position & Employment
def position_and_employment(request):
    if request.method == "POST":
        request.session["position"] = request.POST.dict()
        return redirect("educational_qualifications")

    return render(request, "faculty_requirement/faculty/position_and_employment.html", {
        "data": request.session.get("position", {})
    })


# 3. Educational Qualifications
def educational_qualifications(request):
    if request.method == "POST":
        education = []
        count = len(request.POST.getlist("degree_level"))

        for i in range(count):
            education.append({
                "degree_level": request.POST.getlist("degree_level")[i],
                "degree_name": request.POST.getlist("degree_name")[i],
                "specialization": request.POST.getlist("specialization")[i],
                "institution": request.POST.getlist("institution")[i],
                "university": request.POST.getlist("university")[i],
                "year_of_passing": request.POST.getlist("year_of_passing")[i],
                "percentage": request.POST.getlist("percentage")[i],
                "class_obtained": request.POST.getlist("class_obtained")[i],
                "mode_of_study": request.POST.getlist("mode_of_study")[i],
                "arrears": request.POST.getlist("arrears")[i],
            })

        request.session["education"] = education
        return redirect("academic_experience")

    return render(request, "faculty_requirement/faculty/educational_qualifications.html")


# 4. Academic Experience
def academic_experience(request):
    if request.method == "POST":
        data = []
        for i in range(len(request.POST.getlist("institution"))):
            data.append({
                "institution": request.POST.getlist("institution")[i],
                "designation": request.POST.getlist("designation")[i],
                "from_date": request.POST.getlist("from_date")[i],
                "to_date": request.POST.getlist("to_date")[i],
                "years": request.POST.getlist("years")[i],
                "months": request.POST.getlist("months")[i],
                "days": request.POST.getlist("days")[i],
            })
        request.session["academic_experience"] = data
        return redirect("industry_experience")

    return render(request, "faculty_requirement/faculty/academic_experience.html")


# 5. Industry / Research Experience
def industry_experience(request):
    if request.method == "POST":
        request.session["industry_experience"] = request.POST.dict()
        return redirect("teaching_experience")

    return render(request, "faculty_requirement/faculty/industry_and_research_experience.html")


# 6. Teaching Experience
def teaching_experience(request):
    if request.method == "POST":
        request.session["teaching"] = request.POST.dict()
        return redirect("research_publications")

    return render(request, "faculty_requirement/faculty/teaching_experience.html")


# 7. Research Publications
def research_publications(request):
    if request.method == "POST":
        request.session["publications"] = request.POST.dict()
        return redirect("contributions_and_events")

    return render(request, "faculty_requirement/faculty/research_publications.html")


# 8. Contributions & Events
def contributions_and_events(request):
    if request.method == "POST":
        request.session["contributions"] = request.POST.dict()
        return redirect("referees")

    return render(request, "faculty_requirement/faculty/contributions_and_events.html")


# 9. Referees
def referees(request):
    if request.method == "POST":
        request.session["referees"] = request.POST.dict()
        return redirect("final_declaration_and_submit")

    return render(request, "faculty_requirement/faculty/referees.html")


# 10. Final Save
def final_declaration_and_submit(request):
    if request.method == "POST":

        candidate = Candidate.objects.create(**request.session["candidate"])
        PositionApplication.objects.create(candidate=candidate, **request.session["position"])

        for edu in request.session.get("education", []):
            Education.objects.create(candidate=candidate, **edu)

        for exp in request.session.get("academic_experience", []):
            AcademicExperience.objects.create(candidate=candidate, **exp)

        request.session.flush()
        return redirect("application_success")

    return render(request, "faculty_requirement/faculty/final_declaration_and_submit.html")


def application_success(request):
    return render(request, "faculty_requirement/faculty/application_success.html")
