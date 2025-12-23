from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from applications.models import *

# =================================================
# LIST PAGE
# =================================================
def faculty_data(request):
    applications = []

    for c in Candidate.objects.all().order_by('name'):
        pos = PositionApplication.objects.filter(candidate=c).last()
        applications.append({
            'candidate': c,
            'position': pos or PositionApplication()
        })

    sections = [
        {'key': 'candidate', 'label': 'Candidate'},
        {'key': 'position', 'label': 'Position'},
        {'key': 'qualification', 'label': 'Qualification'},
        {'key': 'sponsored_project', 'label': 'Sponsored'},
        {'key': 'education', 'label': 'Education'},
        {'key': 'research_details', 'label': 'Research'},
        {'key': 'academic_experience', 'label': 'Academic'},
        {'key': 'industry_experience', 'label': 'Industry'},
        {'key': 'teaching_subject', 'label': 'Teaching'},
        {'key': 'contribution', 'label': 'Contribution'},
        {'key': 'programme', 'label': 'Programme'},
        {'key': 'publication', 'label': 'Publication'},
        {'key': 'referee', 'label': 'Referee'},
    ]

    return render(
        request,
        "faculty_requirement/admin/faculty/faculty_data.html",
        {'applications': applications, 'sections': sections}
    )


# =================================================
# DETAIL PAGE (VIEW ALL DATA)
# =================================================
def faculty_application_details(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    position = PositionApplication.objects.filter(candidate=candidate).last() or PositionApplication()

    context = {
        'candidate': candidate,
        'position': position,
        'qualification': Qualification.objects.filter(candidate=candidate),
        'sponsored_projects': SponsoredProject.objects.filter(candidate=candidate),
        'education': Education.objects.filter(candidate=candidate),
        'research_details': ResearchDetails.objects.filter(candidate=candidate).last() or ResearchDetails(),
        'academic': AcademicExperience.objects.filter(candidate=candidate),
        'industry': IndustryExperience.objects.filter(candidate=candidate),
        'teaching': TeachingSubject.objects.filter(candidate=candidate),
        'contributions': Contribution.objects.filter(candidate=candidate),
        'programmes': Programme.objects.filter(candidate=candidate),
        'publications': Publication.objects.filter(candidate=candidate),
        'referees': Referee.objects.filter(candidate=candidate),
    }

    return render(
        request,
        "faculty_requirement/admin/faculty/faculty_application_details.html",
        context
    )


# =================================================
# UPDATE SECTION (INLINE SAVE)
# =================================================
def faculty_section_update(request):
    if request.method != 'POST':
        return JsonResponse({'success': False})

    candidate = get_object_or_404(Candidate, id=request.POST.get('candidate_id'))
    section = request.POST.get('section')
    obj_id = request.POST.get('id')

    try:
        if section == 'candidate':
            # Basic
            candidate.name = request.POST.get('name')
            candidate.email = request.POST.get('email')
            candidate.phone_primary = request.POST.get('phone_primary')
            # Extended
            candidate.age = request.POST.get('age') or None
            candidate.date_of_birth = request.POST.get('date_of_birth') or None
            candidate.gender = request.POST.get('gender')
            candidate.marital_status = request.POST.get('marital_status')
            candidate.community = request.POST.get('community')
            candidate.caste = request.POST.get('caste')
            candidate.pan_number = request.POST.get('pan_number')
            candidate.phone_secondary = request.POST.get('phone_secondary')
            candidate.address = request.POST.get('address') or ''
            candidate.total_experience_years = request.POST.get('total_experience_years') or None
            candidate.present_post_years = request.POST.get('present_post_years') or None
            candidate.mother_name_and_occupation = request.POST.get('mother_name_and_occupation')
            candidate.save()

        elif section == 'position':
            obj, _ = PositionApplication.objects.get_or_create(candidate=candidate)
            obj.position_applied = request.POST.get('position_applied')
            obj.department = request.POST.get('department')
            obj.present_designation = request.POST.get('present_designation')
            obj.present_organization = request.POST.get('present_organization')
            obj.specialization = request.POST.get('specialization')
            obj.assistant_professor_years = request.POST.get('assistant_professor_years') or 0
            obj.associate_professor_years = request.POST.get('associate_professor_years') or 0
            obj.professor_years = request.POST.get('professor_years') or 0
            obj.other_years = request.POST.get('other_years') or 0
            obj.research_experience_years = request.POST.get('research_experience_years') or 0
            obj.industry_experience_years = request.POST.get('industry_experience_years') or 0
            obj.journal_publications = request.POST.get('journal_publications') or 0
            obj.conference_publications = request.POST.get('conference_publications') or 0
            obj.students_guided_completed = request.POST.get('students_guided_completed') or 0
            obj.students_guided_ongoing = request.POST.get('students_guided_ongoing') or 0
            obj.community_and_caste = request.POST.get('community_and_caste')
            obj.save()

        elif section == 'research_details':
            obj, _ = ResearchDetails.objects.get_or_create(candidate=candidate)
            obj.mode_ug = request.POST.get('mode_ug')
            obj.mode_pg = request.POST.get('mode_pg')
            obj.mode_phd = request.POST.get('mode_phd')
            obj.arrears_ug = request.POST.get('arrears_ug') or None
            obj.arrears_pg = request.POST.get('arrears_pg') or None
            obj.gate_score = request.POST.get('gate_score')
            obj.net_slet_score = request.POST.get('net_slet_score')
            obj.me_thesis_title = request.POST.get('me_thesis_title')
            obj.phd_thesis_title = request.POST.get('phd_thesis_title')
            obj.save()

        elif section == 'education':
            if obj_id:
                obj = get_object_or_404(Education, id=obj_id, candidate=candidate)
            else:
                obj = Education(candidate=candidate)
            obj.category = request.POST.get('category')
            obj.degree = request.POST.get('degree')
            obj.specialization = request.POST.get('specialization')
            obj.year_of_passing = request.POST.get('year_of_passing')
            obj.institution = request.POST.get('institution')
            obj.university = request.POST.get('university')
            obj.percentage = request.POST.get('percentage')
            obj.class_obtained = request.POST.get('class_obtained')
            obj.save()

        elif section == 'qualification':
            if obj_id:
                obj = get_object_or_404(Qualification, id=obj_id, candidate=candidate)
            else:
                obj = Qualification(candidate=candidate)
            obj.qualification = request.POST.get('qualification')
            obj.specialization = request.POST.get('specialization')
            obj.institute = request.POST.get('institute')
            obj.year = request.POST.get('year') or None
            obj.save()

        elif section == 'sponsored_project':
            if obj_id:
                obj = get_object_or_404(SponsoredProject, id=obj_id, candidate=candidate)
            else:
                obj = SponsoredProject(candidate=candidate)
            obj.title = request.POST.get('title')
            obj.duration = request.POST.get('duration')
            obj.amount = request.POST.get('amount') or None
            obj.agency = request.POST.get('agency')
            obj.save()

        elif section == 'academic_experience':
            if obj_id:
                obj = get_object_or_404(AcademicExperience, id=obj_id, candidate=candidate)
            else:
                obj = AcademicExperience(candidate=candidate)
            obj.institution = request.POST.get('institution')
            obj.designation = request.POST.get('designation')
            obj.joining_date = request.POST.get('joining_date') or None
            obj.relieving_date = request.POST.get('relieving_date') or ''
            obj.years = request.POST.get('years') or None
            obj.months = request.POST.get('months') or None
            obj.days = request.POST.get('days') or None
            obj.save()

        elif section == 'industry_experience':
            if obj_id:
                obj = get_object_or_404(IndustryExperience, id=obj_id, candidate=candidate)
            else:
                obj = IndustryExperience(candidate=candidate)
            obj.organization = request.POST.get('organization')
            obj.designation = request.POST.get('designation')
            obj.nature_of_work = request.POST.get('nature_of_work')
            obj.joining_date = request.POST.get('joining_date') or None
            obj.relieving_date = request.POST.get('relieving_date') or None
            obj.years = request.POST.get('years') or None
            obj.months = request.POST.get('months') or None
            obj.days = request.POST.get('days') or None
            obj.save()

        elif section == 'teaching_subject':
            if obj_id:
                obj = get_object_or_404(TeachingSubject, id=obj_id, candidate=candidate)
            else:
                obj = TeachingSubject(candidate=candidate)
            obj.level = request.POST.get('level')
            obj.subject_and_result = request.POST.get('subject_and_result')
            obj.save()

        elif section == 'contribution':
            if obj_id:
                obj = get_object_or_404(Contribution, id=obj_id, candidate=candidate)
            else:
                obj = Contribution(candidate=candidate)
            obj.level = request.POST.get('level')
            obj.description = request.POST.get('description')
            obj.save()

        elif section == 'programme':
            if obj_id:
                obj = get_object_or_404(Programme, id=obj_id, candidate=candidate)
            else:
                obj = Programme(candidate=candidate)
            obj.programme_type = request.POST.get('programme_type')
            obj.category = request.POST.get('category')
            obj.count = request.POST.get('count') or 0
            obj.save()

        elif section == 'publication':
            if obj_id:
                obj = get_object_or_404(Publication, id=obj_id, candidate=candidate)
            else:
                obj = Publication(candidate=candidate)
            obj.title = request.POST.get('title')
            obj.indexing = request.POST.get('indexing')
            obj.save()

        elif section == 'referee':
            if obj_id:
                obj = get_object_or_404(Referee, id=obj_id, candidate=candidate)
            else:
                obj = Referee(candidate=candidate)
            obj.name = request.POST.get('name')
            obj.designation = request.POST.get('designation')
            obj.organization = request.POST.get('organization')
            obj.contact_number = request.POST.get('contact_number')
            obj.save()

        else:
            return JsonResponse({'success': False, 'error': 'Unknown section'})

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
