#   -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from twisted.internet import protocol

from protocol.WatcherControlProtocol import WatcherControlProtocol

class IBasicWatcherFactory(Interface):

    def doSomething(stuff):
        """Return a deferred returning a string"""

    def buildProtocol(addr):
        """Return a protocol returning a string"""

class BasicWatcherFactoryFromService(protocol.ClientFactory):
    
    implements(IBasicWatcherFactory)

    #protocol = BasicWatcherProtocol
    protocol = WatcherControlProtocol
    
    def __init__(self, service):
        self.service = service
        
    def doSomething(self, stuff):
        return self.service.my_func(stuff)
    
    def getName(self):
        return self.service.getName()
    
    def getUrlContent(self, url, callback):
        return self.service.getUrlContent(url, callback)
    


