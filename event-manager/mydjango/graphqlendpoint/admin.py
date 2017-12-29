from django.contrib import admin

# Register your models here.
# Register your models here.

from graphqlendpoint.models import Agent, Agent_ot, Agent_unify,Event_ot, Call

admin.site.register(Call)
admin.site.register(Agent)
admin.site.register(Agent_ot)
admin.site.register(Event_ot)
admin.site.register(Agent_unify)
