from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=200,null=True)
    age = models.IntegerField(null=True)
    date_of_birth = models.DateField(null=True)

    gender = models.CharField(max_length=20,null=True)
    marital_status = models.CharField(max_length=20,null=True)

    community = models.CharField(max_length=100,null=True)
    caste = models.CharField(max_length=100,null=True)

    pan_number = models.CharField(max_length=20,null=True)

    email = models.EmailField(null=True)
    phone_primary = models.CharField(max_length=100,null=True)
    phone_secondary = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to="candidate_photos/", null=True, blank=True)
    address = models.TextField()

    total_experience_years = models.IntegerField(null=True)
    present_post_years = models.IntegerField(null=True)

    mother_name_and_occupation = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class PositionApplication(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    position_applied = models.CharField(max_length=100,null=True)
    department = models.CharField(max_length=100,null=True)

    present_designation = models.CharField(max_length=200,null=True)
    present_organization = models.CharField(max_length=200,null=True)

    specialization = models.CharField(max_length=100,null=True)

    assistant_professor_years = models.IntegerField(default=0)
    associate_professor_years = models.IntegerField(default=0)
    professor_years = models.IntegerField(default=0)
    other_years = models.IntegerField(default=0, blank=True)

    research_experience_years = models.IntegerField(default=0)
    industry_experience_years = models.IntegerField(default=0)

    journal_publications = models.IntegerField(default=0)
    conference_publications = models.IntegerField(default=0)

    students_guided_completed = models.IntegerField(default=0)
    students_guided_ongoing = models.IntegerField(default=0)

    community_and_caste = models.CharField(max_length=100)


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
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE,null=True)

    mode_ug = models.CharField(max_length=10,null=True)
    mode_pg = models.CharField(max_length=10,null=True)
    mode_phd = models.CharField(max_length=20,null=True)

    arrears_ug = models.IntegerField(default=0)
    arrears_pg = models.IntegerField(default=0)

    gate_score = models.CharField(max_length=50, blank=True,null=True)
    net_slet_score = models.CharField(max_length=50, blank=True,null=True)

    me_thesis_title = models.TextField(blank=True,null=True)
    phd_thesis_title = models.TextField(blank=True,null=True)



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
    contact_number = models.CharField(max_length=20)
