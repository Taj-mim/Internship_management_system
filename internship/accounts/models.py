from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from opportunity_portal.models import Job


# =========================================================
# USER
# =========================================================

class CustomUserManager(UserManager):

    def create_superuser(
        self,
        username,
        email=None,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.model(
            username=username,
            email=email,
            role=User.Role.ADMIN,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):

    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        COMPANY = "COMPANY", "Company"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} - {self.role}"


# =========================================================
# ORGANIZATION
# =========================================================

class Organization(models.Model):

    organization_id = models.AutoField(
        primary_key=True
    )

    organization_name = models.CharField(
        max_length=255
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    # Company account
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="organization",
        limit_choices_to={"role": User.Role.COMPANY}
    )

    def __str__(self):
        return self.organization_name


# =========================================================
# APPLY
# =========================================================

class Apply(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    # Applicant
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications",
        limit_choices_to={"role": User.Role.STUDENT}
    )

    full_name = models.CharField(
        max_length=255
    )

    email = models.EmailField()
    phone = models.CharField(max_length=20,default="18000000000")

    # Resume
    resume_file = models.FileField(
        upload_to="resumes/"
    )

    resume_file_name = models.CharField(
        max_length=255,
        blank=True
    )

    # Cover Letter
    cover_letter_file = models.FileField(
        upload_to="cover_letters/",
        blank=True,
        null=True
    )

    cover_letter_file_name = models.CharField(
        max_length=255,
        blank=True
    )

    # Application status
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        ACCEPTED = "Accepted", "Accepted"
        REJECTED = "Rejected", "Rejected"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    applied_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"





# =========================================================
# NOTIFICATION
# =========================================================

class Notification(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    # Recipient account (preferred way to target a notification)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user or self.email}: {self.message[:40]}"