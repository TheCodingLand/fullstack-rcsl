from django.contrib import admin

# Register your models here.
# Register your models here.

from graphqlendpoint.models import Agent,Event, Call, Transfer,LoggedInUser, ActiveCalls

admin.site.register(Call)
admin.site.register(Agent)
admin.site.register(Event)
admin.site.register(Transfer)
admin.site.register(LoggedInUser)
admin.site.register(ActiveCalls)