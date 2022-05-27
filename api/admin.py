from django.contrib import admin
from api.models import *

admin.site.register(MyUser)
admin.site.register(Candidate)
admin.site.register(Vote)