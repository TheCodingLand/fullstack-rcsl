from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Event(models.Model):

    timestamp = models.DateTimeField(null=False)
    
    




class Agent_ot(models.Model):

    userloginname = models.CharField(max_length=200, null=True)
    userdisplayname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    is_helpdesk = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    phone = models.CharField(max_length=200, null=True)
    ot_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, null=True, blank=True)
    state = models.CharField(max_length=200, default = "available", blank=True)
    
class Agent_unify(models.Model):
    login = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=False)
    ext = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, null = True, blank=True)
    state = models.CharField(max_length=200, default = "available", blank=True)
    agent_ot=models.OneToOneField(Agent_ot)

    
class Agent(models.Model):
    user=models.OneToOneField(User)
    agent_ot = models.OneToOneField(Agent_ot)
    agent_unify = models.OneToOneField(Agent_unify)
    avatar = models.ImageField(upload_to='userimage',blank=True)

class Event_ot(models.Model):
    CreationDate = models.DateTimeField(null=True)
    Eventtype=  models.CharField(max_length=200, null=True)
    ot_id = models.IntegerField(null=True)
    applicant = models.ForeignKey(Agent_ot)
    responsible = models.ForeignKey(Agent_ot)
    state = models.CharField(max_length=200, null=True)
    transferhistory = models.CharField(max_length=200, null=True)

class Call(models.Model):
    ucid = models.CharField(max_length=200, unique=True)
    state = models.CharField(max_length=200, null=True)
    origin = models.CharField(max_length=200, null=True)
    destination = models.CharField(max_length=200, null=True)
    call_type = models.CharField(max_length=200, null=True)
    start = models.DateTimeField(max_length=200, null=True)
    end = models.DateTimeField(max_length=200, null=True, blank=True)
    isContactCenterCall = models.BooleanField(default=False)
    history = models.CharField(max_length=600, null=True)
    primaryagent = models.ForeignKey(Agent, null=True, related_name='calls')
    secondaryagent = models.ForeignKey(Agent, null=True, related_name='calls')






