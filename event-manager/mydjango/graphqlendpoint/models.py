from django.db import models
from django.contrib.auth.models import User
# Create your models here.


    
class Agent(models.Model):
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=False)
    ot_userloginname = models.CharField(max_length=200, null=True)
    ot_userdisplayname = models.CharField(max_length=200, null=True, blank=True)
    ot_id = models.CharField(max_length=200,null=True)
    user=models.OneToOneField(User, on_delete=models.DO_NOTHING)
    phone_login = models.CharField(max_length=200, null=True)
    phone_active = models.BooleanField(default=False)
    ext = models.CharField(max_length=200, null=True, unique=True)
    phone_state = models.CharField(max_length=200, default = "available", blank=True)
    avatar = models.ImageField(upload_to='userimage',blank=True)
    def __str__(self):
        return "%s" % firstname
        
        
class Event(models.Model):
    creationdate = models.DateTimeField(null=True)
    end=models.DateTimeField(null=True)
    ot_id = models.IntegerField(null=True)
    applicant = models.ForeignKey(Agent, related_name='events_applicant', on_delete=models.CASCADE, null=True)
    responsible = models.ForeignKey(Agent, related_name='events_responsible', on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=200, null=True)
    transferhistory = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
   
    def __str__(self):
        return  "%s" % self.ot_id


class Category(models.Model):
    title = models.CharField(max_length=200, null=True)
    predecessor = models.IntegerField(null=True, blank=True)
    searchcode = models.CharField(max_length=200, null=True)
    ot_id = models.CharField(max_length=200, null=True)
    
    def create_from_json(self,data):
        self.title = data.get("Title")
        self.searchcode = data.get("SearchCode")
        self.ot_id = data.get("id")
    
    def __str__(self):
        return "%s" % self.title

class Ticket(models.Model):
    creationdate = models.DateTimeField(null=True)
    title=models.DateTimeField(null=True)
    category =models.ForeignKey(Category, related_name='tickets', on_delete=models.DO_NOTHING, null=True)
    applicant = models.ForeignKey(Agent, related_name='tickets_created', on_delete=models.CASCADE, null=True)
    responsible = models.ForeignKey(Agent, related_name='tickets_responsible', on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=200, null=True)
    solution = models.CharField(max_length=200, null=True)
    ot_id = models.CharField(max_length=200, null=True)
   
    def __str__(self):
        return "%s" % self.title
    
    
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
    primaryagent = models.ForeignKey(Agent, null=True, related_name='calls', on_delete=models.DO_NOTHING)
    secondaryagent = models.ForeignKey(Agent, null=True, related_name='calls_alt', on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, null=True, related_name='calls_alt', on_delete=models.DO_NOTHING)
    def __str__(self):
        return "%s" % self.ucid
        
    def getTransfers(self):
        tf = Transfer.objects.filter(call=self).order_by('timestamp')
        return tf
    
    def updatehistory(self):
        self.history = ""
        for t in self.getTransfers():
            if t.origin =="" and t.origin:
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
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
 
