from django.contrib import admin

# Register your models here.
# Register your models here.

from graphqlendpoint.models import Agent,Event, Call, Transfer,LoggedInUser, ActiveCalls
        
class AgentAdmin(admin.ModelAdmin):

    list_display = ('ext', 'firstname', 'lastname', 'phone_login', 'phone_state')


class CallAdmin(admin.ModelAdmin):

    list_display = ('ucid', 'state', 'isContactCenterCall', 'history',
                    'end', 'origin')
    list_filter = ('end', 'state', 'primaryagent')


			


admin.site.register(Call, CallAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Event)
admin.site.register(Transfer)
admin.site.register(LoggedInUser)
admin.site.register(ActiveCalls)