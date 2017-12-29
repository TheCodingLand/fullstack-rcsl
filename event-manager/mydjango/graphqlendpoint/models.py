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
    state = models.CharField(max_length=200, default = "available", blank=True)
    def __str__(self):
        return self.userloginname
    
class Agent_unify(models.Model):
    login = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=False)
    ext = models.CharField(max_length=200, null=True, unique=True)
    
    state = models.CharField(max_length=200, default = "available", blank=True)
    agent_ot=models.OneToOneField(Agent_ot,on_delete=models.DO_NOTHING, null=True, blank=True)
    def __str__(self):
        return self.login
    
class Agent(models.Model):
    user=models.OneToOneField(User, on_delete=models.DO_NOTHING)
    agent_ot = models.OneToOneField(Agent_ot,on_delete=models.DO_NOTHING)
    agent_unify = models.OneToOneField(Agent_unify,on_delete=models.DO_NOTHING)
    avatar = models.ImageField(upload_to='userimage',blank=True)
    def __str__(self):
        return self.user
        
class Event_ot(models.Model):
    CreationDate = models.DateTimeField(null=True)
    Eventtype=  models.CharField(max_length=200, null=True)
    ot_id = models.IntegerField(null=True)
    applicant = models.ForeignKey(Agent_ot, related_name='applicant', on_delete=models.CASCADE)
    responsible = models.ForeignKey(Agent_ot, related_name='responsible', on_delete=models.CASCADE)
    state = models.CharField(max_length=200, null=True)
    transferhistory = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.ot_id
    
class Call(models.Model):
    name = models.CharField(max_length=200)
    ucid = models.CharField(max_length=200, unique=True)
    state = models.CharField(max_length=200, null=True)
    origin = models.CharField(max_length=200, null=True)
    destination = models.CharField(max_length=200, null=True)
    call_type = models.CharField(max_length=200, null=True)
    start = models.DateTimeField(max_length=200, null=True)
    end = models.DateTimeField(max_length=200, null=True, blank=True)
    isContactCenterCall = models.BooleanField(default=False)
    history = models.CharField(max_length=600, null=True)
    primaryagent = models.ForeignKey(Agent_unify, null=True, related_name='calls', on_delete=models.DO_NOTHING)
    secondaryagent = models.ForeignKey(Agent_unify, null=True, related_name='calls_alt', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.ucid
        
    def getTransfers(self):
        tf = Transfer.objects.filter(call=self).order_by('timestamp')
        return tf
    
    def updatehistory(self):
        self.history = ""
        for t in self.getTransfers():
            if t.origin =="":
                #first transfer
                self.history == t.destination
            else:
                #other transfers
                self.history = "%s -> %s" % (self.history, t.destination)
        self.save()


class Transfer(models.Model):
    origin = models.CharField(max_length=200, null=True)
    destination = models.CharField(max_length=200)
    timestamp = models.DateTimeField(max_length=200)
    call = models.ForeignKey(Call, on_delete=models.CASCADE )
    def __str__(self):
        return "%s - %" % (self.call, self.destination)

