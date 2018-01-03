from project.models.agent_event import AgentEvent
from project.log_parser.log_line import LogLine


class PresenceLog(LogLine):
    def __init__(self,line):
        super(PresenceLog, self).__init__(line)
        
    def parse(self):
        if self.getUserId():            
            self.linkedCall()
            self.changeACDState()
            self.changeDeviceState()
            self.login()

    def login(self):
        if self.isLoginIn():
            AgentEvent(self.getUserId(), self.date).login(self.getExtension())
            
    def logoff(self):
        if self.isLoginOff():
            AgentEvent(self.getUserId(), self.date).logoff(self.getExtension()) 
            
    def linkedCall(self):
        if self.getUcid():
            AgentEvent(self.getUserId(), self.date).linkCall(self.getUcid())
    
    def changeACDState(self):
        if self.getAcdState():
            AgentEvent(self.getUserId(), self.date).changeacdState(self.getAcdState())
    
    def changeDeviceState(self):
        if self.getLineState():
            AgentEvent(self.getUserId(), self.date).changedevState(self.getLineState())
    
    def getUserId(self):
        return self.search(r"UserId\{(.*?)\}")
        
    def getExtension(self):
        return self.search(r"Extension\{(.*?)\}")
        
    def getAcdState(self):
        state = self.search(r"Acd State\{(.*?)\}")
        if state==False:
            state = self.search(r"TpsSUserPresence::OnEvent. Rcvd Agent (ACDAVAIL)")
        return state
        
    def getLineState(self):
        return self.search(r"State\{(.*?)\}\}\]\}")
        
    def getUcid(self):
        return self.search(r"HandlingState:\{ContactId/RqC\{(.*?)\/")

    def isLoginIn(self):
        return "Cause{Media Logon},Extension{" in self.line and "Presence State:{Active}" in self.line
    
    def isLoginOff(self):
        return ",Cause{Media Logoff},Extension{" in self.line and ",Presence State:{Logoff}" in self.line
# 1b70 TpsSUserPresence::SendEvent. UserMediaStateEvent:{ChangedMedia{Voice},UserId{107},Cause{Media Logon},Extension{534},MediaState:{Media{Voice},State{Logon},Cause{None},StartTime{2018/01/02 06:32:08.853}},Routing State:{State{Unavailable},Reason{0},Source{CTI Query}},Presence State:{Active},Presence State(ExDC):{Away},Affected Contact:{HandlingState{ContactId/RqC{4781514871127062/-1},State{Busy}}}}