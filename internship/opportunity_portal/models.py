from django.db import models
from django.conf import settings


class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    title = models.CharField(max_length=200)

    organization = models.CharField(max_length=200)

    description = models.TextField()

    location = models.CharField(max_length=200)

    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES
    )

    salary = models.CharField(
        max_length=100,
        blank=True
    )

    deadline = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Bookmark(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('job', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('applicant', 'Applicant'),
        ('organization', 'Organization'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"