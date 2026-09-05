from django.shortcuts import render
from .models import JobPost
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import JobPost

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'location', 'job_type', 'salary', 'skills', 'deadline']

def home(request):
    jobs = JobPost.objects.all()
    return render(request, 'jobs/home.html', {'jobs': jobs})

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

