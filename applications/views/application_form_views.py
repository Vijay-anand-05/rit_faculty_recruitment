from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from applications.models import (
    Candidate,
    PositionApplication,
    Education,
    ResearchDetails,
    AcademicExperience,
    IndustryExperience,
    TeachingSubject,
    Contribution,
    Programme,
    Publication,
    Referee,
    ProgrammesPublications
)
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import FileSystemStorage
from applications.models import VisitorLog, ApplicationUsageLog
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

# views.py
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import json

# Create a custom template filter for indexing lists
from django.template.defaulttags import register

@register.filter
def index(indexable, i):
    try:
        return indexable[i]
    except (IndexError, TypeError):
        return ''

def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default



from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage


def individual_summary_sheet(request):
    if request.method == "POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken", None)

        # ================= PHOTO =================
        if request.FILES.get("photo"):
            fs = FileSystemStorage()
            filename = fs.save(request.FILES["photo"].name, request.FILES["photo"])
            data["photo"] = fs.url(filename)
            request.session["photo_path"] = filename

        # ================= FIX: OVERALL SPECIALIZATION =================
        data["specialization"] = data.get("overall_specialization", "").strip()

        # ================= FIX: NUMERIC SANITIZATION =================
        numeric_fields = [
            "assistant_professor_years",
            "associate_professor_years",
            "professor_years",
            "other_years",
            "research_experience_years",
            "industry_experience_years",
            "journal_national",
            "journal_international",
            "conference_national",
            "conference_international",
            "mtech_completed",
            "mtech_ongoing",
            "phd_completed",
            "phd_ongoing",
        ]

        for field in numeric_fields:
            data[field] = to_int(data.get(field))

        # ================= AGGREGATED FIELDS (MODEL MATCH) =================
        data["journal_publications"] = (
            data["journal_national"] + data["journal_international"]
        )

        data["conference_publications"] = (
            data["conference_national"] + data["conference_international"]
        )

        data["students_guided_completed"] = (
            data["mtech_completed"] + data["phd_completed"]
        )

        data["students_guided_ongoing"] = (
            data["mtech_ongoing"] + data["phd_ongoing"]
        )

        # ================= QUALIFICATIONS =================
        qualifications = []
        qual_names = request.POST.getlist("qualification[]")
        specializations = request.POST.getlist("specialization[]")
        institutes = request.POST.getlist("institute[]")
        years = request.POST.getlist("year[]")

        for i in range(len(qual_names)):
            if qual_names[i].strip():
                qualifications.append({
                    "qualification": qual_names[i].strip(),
                    "specialization": specializations[i].strip() if i < len(specializations) else "",
                    "institute": institutes[i].strip() if i < len(institutes) else "",
                    "year": to_int(years[i], None),
                })

        data["qualifications"] = qualifications

        # ================= SPONSORED PROJECTS =================
        projects = []
        titles = request.POST.getlist("project_title[]")
        durations = request.POST.getlist("project_duration[]")
        amounts = request.POST.getlist("project_amount[]")
        agencies = request.POST.getlist("project_agency[]")

        for i in range(len(titles)):
            if titles[i].strip():
                projects.append({
                    "title": titles[i].strip(),
                    "duration": durations[i].strip() if i < len(durations) else "",
                    "amount": to_int(amounts[i], None),
                    "agency": agencies[i].strip() if i < len(agencies) else "",
                })

        data["projects"] = projects

        # ================= SAVE TO SESSION (UNCHANGED FLOW) =================
        request.session["summary"] = data
        return redirect("individual_data_sheet")

    return render(
        request,
        "faculty_requirement/faculty/individual_summary_sheet.html",
        {"data": request.session.get("summary", {})},
    )




# def individual_summary_sheet(request):
#     # 🔹 VISITOR LOG (GET + POST)
#     try:
#         VisitorLog.objects.create(
#             user=request.user if request.user.is_authenticated else None,
#             ip_address=get_client_ip(request),
#             user_agent=request.META.get("HTTP_USER_AGENT", ""),
#             device_type="Mobile"
#             if "Mobile" in request.META.get("HTTP_USER_AGENT", "")
#             else "Desktop",
#             path=request.path,
#             method=request.method,
#         )
#     except Exception:
#         pass  # logging must never break the app

