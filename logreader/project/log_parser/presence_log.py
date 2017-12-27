from project.models.agent_event import AgentEvent
from project.log_parser.log_line import LogLine


class PresenceLog(LogLine):
    def __init__(self,line):
        super(PresenceLog, self).__init__(line)
        
    def parse(self):
        self.linkedCall()
        self.changeACDState()
        self.changeDeviceState()
        
    def linkedCall(self):
        if self.getUcid():
            AgentEvent(self.getUserId(), self.date).linkCall(self.getUcid())
    
    def changeACDState(self):
        if self.getUserId() and self.getAcdState():
            AgentEvent(self.getUserId(), self.date).changeacdState(self.getAcdState())
    
    def changeDeviceState(self):
        if self.getUserId() and self.getLineState():
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
