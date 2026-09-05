from django.contrib import admin
from .models import JobPost
from .models import Profile

admin.site.register(JobPost)
admin.site.register(Profile)