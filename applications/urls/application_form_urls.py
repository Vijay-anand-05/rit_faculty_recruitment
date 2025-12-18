from django.urls import path, include
from applications.urls import main_fr_urls
from applications.views import main_fr_views, application_form_views

urlpatterns = [
   path("", main_fr_views.index, name="index"),


   path(
        "candidate-personal-information/",
        application_form_views.candidate_personal_information,
        name="candidate_personal_information"
    ),

    path(
        "position-and-employment/",
        application_form_views.position_and_employment,
        name="position_and_employment"
    ),

    path(
        "educational-qualifications/",
        application_form_views.educational_qualifications,
        name="educational_qualifications"
    ),

    path(
        "academic-experience/",
        application_form_views.academic_experience,
        name="academic_experience"
    ),

    path(
        "industry-and-research-experience/",
        application_form_views.industry_experience,
        name="industry_experience"
    ),

    path(
        "teaching-experience/",
        application_form_views.teaching_experience,
        name="teaching_experience"
    ),

    path(
        "research-publications/",
        application_form_views.research_publications,
        name="research_publications"
    ),

    path(
        "contributions-and-events/",
        application_form_views.contributions_and_events,
        name="contributions_and_events"
    ),

    path(
        "referees/",
        application_form_views.referees,
        name="referees"
    ),

    path(
        "final-declaration-and-submit/",
        application_form_views.final_declaration_and_submit,
        name="final_declaration_and_submit"
    ),

    path(
        "application-submitted/",
        application_form_views.application_success,
        name="application_success"
    ),
]
