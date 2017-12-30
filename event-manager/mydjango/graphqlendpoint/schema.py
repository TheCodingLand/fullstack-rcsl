import graphene
from graphene_django.types import DjangoObjectType


from .models import Call, Agent


class CallType(DjangoObjectType):
    class Meta:
        model = Call
        
        
class AgentType(DjangoObjectType):
    class Meta:
        model = Agent
        

class Querycalls(graphene.ObjectType):
    calls = graphene.List(CallType)
    @graphene.resolve_only_args
    def resolve_calls(self):
        return Call.objects.all()

class Queryagents(graphene.ObjectType):
    agents = graphene.List(AgentType)
    @graphene.resolve_only_args
    def resolve_agents(self):
        return Agent.objects.all()



