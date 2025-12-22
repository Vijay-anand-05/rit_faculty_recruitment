import os
from django.db import models

from django.db import models
from django.contrib.auth.models import User

import os
from applications.utils import candidate_photo_path


# def candidate_photo_path(instance, filename):
#     # Clean name for folder (avoid spaces & special chars)
#     name = instance.name.replace(" ", "_") if instance.name else "unknown"
#     return os.path.join("candidate_photos", name, filename)


class Candidate(models.Model):
    name = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)
    date_of_birth = models.DateField(null=True)

    gender = models.CharField(max_length=20, null=True)
    marital_status = models.CharField(max_length=20, null=True)

    community = models.CharField(max_length=100, null=True)
    caste = models.CharField(max_length=100, null=True)

    pan_number = models.CharField(max_length=20, null=True)

    email = models.EmailField(null=True)
    phone_primary = models.CharField(max_length=100, null=True)
    phone_secondary = models.CharField(max_length=100, blank=True)

    photo = models.ImageField(
        upload_to=candidate_photo_path,
        null=True,
        blank=True
    )

    address = models.TextField()

    total_experience_years = models.IntegerField(null=True)
    present_post_years = models.IntegerField(null=True)

    mother_name_and_occupation = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name



# models.py

class PositionApplication(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    position_applied = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)

    present_designation = models.CharField(max_length=200, null=True, blank=True)
    present_organization = models.CharField(max_length=200, null=True, blank=True)

    specialization = models.CharField(max_length=200, null=True, blank=True)

    assistant_professor_years = models.PositiveIntegerField(default=0)
    associate_professor_years = models.PositiveIntegerField(default=0)
    professor_years = models.PositiveIntegerField(default=0)
    other_years = models.PositiveIntegerField(default=0)

    research_experience_years = models.PositiveIntegerField(default=0)
    industry_experience_years = models.PositiveIntegerField(default=0)

    journal_publications = models.PositiveIntegerField(default=0)
    conference_publications = models.PositiveIntegerField(default=0)

    students_guided_completed = models.PositiveIntegerField(default=0)
    students_guided_ongoing = models.PositiveIntegerField(default=0)

    community_and_caste = models.CharField(max_length=150, null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True)


class Qualification(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    qualification = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    institute = models.CharField(max_length=200, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)


class SponsoredProject(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    title = models.CharField(max_length=300)
    duration = models.CharField(max_length=50, null=True, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    agency = models.CharField(max_length=200, null=True, blank=True)


class Education(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    category = models.CharField(max_length=20,null=True)  # SSLC / HSC / UG / PG / PhD
    degree = models.CharField(max_length=100,null=True)
    specialization = models.CharField(max_length=100, blank=True,null=True)

    year_of_passing = models.CharField(max_length=10,null=True)
    institution = models.CharField(max_length=200,null=True)
    university = models.CharField(max_length=200,null=True)

    percentage = models.CharField(max_length=20,null=True)
    class_obtained = models.CharField(max_length=50,null=True)



class ResearchDetails(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)

    mode_ug = models.CharField(max_length=30, null=True, blank=True)
    mode_pg = models.CharField(max_length=30, null=True, blank=True)
    mode_phd = models.CharField(max_length=30, null=True, blank=True)

    arrears_ug = models.IntegerField(null=True, blank=True)
    arrears_pg = models.IntegerField(null=True, blank=True)

    gate_score = models.CharField(max_length=50, null=True, blank=True)
    net_slet_score = models.CharField(max_length=50, null=True, blank=True)

    me_thesis_title = models.TextField(null=True, blank=True)
    phd_thesis_title = models.TextField(null=True, blank=True)



class AcademicExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    institution = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)

    joining_date = models.DateField(null=True)
    relieving_date = models.CharField(max_length=50, blank=True)  # "Till Date" allowed

    years = models.IntegerField(null=True)
    months = models.IntegerField(null=True)
    days = models.IntegerField(null=True)




class IndustryExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    organization = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)
    nature_of_work = models.CharField(max_length=200)

    joining_date = models.DateField(null=True)
    relieving_date = models.DateField(null=True)

    years = models.IntegerField(null=True)
    months = models.IntegerField(null=True)
    days = models.IntegerField(null=True)



class TeachingSubject(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    level = models.CharField(max_length=10)  # UG / PG
    subject_and_result = models.CharField(max_length=200)



class Contribution(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    level = models.CharField(max_length=50)  # Department / College
    description = models.CharField(max_length=200)



class Programme(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    programme_type = models.CharField(max_length=50)  # Workshop / FDP etc
    category = models.CharField(max_length=50, null=True)        # Participated / Organized
    count = models.IntegerField()


class Publication(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE,null=True)

    title = models.TextField()
    indexing = models.CharField(max_length=100, null=True)



class Referee(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)

    contact_number = models.CharField(max_length=15)




class Document(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to="candidate_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)




class AdminLoginLog(models.Model):
    ACTION_CHOICES = (
        ("LOGIN_SUCCESS", "Login Success"),
        ("LOGIN_FAILED", "Login Failed"),
        ("LOGOUT", "Logout"),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    username_attempted = models.CharField(max_length=150, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)

    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    session_key = models.CharField(max_length=40, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Admin Login Log"
        verbose_name_plural = "Admin Login Logs"

    def __str__(self):
        return f"{self.username_attempted} - {self.action} - {self.timestamp}"

class VisitorLog(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_type = models.CharField(max_length=50)
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["ip_address"]),
            models.Index(fields=["timestamp"]),
        ]

class ApplicationUsageLog(models.Model):
    ACTION_CHOICES = [
        ("FORM_SUBMITTED", "Form Submitted"),
    ]

    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="usage_logs"
    )

    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_type = models.CharField(max_length=50)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    timestamp = models.DateTimeField(auto_now_add=True)


# models.py
class ProgrammesPublications(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="programmes_publications"
    )

    programmes = models.CharField(max_length=1000, default="", null=True)
    publications = models.CharField(max_length=1000, default="", null=True)

    research_publications_details = models.CharField(max_length=1000, default="", null=True)
    research_scholars_details = models.TextField(blank=True, null=True)

    sponsored_projects = models.CharField(max_length=1000, default="", null=True)
    memberships = models.CharField(max_length=1000, default="", null=True)
    awards = models.CharField(max_length=1000, default="", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Programmes & Publications - {self.candidate.name}"

# === Organization Masters ===
class Degree(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    # New fields
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    degree = models.ForeignKey('Degree', on_delete=models.SET_NULL, null=True, blank=True, related_name='departments')

    def __str__(self) -> str:
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.name


class LevelOfEducation(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.name