#     # 🔹 FORM SUBMISSION
#     if request.method == "POST":
#         data = request.POST.dict()
#         data.pop("csrfmiddlewaretoken", None)

#         # HANDLE PHOTO UPLOAD
#         if request.FILES.get("photo"):
#             fs = FileSystemStorage()
#             filename = fs.save(request.FILES["photo"].name, request.FILES["photo"])
#             data["photo"] = fs.url(filename)
#             request.session["photo_path"] = filename

#         # Store summary in session
#         request.session["summary"] = data

#         # ⚠️ NO ApplicationUsageLog here yet
#         # Because candidate is NOT created at this stage

#         return redirect("individual_data_sheet")

#     return render(
#         request,
#         "faculty_requirement/faculty/individual_summary_sheet.html",
#         {"data": request.session.get("summary", {})},
#     )




def individual_data_sheet(request):
    if request.method == "POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken", None)
        request.session["personal"] = data
        return redirect("educational_qualifications")

    return render(
        request,
        "faculty_requirement/faculty/individual_data_sheet.html",
        {"data": request.session.get("personal", {})},
    )


def educational_qualifications(request):
    if request.method == "POST":

        education_list = []

        categories = request.POST.getlist("category[]")
        degrees = request.POST.getlist("degree[]")
        specializations = request.POST.getlist("specialization[]")
        years = request.POST.getlist("year_of_passing[]")
        institutions = request.POST.getlist("institution[]")
        universities = request.POST.getlist("university[]")
        percentages = request.POST.getlist("percentage[]")
        classes = request.POST.getlist("class_obtained[]")

        for i in range(len(categories)):
            education_list.append({
                "category": categories[i],
                "degree": degrees[i],
                "specialization": specializations[i],
                "year_of_passing": years[i],
                "institution": institutions[i],
                "university": universities[i],
                "percentage": percentages[i],
                "class_obtained": classes[i],
            })

        request.session["education"] = education_list

        request.session["research_details"] = {
            "mode_ug": request.POST.get("mode_ug"),
            "mode_pg": request.POST.get("mode_pg"),
            "mode_phd": request.POST.get("mode_phd"),
            "arrears_ug": request.POST.get("arrears_ug"),
            "arrears_pg": request.POST.get("arrears_pg"),
            "gate_score": request.POST.get("gate_score"),
            "net_slet_score": request.POST.get("net_slet_score"),
            "me_thesis_title": request.POST.get("me_thesis_title"),
            "phd_thesis_title": request.POST.get("phd_thesis_title"),
        }

        return redirect("academic_and_industry_experience")

    return render(
        request,
        "faculty_requirement/faculty/educational_qualifications.html",
        {
            "education": request.session.get("education", []),
            "research": request.session.get("research_details", {}),
        }
    )





def academic_and_industry_experience(request):
    if request.method == "POST":

        academic_list = []
        for i in range(len(request.POST.getlist("academic_institution[]"))):
            academic_list.append({
                "institution": request.POST.getlist("academic_institution[]")[i],
                "designation": request.POST.getlist("academic_designation[]")[i],
                "joining_date": request.POST.getlist("academic_joining_date[]")[i],
                "relieving_date": request.POST.getlist("academic_relieving_date[]")[i],
                "years": request.POST.getlist("academic_years[]")[i],
                "months": request.POST.getlist("academic_months[]")[i],
                "days": request.POST.getlist("academic_days[]")[i],
            })

        industry_list = []
        for i in range(len(request.POST.getlist("industry_organization[]"))):
            industry_list.append({
                "organization": request.POST.getlist("industry_organization[]")[i],
                "designation": request.POST.getlist("industry_designation[]")[i],
                "nature_of_work": request.POST.getlist("industry_nature[]")[i],
                "joining_date": request.POST.getlist("industry_joining_date[]")[i],
                "relieving_date": request.POST.getlist("industry_relieving_date[]")[i],
                "years": request.POST.getlist("industry_years[]")[i],
                "months": request.POST.getlist("industry_months[]")[i],
                "days": request.POST.getlist("industry_days[]")[i],
            })

        request.session["academic_experience"] = academic_list
        request.session["industry_experience"] = industry_list

        return redirect("teaching_and_contributions")

    return render(
        request,
        "faculty_requirement/faculty/academic_and_industry_experience.html",
        {
            "academic": request.session.get("academic_experience", []),
            "industry": request.session.get("industry_experience", []),
        }
    )




