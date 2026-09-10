from django.shortcuts import render
from .models import JobPost, Profile, Application
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'location', 'job_type', 'salary', 'skills', 'deadline']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']


def home(request):
    jobs = JobPost.objects.all()

    search = request.GET.get('search')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) | Q(description__icontains=search) | Q(skills__icontains=search)
        )
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    applied_job_ids = []
    if request.user.is_authenticated:
        applied_job_ids = list(
            Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)
        )

    return render(request, 'jobs/home.html', {
        'jobs': jobs,
        'search': search or '',
        'location': location or '',
        'job_type': job_type or '',
        'job_types': JobPost.JOB_TYPES,
        'applied_job_ids': applied_job_ids,
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role=form.cleaned_data['role'])
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'jobs/signup.html', {'form': form})


@login_required
def post_job(request):
    profile = getattr(request.user, 'profile', None)

    if not profile or profile.role != 'recruiter':
        messages.error(request, "Only recruiters can post jobs.")
        return redirect('home')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('home')
    else:
        form = JobPostForm()

    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def apply_job(request, job_id):
    job = JobPost.objects.get(id=job_id)
    profile = getattr(request.user, 'profile', None)

    if not profile or profile.role != 'seeker':
        messages.error(request, "Only job seekers can apply.")
        return redirect('home')

    already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    if already_applied:
        messages.error(request, "You've already applied to this job.")
        return redirect('home')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Application submitted!")
            return redirect('home')
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@login_required
def recruiter_dashboard(request):
    profile = getattr(request.user, 'profile', None)

    if not profile or profile.role != 'recruiter':
        messages.error(request, "Only recruiters can view this page.")
        return redirect('home')

    jobs = request.user.job_posts.all()
    total_applicants = Application.objects.filter(job__posted_by=request.user).count()
    today = timezone.now().date()

    return render(request, 'jobs/recruiter_dashboard.html', {
        'jobs': jobs,
        'total_applicants': total_applicants,
        'today': today,
    })


@login_required
def seeker_dashboard(request):
    profile = getattr(request.user, 'profile', None)

    if not profile or profile.role != 'seeker':
        messages.error(request, "Only job seekers can view this page.")
        return redirect('home')

    applications = request.user.applications.all()
    pending_count = applications.filter(status='pending').count()
    accepted_count = applications.filter(status='accepted').count()

    return render(request, 'jobs/seeker_dashboard.html', {
        'applications': applications,
        'pending_count': pending_count,
        'accepted_count': accepted_count,
    })