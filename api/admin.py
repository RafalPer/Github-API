from django.contrib import admin
from api.models import Project, Commit

admin.site.register(Project)
admin.site.register(Commit)
