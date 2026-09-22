from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from opportunity_portal.models import Job
from .models import User, Organization, Notification
from .forms import (
    StudentRegistrationForm,
    CompanyRegistrationForm,
)
from .notifications import notify_users
from accounts.models import Apply as Application

# =========================================================
# REGISTER CHOICE
# =========================================================

def register(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(
        request,
        "accounts/register.html"
    )


# =========================================================
# STUDENT REGISTRATION
# =========================================================

def student_register(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            # Save student
            user = form.save()

            # Automatically login after registration
            login(request, user)

            messages.success(
                request,
                f"Welcome {user.first_name or user.username}!"
            )

            # Go directly to student dashboard
            return redirect("applicant_dashboard")

    else:

        form = StudentRegistrationForm()

    return render(
        request,
        "accounts/register_student.html",
        {
            "form": form
        }
    )


# =========================================================
# COMPANY REGISTRATION
# =========================================================

def company_register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = CompanyRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            Organization.objects.create(
                organization_name=form.cleaned_data["organization_name"],
                website=form.cleaned_data["website"],
                user=user
            )

            login(request, user)

            messages.success(
                request,
                f"Welcome {user.username}!"
            )

            return redirect("company_dashboard")

    else:

        form = CompanyRegistrationForm()

    return render(
        request,
        "accounts/register_company.html",
        {
            "form": form
        }
    )
# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    admin_login = request.GET.get("role") == "admin"


    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            # If this is the Admin Login page,
            # only an ADMIN user can log in
            if admin_login and user.role != User.Role.ADMIN:
                messages.error(
                    request,
                    "This account does not have administrator access."
                )
                return redirect("login")

            # Normal login
            # Create login session
            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            # Return the user to the page they were trying to
            # reach before logging in (e.g. "Apply Now"), if any
            next_url = request.POST.get("next") or request.GET.get("next")

            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            # Send user according to role
            return redirect("dashboard")

        # Wrong username/password
        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html",
        {
        "admin_login": admin_login
        }
    )


# =========================================================
# MAIN DASHBOARD REDIRECTION
# =========================================================

@login_required
def dashboard(request):

    # -----------------------------------------------------
    # STUDENT
    # -----------------------------------------------------

    if request.user.role == User.Role.STUDENT:

        return redirect("applicant_dashboard")


    # -----------------------------------------------------
    # COMPANY
    # -----------------------------------------------------

    elif request.user.role == User.Role.COMPANY:

        return redirect("company_dashboard")


    # -----------------------------------------------------
    # ADMIN
    # -----------------------------------------------------

    elif request.user.role == User.Role.ADMIN:

        return redirect("admin_dashboard")


    # -----------------------------------------------------
    # INVALID ROLE
    # -----------------------------------------------------

    else:

        logout(request)

        messages.error(
            request,
            "Invalid user role."
        )

        return redirect("login")

# =========================================================
# COMPANY DASHBOARD
# =========================================================

@login_required
def company_dashboard(request):

    if request.user.role != User.Role.COMPANY:

        messages.error(
            request,
            "You do not have permission to access the company dashboard."
        )

        return redirect("dashboard")

    # Get the organization belonging to this company account
    try:
        organization = request.user.organization
    except Organization.DoesNotExist:

        messages.error(
            request,
            "No organization profile is associated with this account."
        )

        return redirect("dashboard")

    # Get only jobs posted by this organization
    jobs = Job.objects.filter(
        organization=organization.organization_name
    ).order_by(
        "-created_at"
    )

    # Get applications for this organization's jobs
    applications = Application.objects.filter(
        job__in=jobs
    ).select_related(
        "job",
        "user"
    ).order_by(
        "-applied_date"
    )

    return render(
        request,
        "opportunity_portal/organization_dashboard.html",
        {
            "organization": organization,
            "jobs": jobs,
            "applications": applications,
        }
    )

# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required
def admin_dashboard(request):

    # Only admins can access this page
    if request.user.role != User.Role.ADMIN:

        messages.error(
            request,
            "You do not have permission to access the admin dashboard."
        )

        return redirect("dashboard")

    # -----------------------------------------------------
    # SEND NOTIFICATION (admin broadcast form)
    # -----------------------------------------------------

    if request.method == "POST" and request.POST.get("form_type") == "send_notification":

        audience = request.POST.get("audience")
        message_text = request.POST.get("message", "").strip()

        if not message_text:

            messages.error(
                request,
                "Notification message cannot be empty."
            )

        else:

            if audience == "students":
                targets = User.objects.filter(role=User.Role.STUDENT)

            elif audience == "companies":
                targets = User.objects.filter(role=User.Role.COMPANY)

            else:
                targets = User.objects.exclude(role=User.Role.ADMIN)

            notify_users(targets, message_text)

            messages.success(
                request,
                f"Notification sent to {targets.count()} user(s)."
            )

        return redirect("admin_dashboard")

    # -----------------------------------------------------
    # STAT CARDS
    # -----------------------------------------------------

    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()
    total_applicants = User.objects.filter(role=User.Role.STUDENT).count()
    total_organizations = Organization.objects.count()

    # -----------------------------------------------------
    # RECENT ACTIVITY
    # -----------------------------------------------------

    recent_jobs = Job.objects.order_by("-created_at")[:5]

    # -----------------------------------------------------
    # JOB POSTING TREND (last 7 days)
    # -----------------------------------------------------

    today = timezone.localdate()
    days = [today - timedelta(days=offset) for offset in range(6, -1, -1)]

    chart_labels = [day.strftime("%a") for day in days]

    chart_data = [
        Job.objects.filter(created_at__date=day).count()
        for day in days
    ]

    # -----------------------------------------------------
    # NOTIFICATIONS SENT (recent)
    # -----------------------------------------------------

    recent_notifications = Notification.objects.order_by("-created_at")[:8]

    return render(
        request,
        "accounts/admin_dashboard.html",
        {
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "total_applicants": total_applicants,
            "total_organizations": total_organizations,
            "recent_jobs": recent_jobs,
            "chart_labels": chart_labels,
            "chart_data": chart_data,
            "recent_notifications": recent_notifications,
        }
    )


# =========================================================
# NOTIFICATIONS
# =========================================================

@login_required
def notifications_view(request):

    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "accounts/notifications.html",
        {
            "notifications": user_notifications
        }
    )


@login_required
def mark_notification_read(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        notification.is_read = True
        notification.save()

    return redirect("notifications")


@login_required
def mark_all_notifications_read(request):

    if request.method == "POST":

        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)

        messages.success(
            request,
            "All notifications marked as read."
        )

    return redirect("notifications")


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    # Destroy login session
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    # After logout user MUST login again
    return redirect("login")

def home(request):
    latest_jobs = Job.objects.order_by("-created_at")
    return render(request, "accounts/home.html", {
            "jobs": latest_jobs
        })