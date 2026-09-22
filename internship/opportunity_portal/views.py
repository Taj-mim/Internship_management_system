from .forms import ApplicationForm
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Apply as Application
from django.contrib.auth.decorators import login_required
from accounts.models import User, Apply, Organization
from accounts.notifications import notify_user
from django.contrib import messages
from django.db.models import Q
from .models import Job, Bookmark

def job_list(request):

    jobs = Job.objects.all().order_by(
        '-created_at'
    )

    search = request.GET.get(
        'search',
        ''
    )

    location = request.GET.get(
        'location',
        ''
    )

    job_type = request.GET.get(
        'job_type',
        ''
    )


    # SEARCH FILTER

    if search:

        jobs = jobs.filter(

            Q(title__icontains=search) |

            Q(organization__icontains=search) |

            Q(description__icontains=search)

        )


    # LOCATION FILTER

    if location:

        jobs = jobs.filter(
            location__icontains=location
        )


    # JOB TYPE FILTER

    if job_type:

        jobs = jobs.filter(
            job_type=job_type
        )


    # BOOKMARKED JOB IDS

    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related(
        'job'
    ).order_by(
        '-created_at'
    )

    bookmarked_jobs = list(
        bookmarks.values_list(
            'job_id',
            flat=True
        )
    ) if request.user.is_authenticated else []

    return render(
        request,
        'opportunity_portal/job_list.html',
        {
            'jobs': jobs,
            'search': search,
            'location': location,
            'job_type': job_type,
            'bookmarked_jobs': bookmarked_jobs,
            'bookmarks': bookmarks,
        }
    )


@login_required
def apply_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )


    # CHECK USER ROLE

    try:

        role = request.user.role

    except:

        messages.error(
            request,
            'Please create an applicant profile first.'
        )

        return redirect('job_list')


    if request.user.role != User.Role.STUDENT:

        messages.error(
            request,
            'Only applicants can apply for jobs.'
        )

        return redirect('job_list')


    # CHECK DUPLICATE APPLICATION

    already_applied = Application.objects.filter(
        job=job,
        user=request.user
    ).exists()


    if already_applied:

        messages.warning(
            request,
            'You have already applied for this job.'
        )

        return redirect(
            'applicant_dashboard'
        )


    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )


        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.job = job

            application.user = request.user

            application.save()

            # Notify the organization that owns this job posting

            organization = Organization.objects.filter(
                organization_name=job.organization
            ).select_related('user').first()

            if organization:

                notify_user(
                    organization.user,
                    f'{request.user.get_full_name() or request.user.username} '
                    f'applied for "{job.title}".'
                )

            messages.success(
                request,
                'Your application has been submitted successfully!'
            )


            return redirect(
                'applicant_dashboard'
            )


    else:

        form = ApplicationForm(
        initial={
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
        }
    )


    return render(
        request,
        'opportunity_portal/apply.html',
        {
            'form': form,
            'job': job
        }
    )


@login_required
def bookmark_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )


    bookmark = Bookmark.objects.filter(
        job=job,
        user=request.user
    ).first()


    if bookmark:

        bookmark.delete()

        messages.success(
            request,
            'Job removed from bookmarks.'
        )

    else:

        Bookmark.objects.create(
            job=job,
            user=request.user
        )

        messages.success(
            request,
            'Job bookmarked successfully! 🔖'
        )


    return redirect(
        'job_list'
    )


@login_required
def applicant_dashboard(request):

    try:
        role = request.user.role

        if role != User.Role.STUDENT:
            messages.error(
                request,
                "You do not have permission to access the student dashboard."
            )
            return redirect("dashboard")

    except Exception:
        messages.error(
            request,
            "Unable to verify your account role."
        )
        return redirect("dashboard")

    applications = Apply.objects.filter(
        user=request.user
    ).select_related(
        'job'
    ).order_by(
        '-applied_date'
    )

    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related(
        'job'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        "opportunity_portal/applicant_dashboard.html",
        {
            "applications": applications,
            "bookmarks": bookmarks
        }
    )