def teaching_and_contributions(request):
    subjects = request.session.get("subjects", [])
    contributions = request.session.get("contributions", [])

    has_ug = any(s.get("level") == "UG" for s in subjects)
    has_pg = any(s.get("level") == "PG" for s in subjects)

    has_dept = any(c.get("level") == "Department" for c in contributions)
    has_college = any(c.get("level") == "College" for c in contributions)

    if request.method == "POST":
        subjects = []
        for s in request.POST.getlist("ug_subjects[]"):
            subjects.append({"level": "UG", "subject_and_result": s})
        for s in request.POST.getlist("pg_subjects[]"):
            subjects.append({"level": "PG", "subject_and_result": s})

        contributions = []
        for d in request.POST.getlist("department_contributions[]"):
            contributions.append({"level": "Department", "description": d})
        for c in request.POST.getlist("college_contributions[]"):
            contributions.append({"level": "College", "description": c})

        request.session["subjects"] = subjects
        request.session["contributions"] = contributions
        return redirect("programmes_and_publications")

    return render(
        request,
        "faculty_requirement/faculty/teaching_and_contributions.html",
        {
            "subjects": subjects,
            "contributions": contributions,
            "has_ug": has_ug,
            "has_pg": has_pg,
            "has_dept": has_dept,
            "has_college": has_college,
        }
    )
def to_int(val, default=0):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default



def programmes_and_publications(request):
    if request.method == "POST":

        request.session["programmes"] = [
            {
                "programme_type": p.strip(),
                "count": to_int(c),
            }
            for p, c in zip(
                request.POST.getlist("programme_type[]"),
                request.POST.getlist("programme_count[]"),
            )
            if p.strip()
        ]

        request.session["publications"] = [
            {
                "title": t.strip(),
                "indexing": i,
            }
            for t, i in zip(
                request.POST.getlist("publication_title[]"),
                request.POST.getlist("publication_indexing[]"),
            )
            if t.strip()
        ]

        request.session["research_publications"] = [
            {"details": d.strip()}
            for d in request.POST.getlist("research_publication_details[]")
            if d.strip()
        ]

        request.session["research_scholars"] = request.POST.get(
            "research_scholars_details", ""
        ).strip()

        request.session["sponsored_projects"] = [
            {
                "title": t.strip(),
                "status": s,
                "funding_agency": a.strip(),
                "amount": to_int(amt),
                "duration": d.strip(),
            }
            for t, s, a, amt, d in zip(
                request.POST.getlist("project_title[]"),
                request.POST.getlist("project_status[]"),
                request.POST.getlist("funding_agency[]"),
                request.POST.getlist("project_amount[]"),
                request.POST.getlist("project_duration[]"),
            )
            if t.strip()
        ]

        request.session["memberships"] = [
            {"details": d.strip()}
            for d in request.POST.getlist("membership_details[]")
            if d.strip()
        ]

        request.session["awards"] = [
            {"details": d.strip()}
            for d in request.POST.getlist("award_details[]")
            if d.strip()
        ]

        return redirect("referees_and_declaration")

    return render(
        request,
        "faculty_requirement/faculty/programmes_and_publications.html",
        {
            "programmes": request.session.get("programmes", []),
            "publications": request.session.get("publications", []),
            "research_publications": request.session.get("research_publications", []),
            "research_scholars": request.session.get("research_scholars", ""),
            "sponsored_projects": request.session.get("sponsored_projects", []),
            "memberships": request.session.get("memberships", []),
            "awards": request.session.get("awards", []),
        },
    )




def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

# def referees_and_declaration(request):
#     if request.method == "POST":

#         # -------- CANDIDATE (ONLY CANDIDATE FIELDS) --------
#         personal = request.session["personal"]

#         candidate_data = {
#             "name": personal.get("name"),
#             "age": to_int(personal.get("age")),
#             "date_of_birth": parse_date(personal.get("date_of_birth")),
#             "gender": personal.get("gender"),
#             "marital_status": personal.get("marital_status"),
#             "community": personal.get("community"),
#             "caste": personal.get("caste"),
#             "pan_number": personal.get("pan_number"),
#             "email": personal.get("email"),
#             "phone_primary": personal.get("phone_primary"),
#             "phone_secondary": personal.get("phone_secondary"),
#             "address": personal.get("address"),

