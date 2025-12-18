from django.db import models

class Candidate(models.Model):
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()

    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=20)

    community = models.CharField(max_length=50)
    caste = models.CharField(max_length=50)

    pan_number = models.CharField(max_length=20)

    email = models.EmailField()
    phone_primary = models.CharField(max_length=15)
    phone_secondary = models.CharField(max_length=15, blank=True)

    address = models.TextField()

    photo = models.ImageField(upload_to="candidate_photos/")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name





class PositionApplication(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    current_designation = models.CharField(max_length=150)
    current_organization = models.CharField(max_length=200)

    years_experience = models.PositiveIntegerField()

    applied_date = models.DateField(auto_now_add=True)




class Education(models.Model):
    DEGREE_LEVELS = [
        ("SSLC", "SSLC"),
        ("HSC", "HSC"),
        ("UG", "UG"),
        ("PG", "PG"),
        ("PHD", "PhD"),
        ("POSTDOC", "Post Doctoral"),
    ]

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    degree_level = models.CharField(max_length=20, choices=DEGREE_LEVELS)
    degree_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True)

    institution = models.CharField(max_length=200)
    university = models.CharField(max_length=200)

    year_of_passing = models.CharField(max_length=10)
    percentage = models.CharField(max_length=10)
    class_obtained = models.CharField(max_length=50)

    mode_of_study = models.CharField(max_length=10)
    arrears = models.PositiveIntegerField(default=0)





class AcademicExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    institution = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)

    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)

    years = models.PositiveIntegerField()
    months = models.PositiveIntegerField()
    days = models.PositiveIntegerField()





class IndustryExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    organization = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)
    nature_of_work = models.CharField(max_length=200)

    from_date = models.DateField()
    to_date = models.DateField()

    years = models.PositiveIntegerField()
    months = models.PositiveIntegerField()
    days = models.PositiveIntegerField()







class Publication(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    title = models.TextField()
    publication_type = models.CharField(max_length=50)  # Journal / Conference
    indexing = models.CharField(max_length=50)  # Scopus / ISBN / ISSN

    year = models.CharField(max_length=10)






class TeachingSubject(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    subject_name = models.CharField(max_length=200)
    level = models.CharField(max_length=10)  # UG / PG
    result_percentage = models.CharField(max_length=10)







class Contribution(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    level = models.CharField(max_length=50)  # Department / College
    role = models.CharField(max_length=200)



class EventParticipation(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    event_type = models.CharField(max_length=50)
    count = models.PositiveIntegerField()



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

