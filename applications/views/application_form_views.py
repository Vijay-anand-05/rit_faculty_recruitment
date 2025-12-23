from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from applications.models import (
    Candidate,
    Document,
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
    ProgrammesPublications, Degree, Designation, Department, LevelOfEducation, Document_Type, Document, Certificate_Permission,
)
import os
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
        data = {}
        post = request.POST

        data["name"] = post.get("name")
        data["age"] = to_int(post.get("age"))
        data["present_organization"] = post.get("present_organization")
        data["overall_specialization"] = post.get("overall_specialization", "").strip()
        data["specialization"] = data["overall_specialization"]

        data["position_applied"] = to_int(post.get("position_applied"), None)
        data["present_designation"] = to_int(post.get("present_designation"), None)
        data["department"] = to_int(post.get("department"), None)

        # ✅ TEMP PROFILE IMAGE (ONLY ONCE)
        if request.FILES.get("photo"):
            if not request.session.session_key:
                request.session.save()

            tmp_path = default_storage.save(
                f"tmp/profile_{request.session.session_key}_{request.FILES['photo'].name}",
                request.FILES["photo"]
            )
            request.session["photo_tmp_path"] = tmp_path


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

        for f in numeric_fields:
            data[f] = to_int(post.get(f))

        data["journal_publications"] = data["journal_national"] + data["journal_international"]
        data["conference_publications"] = data["conference_national"] + data["conference_international"]
        data["students_guided_completed"] = data["mtech_completed"] + data["phd_completed"]
        data["students_guided_ongoing"] = data["mtech_ongoing"] + data["phd_ongoing"]

        request.session["summary"] = data
        return redirect("individual_data_sheet")

    raw = request.session.get("summary", {})

    hydrated = raw.copy()
    hydrated["position_applied"] = (
    Designation.objects.filter(id=raw.get("position_applied")).first()
    if raw.get("position_applied") else None
)
    hydrated["present_designation"] = (
    Designation.objects.filter(id=raw.get("present_designation")).first()
    if raw.get("present_designation") else None
)

    hydrated["department"] = (
    Department.objects.filter(id=raw.get("department")).first()
    if raw.get("department") else None
)

    return render(
        request,
        "faculty_requirement/faculty/individual_summary_sheet.html",
        {
            "data": hydrated,
            "designations": Designation.objects.all(),
            "departments": Department.objects.all(),
            "degrees": Degree.objects.all().order_by("degree"),
        },
    )




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


from django.core.files.storage import default_storage

def teaching_and_contributions(request):

    subjects = request.session.get("subjects", [])
    contributions = request.session.get("contributions", [])
    summary = request.session.get("summary", {})

    department_id = summary.get("department")

    all_documents = Document_Type.objects.all()

    required_doc_ids = set(
        Certificate_Permission.objects.filter(
            department_id=department_id,
            is_required=True
        ).values_list("document_type_id", flat=True)
    )

    uploaded_docs = request.session.get("uploaded_documents", {})

    if request.method == "POST":

        subjects = (
            [{"level": "UG", "subject_and_result": s}
             for s in request.POST.getlist("ug_subjects[]")] +
            [{"level": "PG", "subject_and_result": s}
             for s in request.POST.getlist("pg_subjects[]")]
        )

        contributions = (
            [{"level": "Department", "description": d}
             for d in request.POST.getlist("department_contributions[]")] +
            [{"level": "College", "description": c}
             for c in request.POST.getlist("college_contributions[]")]
        )

        # ✅ TEMP DOCUMENT UPLOAD (MERGE)
        for doc in all_documents:
            field = f"document_{doc.id}"
            if field in request.FILES:
                tmp_path = default_storage.save(
                    f"tmp/doc_{doc.id}_{request.FILES[field].name}",
                    request.FILES[field]
                )
                uploaded_docs[str(doc.id)] = tmp_path

        missing_required = [
            doc.document_type
            for doc in all_documents
            if doc.id in required_doc_ids and str(doc.id) not in uploaded_docs
        ]

        if missing_required:
            return render(
                request,
                "faculty_requirement/faculty/teaching_and_contributions.html",
                {
                    "subjects": subjects,
                    "contributions": contributions,
                    "all_documents": all_documents,
                    "required_doc_ids": required_doc_ids,
                    "uploaded_docs": [
                        {"id": int(k), "name": os.path.basename(v)}
                        for k, v in uploaded_docs.items()
                    ],
                    "error": f"Required documents missing: {', '.join(missing_required)}",
                },
            )

        request.session["subjects"] = subjects
        request.session["contributions"] = contributions
        request.session["uploaded_documents"] = uploaded_docs

        return redirect("programmes_and_publications")

    return render(
        request,
        "faculty_requirement/faculty/teaching_and_contributions.html",
        {
            "subjects": subjects,
            "contributions": contributions,
            "all_documents": all_documents,
            "required_doc_ids": required_doc_ids,
            "uploaded_docs": [
                {"id": int(k), "name": os.path.basename(v)}
                for k, v in uploaded_docs.items()
            ],
        },
    )



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
            photo=None,
            
        )
                # ---------- SAVE PROFILE IMAGE ----------

        # 🔥 UNIQUE BASE FOLDER
        import re
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", candidate.name)
        base_path = f"candidate/{safe_name}-{candidate.id}"

        # ================= PROFILE IMAGE =================
        photo_tmp = request.session.get("photo_tmp_path")
        if photo_tmp:
            with default_storage.open(photo_tmp, "rb") as f:
                candidate.photo.save(
                    f"{base_path}/profile/profile.jpg",
                    ContentFile(f.read()),
                    save=True
                )
            default_storage.delete(photo_tmp)

        # ================= DOCUMENTS =================
        uploaded_docs = request.session.get("uploaded_documents", {})
        for doc_id, tmp_path in uploaded_docs.items():
            doc_type = Document_Type.objects.filter(id=int(doc_id)).first()
            if not doc_type:
                continue
            ext = os.path.splitext(tmp_path)[1]

            filename = (
                f"{safe_name}-{candidate.id}_"
                f"{doc_type.document_type.upper().replace(' ', '_')}{ext}"
            )

            with default_storage.open(tmp_path, "rb") as f:
                Document.objects.create(
                    candidate=candidate,
                    document_type=doc_type,
                    file=ContentFile(
                        f.read(),
                        name=f"{base_path}/documents/{filename}"
                    )
                )
            default_storage.delete(tmp_path)
        # ================= RESOLVE FOREIGN KEYS =================
        position_applied = Designation.objects.filter(
            id=summary.get("position_applied")
        ).first()

        present_designation = Designation.objects.filter(
            id=summary.get("present_designation")
        ).first()

        department = Department.objects.filter(
            id=summary.get("department")
        ).first()

        # ================= POSITION APPLICATION =================
        PositionApplication.objects.create(
            candidate=candidate,
            position_applied=position_applied,
            department=department,
            present_designation=present_designation,
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