#             # 🔥 FIXED HERE
#             "total_experience_years": to_int(personal.get("total_experience_years")),
#             "present_post_years": to_int(personal.get("present_post_years")),

#             "mother_name_and_occupation": personal.get("mother_name_and_occupation"),
#         }


#         photo_path = request.session.get("photo_path")

#         if photo_path:
#             candidate = Candidate.objects.create(
#                 **candidate_data,
#                 photo=photo_path
#             )
#         else:
#             candidate = Candidate.objects.create(**candidate_data)


#         # -------- POSITION APPLICATION --------
#         summary = request.session["summary"]

#         PositionApplication.objects.create(
#             candidate=candidate,
#             position_applied=summary.get("position_applied"),
#             department=summary.get("department"),
#             present_designation=summary.get("present_designation"),
#             present_organization=summary.get("present_organization"),
#             specialization=summary.get("specialization"),
#             assistant_professor_years=summary.get("assistant_professor_years", 0),
#             associate_professor_years=summary.get("associate_professor_years", 0),
#             professor_years=summary.get("professor_years", 0),
#             other_years=summary.get("other_years", 0),
#             research_experience_years=summary.get("research_experience_years", 0),
#             industry_experience_years=summary.get("industry_experience_years", 0),
#             journal_publications=summary.get("journal_publications", 0),
#             conference_publications=summary.get("conference_publications", 0),
#             students_guided_completed=summary.get("students_guided_completed", 0),
#             students_guided_ongoing=summary.get("students_guided_ongoing", 0),
#             community_and_caste=summary.get("community_and_caste"),
#         )

#         # -------- SAVE ALL OTHER SECTIONS (UNCHANGED) --------
#         for edu in request.session.get("education", []):
#             Education.objects.create(candidate=candidate, **edu)

#         ResearchDetails.objects.create(
#             candidate=candidate,
#             **request.session["research_details"]
#         )

#         for exp in request.session.get("academic_experience", []):
#             AcademicExperience.objects.create(candidate=candidate, **exp)

#         for exp in request.session.get("industry_experience", []):
#             IndustryExperience.objects.create(candidate=candidate, **exp)

#         for sub in request.session.get("subjects", []):
#             TeachingSubject.objects.create(candidate=candidate, **sub)

#         for con in request.session.get("contributions", []):
#             Contribution.objects.create(candidate=candidate, **con)

#         for prog in request.session.get("programmes", []):
#             Programme.objects.create(candidate=candidate, **prog)

#         for pub in request.session.get("publications", []):
#             Publication.objects.create(candidate=candidate, **pub)

#         for i in range(len(request.POST.getlist("ref_name[]"))):
#             Referee.objects.create(
#                 candidate=candidate,
#                 name=request.POST.getlist("ref_name[]")[i],
#                 designation=request.POST.getlist("ref_designation[]")[i],
#                 organization=request.POST.getlist("ref_organization[]")[i],
#                 contact_number=request.POST.getlist("ref_contact[]")[i],
#             )

#         request.session.flush()
#         return redirect("application_success")

#     return render(
#         request,
#         "faculty_requirement/faculty/referees_and_declaration.html",
#         {
#             "referees": []
#         }
#     )

