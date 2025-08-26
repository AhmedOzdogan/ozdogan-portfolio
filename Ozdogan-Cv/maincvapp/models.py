from django.db import models
from sortedm2m.fields import SortedManyToManyField

class Skills(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Certificates(models.Model):
    name = models.CharField(max_length=255)
    issued_by = models.CharField(max_length=255)
    date_issued = models.DateField()
    credential_id = models.CharField(max_length=255, null=True, blank=True)
    credential_url = models.URLField(max_length=255, null=True, blank=True)
    skills = models.ManyToManyField("Skills", related_name="certificates")

    def __str__(self):
        return self.name


class CertificateGroups(models.Model):
    name = models.CharField(max_length=255)
    certificates = SortedManyToManyField(
        Certificates,
        related_name="certificate_groups",
        blank=True,
    )
    issued_by = models.CharField(max_length=255, null=True)
    date_issued = models.DateField(null=True)
    credential_id = models.CharField(max_length=255, null=True, blank=True)
    credential_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    
class WorkExperience(models.Model):
    id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    
class Languages(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    details = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='img/', null=True, blank=True)


    def __str__(self):
        return f"{self.name} ({self.details})"