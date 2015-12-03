from django.contrib import admin
from referendums.models import Vote, Referendum

# Register your models here.

admin.site.register(Vote)
admin.site.register(Referendum)
