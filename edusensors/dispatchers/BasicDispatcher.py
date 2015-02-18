#   -*- coding: utf-8 -*-
#   Basic Dispatcher

#from twisted.application import service, internet
from service.BasicDispatcherService import BasicDispatcherService, IBasicDispatcherService

from factory.BasicDispatcherFactory import *
from protocol import *

from twisted.application import service, internet
from zope.interface import Interface, implements

from twisted.python import components
components.registerAdapter(BasicDispatcherFactoryFromService,
                           IBasicDispatcherService,
                           IBasicDispatcherFactory)


application = service.Application('basic dispatcher', uid=1, gid=1)
bdService = BasicDispatcherService()
internet.TCPServer(20000, IBasicDispatcherFactory(bdService)).setServiceParent(service.IServiceCollection(application))
