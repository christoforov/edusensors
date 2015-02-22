#   -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from twisted.internet import protocol
from twisted.internet.defer import Deferred

from protocol.WatcherRemoteControlProtocol import WatcherRemoteControlProtocol

class IBasicWatcherClientFactory(Interface):

    def doSomething(stuff):
        """Return a deferred returning a string"""

    def buildProtocol(addr):
        """Return a protocol returning a string"""

class BasicWatcherClientFactory(protocol.ClientFactory):
    
    implements(IBasicWatcherClientFactory)

    output = []
    commands = []
    #protocol = BasicWatcherProtocol
    protocol = WatcherRemoteControlProtocol
    
    def __init__(self, commands=[]):
        self.done = Deferred()
        self.commands = commands
        #self.done = 0

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        #self.done = self.protocol.output
        self.done.callback(self.output)
        


