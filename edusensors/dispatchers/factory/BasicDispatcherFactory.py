#   -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from twisted.internet import protocol

from protocol.DispatcherControlProtocol import DispatcherControlProtocol

class IBasicDispatcherFactory(Interface):

    def doSomething(stuff):
        """Return a deferred returning a string"""

    def buildProtocol(addr):
        """Return a protocol returning a string"""

class BasicDispatcherFactoryFromService(protocol.ClientFactory):
    
    implements(IBasicDispatcherFactory)

    #protocol = BasicDispatcherProtocol
    protocol = DispatcherControlProtocol
    
    def __init__(self, service):
        self.service = service
        
    def doSomething(self, stuff):
        print "doSomething, OINK?", stuff
        return self.service.my_func(stuff)
    
    def query(self, sqlQuery):
        return self.service.query(sqlQuery)


