from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ManagerOrDeveloperCreationForm, ManagerOrDeveloperChangeForm
from .models import ManagerOrDeveloper
# Register your models here.

admin.site.register(Project)
admin.site.register(Developer)
admin.site.register(Manager)
admin.site.register(Sprint_Backlog)
admin.site.register(PBI)
admin.site.register(Task)

class ManagerOrDeveloperAdmin(UserAdmin):
    add_form = ManagerOrDeveloperCreationForm
    form = ManagerOrDeveloperChangeForm
    model = ManagerOrDeveloper
    list_display = ['post', 'name', 'email', 'username',]

admin.site.register(ManagerOrDeveloper, ManagerOrDeveloperAdmin)