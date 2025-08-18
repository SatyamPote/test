from django.db import models
from django.utils.text import slugify

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='company_logos/', help_text="Upload the company's main logo.")

    def __str__(self):
        return self.name

class Interview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='interviews')
    name = models.CharField(max_length=200, help_text="e.g., AWS Full Stack Interview")
    logo_image = models.ImageField(upload_to='interview_logos/', help_text="The logo for the interview card (e.g., Amazon logo).")
    tag = models.CharField(max_length=100, help_text="e.g., Mix Between Behavioral And Technical")
    short_description = models.TextField(help_text="A short enticing description for the card.")
    job_description_for_ai = models.TextField(help_text="The full, detailed job description to be sent to the AI Interviewer API.")
    slug = models.SlugField(unique=True, blank=True, help_text="A unique URL-friendly version of the name. Will be auto-generated.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} at {self.company.name}"