from django.contrib import admin
from .models import JobPost
from .models import Profile
from .models import Application

admin.site.register(JobPost)
admin.site.register(Profile)
admin.site.register(Application)