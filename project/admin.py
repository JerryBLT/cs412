from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Study)
admin.site.register(Participant)
admin.site.register(Enrollment)
admin.site.register(Visit)
admin.site.register(VisitDocument)
admin.site.register(UserProfile)