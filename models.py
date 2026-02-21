from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class Investigator(models.Model):
    investigator_id = models.ForeignKey(Login,on_delete=models.CASCADE)
    username = models.CharField(max_length=20,null=True)
    name = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    image = models.ImageField(upload_to='Image',null=True)

class Victim(models.Model):
    victim_id = models.ForeignKey(Login,on_delete=models.CASCADE)
    username = models.CharField(max_length=20,null=True)
    name = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    image = models.ImageField(upload_to='Image',null=True)

# models.py
class Case(models.Model):
    case_title = models.CharField(max_length=200)
    case_description = models.TextField()
    victim = models.ForeignKey(Victim, on_delete=models.CASCADE)
    investigator = models.ForeignKey(Investigator, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed')],
        default='Open'
    )
    incident_place = models.CharField(max_length=255, null=True)
    image1 = models.ImageField(upload_to="case_images/", null=True, blank=True)
    image2 = models.ImageField(upload_to="case_images/", null=True, blank=True)
    image3 = models.ImageField(upload_to="case_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    evidence_description = models.TextField(null=True, blank=True)
    evidence_image1 = models.ImageField(upload_to="evidence_images/", null=True, blank=True)
    evidence_image2 = models.ImageField(upload_to="evidence_images/", null=True, blank=True)
    evidence_image3 = models.ImageField(upload_to="evidence_images/", null=True, blank=True)

    # 🆕 Video upload + detection fields
    evidence_video = models.FileField(upload_to="evidence_videos/", null=True, blank=True)
    video_verdict = models.CharField(max_length=30, null=True, blank=True)  # "Real" / "AI-Generated" / "Uncertain"
    video_confidence = models.FloatField(null=True, blank=True)

    witness_statements = models.TextField(null=True, blank=True)
    forensic_report = models.TextField(null=True, blank=True)
    suspect_details = models.TextField(null=True, blank=True)
    victim_details = models.TextField(null=True, blank=True)

    requested_investigator = models.ForeignKey(
        Investigator, on_delete=models.SET_NULL, null=True, blank=True, related_name='requested_cases'
    )
    updated_at = models.DateTimeField(auto_now=True)


class Suspect(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="suspect_images/", null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=[('Under Investigation', 'Under Investigation'), ('Arrested', 'Arrested'), ('Released', 'Released')], 
        default='Under Investigation'
    )

class CaseAnalysis(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE) 
    investigator = models.ForeignKey(Investigator, on_delete=models.CASCADE)  
    analysis_summary = models.TextField(null=True, blank=True)
    identified_suspect = models.ForeignKey(Suspect, on_delete=models.SET_NULL, null=True, blank=True) 
    identified_suspect1 = models.CharField(max_length=255, null=True, blank=True,default='pending') 
    final_conclusion = models.CharField(
        max_length=50, 
        choices=[('Open', 'Open'), ('Solved', 'Solved'), ('Closed', 'Closed')],
        default='Open'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class Chat(models.Model):
    sellerid = models.ForeignKey(Investigator, on_delete=models.CASCADE)
    customerid = models.ForeignKey(Victim, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)

class Court1(models.Model):
    court_idd = models.ForeignKey(Login, on_delete=models.CASCADE)
    court_name = models.CharField(max_length=100)
    court_type = models.CharField(max_length=100)
    judge_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    court_image = models.ImageField(upload_to='court_images/', null=True, blank=True)

    def __str__(self):
        return self.court_name
