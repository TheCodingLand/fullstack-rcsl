import graphene
from graphene_django.types import DjangoObjectType

from .models import Call


class CallType(DjangoObjectType):
    class Meta:
        model = Call
        


class Query(graphene.AbstractType):
    all_calls = graphene.List(CallType)
    call = graphene.Field(
        Call,
        id=graphene.Int(),
    )

    def resolve_all_calls(self, args, context, info):
        return Call.objects.all()

    def resolve_call(self, args, context, info):
        UCID = args.get('UCID')
        return Call.objects.get(UCID=UCID)
