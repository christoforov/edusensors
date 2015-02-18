#   -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from twisted.internet import protocol

from protocol.AgentControlProtocol import AgentControlProtocol

class IBasicAgentFactory(Interface):

    def doSomething(stuff):
        """Return a deferred returning a string"""

    def buildProtocol(addr):
        """Return a protocol returning a string"""

class BasicAgentFactoryFromService(protocol.ClientFactory):
    
    implements(IBasicAgentFactory)

    #protocol = BasicAgentProtocol
    protocol = AgentControlProtocol
    
    def __init__(self, service):
        self.service = service
        
    def doSomething(self, stuff):
        print "doSomething, OINK?", stuff
        return self.service.my_func(stuff)
    
    def getName(self):
        return self.service.getName()
    
    def query(self, sqlQuery):
        return self.service.query(sqlQuery)


