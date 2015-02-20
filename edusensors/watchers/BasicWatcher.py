#   -*- coding: utf-8 -*-
#   Basic

from service.BasicWatcherService import BasicWatcherService, IBasicWatcherService

from factory.BasicWatcherFactory import *
from protocol import *

from twisted.application import service, internet
from zope.interface import Interface, implements

from twisted.python import components
components.registerAdapter(BasicWatcherFactoryFromService,
                           IBasicWatcherService,
                           IBasicWatcherFactory)

name = 'Watcher 001(Basic)'
application = service.Application('basic watcher', uid=1, gid=1)
taService = BasicWatcherService(name)
internet.TCPServer(10501, IBasicWatcherFactory(taService)).setServiceParent(service.IServiceCollection(application))
