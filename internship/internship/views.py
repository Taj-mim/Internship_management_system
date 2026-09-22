from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User, Organization
from opportunity_portal.models import Job
from accounts.models import Apply as Application
from accounts.notifications import notify_user
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def index(request):

    latest_jobs = Job.objects.order_by(
        "-created_at"
    )[:6]

    return render(
        request,
        "index.html",
        {
            "jobs": latest_jobs
        }
    )


# =========================================================
# STUDENT CRUD
# =========================================================

@login_required
def student_list(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    students = User.objects.filter(
        role=User.Role.STUDENT
    ).order_by("id")

    return render(
        request,
        "student_list.html",
        {
            "students": students
        }
    )


@login_required
def student_add(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=User.Role.STUDENT
        )

        return redirect("student_list")

    return render(
        request,
        "student_add.html"
    )


@login_required
def student_edit(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    student = get_object_or_404(
        User,
        pk=pk,
        role=User.Role.STUDENT
    )

    if request.method == "POST":

        student.username = request.POST.get("username")
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.email = request.POST.get("email")

        password = request.POST.get("password")

        if password:
            student.set_password(password)

        student.save()

        return redirect("student_list")

    return render(
        request,
        "student_edit.html",
        {
            "student": student
        }
    )


@login_required
def student_delete(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    student = get_object_or_404(
        User,
        pk=pk,
        role=User.Role.STUDENT
    )

    if request.method == "POST":
        student.delete()

    return redirect("student_list")


# =========================================================
# ORGANIZATION CRUD
# =========================================================
@login_required
def CRUD_org(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    organizations = Organization.objects.select_related(
        "user"
    ).order_by(
        "organization_id"
    )

    return render(
        request,
        "CRUD_org.html",
        {
            "organizations": organizations
        }
    )


@login_required
def organization_add(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        organization_name = request.POST.get("organization_name")
        website = request.POST.get("website")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=User.Role.COMPANY
        )

        Organization.objects.create(
            organization_name=organization_name,
            website=website,
            user=user
        )

        return redirect("CRUD_org")

    return render(
        request,
        "organization_add.html"
    )


@login_required
def organization_edit(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    organization = get_object_or_404(
        Organization.objects.select_related("user"),
        pk=pk
    )

    user = organization.user

    if request.method == "POST":

        organization.organization_name = request.POST.get(
            "organization_name"
        )

        organization.website = request.POST.get(
            "website"
        )

        user.username = request.POST.get(
            "username"
        )

        user.email = request.POST.get(
            "email"
        )

        password = request.POST.get("password")

        if password:
            user.set_password(password)

        user.save()
        organization.save()

        return redirect("CRUD_org")

    return render(
        request,
        "organization_edit.html",
        {
            "organization": organization
        }
    )


@login_required
def organization_delete(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    organization = get_object_or_404(
        Organization,
        pk=pk
    )

    if request.method == "POST":
        organization.delete()

    return redirect("CRUD_org")


# =========================================================
# POST / JOB CRUD
# =========================================================

@login_required
def CRUD_post(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    posts = Job.objects.all().order_by("-created_at")

    return render(
        request,
        "CRUD_post.html",
        {
            "posts": posts
        }
    )

@login_required
def post_add(request):

    # Only ADMIN and COMPANY can create posts
    if request.user.role not in [User.Role.ADMIN, User.Role.COMPANY]:
        return redirect("dashboard")

    # Get the organization of the logged-in company user
    organization = None

    if request.user.role == User.Role.COMPANY:
        organization = get_object_or_404(
            Organization,
            user=request.user
        )

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        job_type = request.POST.get("job_type")
        salary = request.POST.get("salary")
        deadline = request.POST.get("deadline")

        # ADMIN can choose any organization
        if request.user.role == User.Role.ADMIN:
            organization_name = request.POST.get("organization")

        # COMPANY can ONLY post for itself
        else:
            organization_name = organization.organization_name

        Job.objects.create(
            title=title,
            organization=organization_name,
            description=description,
            location=location,
            job_type=job_type,
            salary=salary,
            deadline=deadline
        )

        messages.success(
            request,
            "Post created successfully."
        )

        # Return to the appropriate dashboard
        if request.user.role == User.Role.ADMIN:
            return redirect("CRUD_post")

        return redirect("dashboard")

    return render(
        request,
        "post_add.html",
        {
            "job_types": Job.JOB_TYPE_CHOICES,
            "organization": organization,
            "is_admin": request.user.role == User.Role.ADMIN,
        }
    )



@login_required
def post_edit(request, pk):
    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    job = get_object_or_404(
        Job,
        pk=pk
    )

    if request.method == "POST":

        job.title = request.POST.get("title")
        job.organization = request.POST.get("organization")
        job.description = request.POST.get("description")
        job.location = request.POST.get("location")
        job.job_type = request.POST.get("job_type")
        job.salary = request.POST.get("salary")
        job.deadline = request.POST.get("deadline")

        job.save()

        return redirect("CRUD_post")

    return render(
        request,
        "post_edit.html",
        {
            "job": job,
            "job_types": Job.JOB_TYPE_CHOICES
        }
    )



@login_required
def post_delete(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    post = get_object_or_404(
        Job,
        pk=pk
    )

    if request.method == "POST":
        post.delete()

    return redirect("CRUD_post")


# =========================================================
# APPLICATIONS (ADMIN)
# =========================================================

@login_required
def CRUD_application(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    applications = Application.objects.select_related(
        "job",
        "user"
    ).order_by("-applied_date")

    return render(
        request,
        "CRUD_application.html",
        {
            "applications": applications
        }
    )


@login_required
def update_application_status(request, application_id, status):

    application = get_object_or_404(
        Application,
        id=application_id
    )

    # Make sure this application belongs to a job
    # posted by the logged-in organization (or an admin)

    is_owner = False

    if request.user.role == User.Role.ADMIN:

        is_owner = True

    else:

        organization = Organization.objects.filter(
            user=request.user
        ).first()

        if organization and application.job.organization == organization.organization_name:
            is_owner = True

    if not is_owner:

        messages.error(
            request,
            'You do not have permission to update this application.'
        )

        return redirect('dashboard')

    if request.method == 'POST':

        if status == 'accepted':

            application.status = 'Accepted'

            application.save()

            notify_user(
                application.user,
                f'Your application for "{application.job.title}" at '
                f'{application.job.organization} has been accepted. 🎉'
            )
            send_application_status_email(
            application,
            "Accepted"
             )

            messages.success(
                request,
                'Application accepted successfully.'
            )

        elif status == 'rejected':

            application.status = 'Rejected'

            application.save()

            notify_user(
                application.user,
                f'Your application for "{application.job.title}" at '
                f'{application.job.organization} has been rejected.'
            )

            send_application_status_email(
                application,
                "Rejected"
            )

            messages.success(
                request,
                'Application rejected successfully.'
            )

        else:

            messages.error(
                request,
                'Invalid application status.'
            )

    if request.user.role == User.Role.ADMIN:
        return redirect('CRUD_application')

    return redirect(
        'company_dashboard'
    )

def send_application_status_email(application, status):

    print("EMAIL FUNCTION CALLED")
    print("Recipient:", application.email)
    print("Status:", status)

    if status == "Accepted":
        subject = f'Application Accepted - {application.job.title}'
        message = f"""
Dear {application.full_name},

Congratulations!

Your application for the position of "{application.job.title}" at {application.job.organization} has been accepted.

Best regards,
InternHub Team
"""

    elif status == "Rejected":
        subject = f'Application Update - {application.job.title}'
        message = f"""
Dear {application.full_name},

Thank you for applying for the position of "{application.job.title}" at {application.job.organization}.

Unfortunately, your application has not been selected at this time.

Best regards,
InternHub Team
"""

    else:
        return

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[application.email],
        fail_silently=False
    )

    print("EMAIL SENT")