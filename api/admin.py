from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ['id', 'username', 'email', 'password', 'is_voted']
	list_display_links = ['id', 'username']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'count']
	list_display_links = ['id', 'name']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
	list_display = ['id', 'candidate', 'user', 'created_at', 'updated_at']
	list_display_links = ['id']
