from django.contrib import admin
from .models import Company, Interview

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'tag')
    list_filter = ('company',)
    search_fields = ('name', 'company__name', 'tag')
    prepopulated_fields = {'slug': ('name',)}