def referees_and_declaration(request):

    if request.method == "POST":

        personal = request.session.get("personal")
        summary = request.session.get("summary")

        if not personal or not summary:
            return redirect("application_success")

        # ================= CANDIDATE =================
        candidate = Candidate.objects.create(
            name=personal.get("name"),
            age=to_int(personal.get("age")),
            date_of_birth=parse_date(personal.get("date_of_birth")),
            gender=personal.get("gender"),
            marital_status=personal.get("marital_status"),
            community=personal.get("community"),
            caste=personal.get("caste"),
            pan_number=personal.get("pan_number"),
            email=personal.get("email"),
            phone_primary=personal.get("phone_primary"),
            phone_secondary=personal.get("phone_secondary"),
            address=personal.get("address"),
            total_experience_years=to_int(personal.get("total_experience_years")),
            present_post_years=to_int(personal.get("present_post_years")),
            mother_name_and_occupation=personal.get("mother_name_and_occupation"),
            photo=request.session.get("photo_path"),
        )

        # ================= POSITION APPLICATION =================
        PositionApplication.objects.create(
            candidate=candidate,
            position_applied=summary.get("position_applied"),
            department=summary.get("department"),
            present_designation=summary.get("present_designation"),
            present_organization=summary.get("present_organization"),
            specialization=summary.get("overall_specialization"),

            assistant_professor_years=to_int(summary.get("assistant_professor_years")),
            associate_professor_years=to_int(summary.get("associate_professor_years")),
            professor_years=to_int(summary.get("professor_years")),
            other_years=to_int(summary.get("other_years")),

            research_experience_years=to_int(summary.get("research_experience_years")),
            industry_experience_years=to_int(summary.get("industry_experience_years")),

            journal_publications=(
                to_int(summary.get("journal_national")) +
                to_int(summary.get("journal_international"))
            ),
            conference_publications=(
                to_int(summary.get("conference_national")) +
                to_int(summary.get("conference_international"))
            ),

            students_guided_completed=(
                to_int(summary.get("mtech_completed")) +
                to_int(summary.get("phd_completed"))
            ),
            students_guided_ongoing=(
                to_int(summary.get("mtech_ongoing")) +
                to_int(summary.get("phd_ongoing"))
            ),

            community_and_caste=summary.get("community_and_caste"),
        )

        # ================= EDUCATION =================
        for edu in request.session.get("education", []):
            Education.objects.create(candidate=candidate, **edu)

        # ================= RESEARCH DETAILS =================
        r = request.session.get("research_details", {})
        ResearchDetails.objects.create(
            candidate=candidate,
            mode_ug=r.get("mode_ug"),
            mode_pg=r.get("mode_pg"),
            mode_phd=r.get("mode_phd"),
            arrears_ug=to_int(r.get("arrears_ug")),
            arrears_pg=to_int(r.get("arrears_pg")),
            gate_score=to_int(r.get("gate_score")),
            net_slet_score=to_int(r.get("net_slet_score")),
            me_thesis_title=r.get("me_thesis_title"),
            phd_thesis_title=r.get("phd_thesis_title"),
        )

        # ================= EXPERIENCE =================
        for exp in request.session.get("academic_experience", []):
            AcademicExperience.objects.create(candidate=candidate, **exp)

        for exp in request.session.get("industry_experience", []):
            IndustryExperience.objects.create(candidate=candidate, **exp)

        # ================= TEACHING & CONTRIBUTIONS =================
        for s in request.session.get("subjects", []):
            TeachingSubject.objects.create(candidate=candidate, **s)

        for c in request.session.get("contributions", []):
            Contribution.objects.create(candidate=candidate, **c)

        # ================= PROGRAMMES & PUBLICATIONS =================
        for p in request.session.get("programmes", []):
            Programme.objects.create(candidate=candidate, **p)

        for p in request.session.get("publications", []):
            Publication.objects.create(candidate=candidate, **p)

        ProgrammesPublications.objects.create(
            candidate=candidate,
            programmes=request.session.get("programmes", []),
            publications=request.session.get("publications", []),
            research_publications_details=request.session.get("research_publications", []),
            research_scholars_details=request.session.get("research_scholars", ""),
            sponsored_projects=request.session.get("sponsored_projects", []),
            memberships=request.session.get("memberships", []),
            awards=request.session.get("awards", []),
        )

        # ================= REFEREES =================
        for i in range(len(request.POST.getlist("ref_name[]"))):
            Referee.objects.create(
                candidate=candidate,
                name=request.POST.getlist("ref_name[]")[i],
                designation=request.POST.getlist("ref_designation[]")[i],
                organization=request.POST.getlist("ref_organization[]")[i],
                contact_number=request.POST.getlist("ref_contact[]")[i],
            )

        request.session.flush()
        return redirect("application_success")

    return render(
        request,
        "faculty_requirement/faculty/referees_and_declaration.html",
        {"referees": []},
    )



def application_success(request):
    return render(request, "faculty_requirement/faculty/application_success.html")