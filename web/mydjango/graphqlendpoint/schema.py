import graphene
from graphene_django.types import DjangoObjectType


from .models import Call


class CallType(DjangoObjectType):
    class Meta:
        model = Call


class Query(graphene.ObjectType):
    calls = graphene.List(CallType)
    @graphene.resolve_only_args
    def resolve_calls(self):
        return Call.objects.all()


