#   -*- coding: utf-8 -*-
#   Basic

#import sys
#sys.path.append('.')
#from twisted.application import service, internet
from service.BasicAgentService import BasicAgentService, IBasicAgentService

from factory.BasicAgentFactory import *
from protocol import *



from twisted.application import service, internet
from zope.interface import Interface, implements

from twisted.python import components
components.registerAdapter(BasicAgentFactoryFromService,
                           IBasicAgentService,
                           IBasicAgentFactory)

name = 'agent 001(Basic)'
application = service.Application('basic agent', uid=1, gid=1)
taService = BasicAgentService(name)
internet.TCPServer(10001, IBasicAgentFactory(taService)).setServiceParent(service.IServiceCollection(application))
