#   -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from twisted.application import service
from twisted.internet import defer
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
from twisted.internet import reactor


class IBasicWatcherService(Interface):
    def my_func(self, value):
        """Return a deferred returning a string"""
    

class BasicWatcherService(service.Service):
    implements(IBasicWatcherService)
    
    headers = {'User-Agent:': ['EduSensors Web Client'],
                'Content-Type': ['text/html'],
                'Ninjasheader': ['Ninja stuff has nothing to do with STAR WARS!']
               }
    
    def __init__(self, name):
        self.name = name
        
    def getName(self):
        return self.name
    
    def my_func(self, value):
        print 'BasicWatcherService::my_func'
        return defer.Deferred()
    
    def getUrlContent(self, url, callback):
        print 'URL:', url
        agent = Agent(reactor)
        d = agent.request('GET',
                          url,
                          Headers(self.headers),
                          None
        )
        
        def cbReadBody(response):
            print 'Response version:', response.version
            print 'Response code:', response.code
            print 'Response phrase:', response.phrase
            defered = readBody(response)
            defered.addCallback(callback)
            
        
        d.addCallback(cbReadBody)
        return d