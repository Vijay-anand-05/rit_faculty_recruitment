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
)
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import FileSystemStorage
from applications.models import VisitorLog, ApplicationUsageLog

def individual_summary_sheet(request):
    if request.method == "POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken", None)

        # ✅ HANDLE PHOTO UPLOAD
        if request.FILES.get("photo"):
            fs = FileSystemStorage()
            filename = fs.save(request.FILES["photo"].name, request.FILES["photo"])
            data["photo"] = fs.url(filename)
            request.session["photo_path"] = filename  # store relative path

        request.session["summary"] = data
        return redirect("individual_data_sheet")

    return render(
        request,
        "faculty_requirement/faculty/individual_summary_sheet.html",
        {"data": request.session.get("summary", {})},
    )


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


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


def programmes_and_publications(request):
    if request.method == "POST":

        programmes = []
        for ptype, count in zip(
            request.POST.getlist("programme_type[]"),
            request.POST.getlist("programme_count[]"),
        ):
            if ptype or count:
                programmes.append({
                    "programme_type": ptype,
                    "count": count,
                })

        publications = []
        for title, indexing in zip(
            request.POST.getlist("publication_title[]"),
            request.POST.getlist("publication_indexing[]"),
        ):
            if title or indexing:
                publications.append({
                    "title": title,
                    "indexing": indexing,
                })

        request.session["programmes"] = programmes
        request.session["publications"] = publications

        return redirect("referees_and_declaration")

    return render(
        request,
        "faculty_requirement/faculty/programmes_and_publications.html",
        {
            "programmes": request.session.get("programmes", []),
            "publications": request.session.get("publications", []),
        }
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
    # 🔹 VISITOR LOG (GET + POST)
    try:
        VisitorLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            device_type="Mobile"
            if "Mobile" in request.META.get("HTTP_USER_AGENT", "")
            else "Desktop",
            path=request.path,
            method=request.method,
        )
    except Exception:
        pass  # logging must NEVER block submission

    if request.method == "POST":

        # -------- CANDIDATE --------
        personal = request.session["personal"]

        candidate_data = {
            "name": personal.get("name"),
            "age": to_int(personal.get("age")),
            "date_of_birth": parse_date(personal.get("date_of_birth")),
            "gender": personal.get("gender"),
            "marital_status": personal.get("marital_status"),
            "community": personal.get("community"),
            "caste": personal.get("caste"),
            "pan_number": personal.get("pan_number"),
            "email": personal.get("email"),
            "phone_primary": personal.get("phone_primary"),
            "phone_secondary": personal.get("phone_secondary"),
            "address": personal.get("address"),
            "total_experience_years": to_int(personal.get("total_experience_years")),
            "present_post_years": to_int(personal.get("present_post_years")),
            "mother_name_and_occupation": personal.get("mother_name_and_occupation"),
        }

        photo_path = request.session.get("photo_path")

        if photo_path:
            candidate = Candidate.objects.create(**candidate_data, photo=photo_path)
        else:
            candidate = Candidate.objects.create(**candidate_data)

        # -------- POSITION APPLICATION --------
        summary = request.session["summary"]

        PositionApplication.objects.create(
            candidate=candidate,
            position_applied=summary.get("position_applied"),
            department=summary.get("department"),
            present_designation=summary.get("present_designation"),
            present_organization=summary.get("present_organization"),
            specialization=summary.get("specialization"),
            assistant_professor_years=summary.get("assistant_professor_years", 0),
            associate_professor_years=summary.get("associate_professor_years", 0),
            professor_years=summary.get("professor_years", 0),
            other_years=summary.get("other_years", 0),
            research_experience_years=summary.get("research_experience_years", 0),
            industry_experience_years=summary.get("industry_experience_years", 0),
            journal_publications=summary.get("journal_publications", 0),
            conference_publications=summary.get("conference_publications", 0),
            students_guided_completed=summary.get("students_guided_completed", 0),
            students_guided_ongoing=summary.get("students_guided_ongoing", 0),
            community_and_caste=summary.get("community_and_caste"),
        )

        # -------- OTHER SECTIONS --------
        for edu in request.session.get("education", []):
            Education.objects.create(candidate=candidate, **edu)

        ResearchDetails.objects.create(
            candidate=candidate, **request.session["research_details"]
        )

        for exp in request.session.get("academic_experience", []):
            AcademicExperience.objects.create(candidate=candidate, **exp)

        for exp in request.session.get("industry_experience", []):
            IndustryExperience.objects.create(candidate=candidate, **exp)

        for sub in request.session.get("subjects", []):
            TeachingSubject.objects.create(candidate=candidate, **sub)

        for con in request.session.get("contributions", []):
            Contribution.objects.create(candidate=candidate, **con)

        for prog in request.session.get("programmes", []):
            Programme.objects.create(candidate=candidate, **prog)

        for pub in request.session.get("publications", []):
            Publication.objects.create(candidate=candidate, **pub)

        for i in range(len(request.POST.getlist("ref_name[]"))):
            Referee.objects.create(
                candidate=candidate,
                name=request.POST.getlist("ref_name[]")[i],
                designation=request.POST.getlist("ref_designation[]")[i],
                organization=request.POST.getlist("ref_organization[]")[i],
                contact_number=request.POST.getlist("ref_contact[]")[i],
            )

        # 🔥 APPLICATION USAGE LOG (FINAL & CORRECT)
        try:
            ApplicationUsageLog.objects.create(
                candidate=candidate,
                ip_address=get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                device_type="Mobile"
                if "Mobile" in request.META.get("HTTP_USER_AGENT", "")
                else "Desktop",
                action="FORM_SUBMITTED",
            )
        except Exception:
            pass

        # -------- CLEANUP --------
        request.session.flush()
        return redirect("application_success")

    return render(
        request,
        "faculty_requirement/faculty/referees_and_declaration.html",
        {"referees": []},
    )

def application_success(request):
    return render(request, "faculty_requirement/faculty/application_success.html")