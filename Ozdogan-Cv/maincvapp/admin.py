from django.contrib import admin
from .models import Skills, Certificates, CertificateGroups, WorkExperience, Languages

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Certificates)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'issued_by', 'date_issued', 'credential_id', 'credential_url')
    search_fields = ('name', 'issued_by', 'credential_id')
    ordering = ('-date_issued',)
    
@admin.register(CertificateGroups)
class CertificateGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','issued_by', 'date_issued', 'credential_id', 'credential_url')
    search_fields = ('name',)
    ordering = ('-date_issued',)

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'company_name', 'start_date', 'end_date', 'is_current', 'location')
    search_fields = ('job_title', 'company_name', 'location')
    ordering = ('-start_date',)

@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'details', 'picture')
    search_fields = ('name',)