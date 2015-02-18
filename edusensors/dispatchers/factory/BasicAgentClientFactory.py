#   -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from twisted.internet import protocol
from twisted.internet.defer import Deferred

from protocol.AgentRemoteControlProtocol import AgentRemoteControlProtocol

class IBasicAgentClientFactory(Interface):

    def doSomething(stuff):
        """Return a deferred returning a string"""

    def buildProtocol(addr):
        """Return a protocol returning a string"""

class BasicAgentClientFactory(protocol.ClientFactory):
    
    implements(IBasicAgentClientFactory)

    output = []
    commands = []
    #protocol = BasicAgentProtocol
    protocol = AgentRemoteControlProtocol
    
    def __init__(self, commands=[]):
        self.done = Deferred()
        self.commands = commands
        #self.done = 0

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('1111connection lost:', reason.getErrorMessage())
        #self.done = self.protocol.output
        self.done.callback(self.output)
        


