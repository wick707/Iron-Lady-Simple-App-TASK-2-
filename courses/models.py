from django.db import models
from django.urls import reverse

class Course(models.Model):
    name = models.CharField(max_length=200)
    overview = models.TextField()
    target_audience = models.TextField()
    duration = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    fee = models.CharField(max_length=100)
    certificate_provided = models.BooleanField(default=False)
    interests_aligned = models.TextField(help_text="List interests, one per line.")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Redirect to the dashboard after a course is created or updated
        return reverse('dashboard')

