# -*- coding: utf-8 -*-

from twisted.protocols.basic import LineReceiver
from twisted.internet import defer
#from factory.TestWatcherFactory import TestWatcherFactoryFromService

class WatcherControlProtocol(LineReceiver):
    
    
    request_count = 0

    def connectionMade(self):
        self.printMenu()
        self.transport.write('\r\n> ')
        
    def lineReceived(self, command):
        
        print "ACP: lineReceived:", command
        
        #print d + int(stuff)
        
        result = self.parseCommand(command)
        if result[1]:
            getattr(self, result[0])(result[1])
        else:
            getattr(self, result[0])()
        
        if result[0] != 'loseConnection':
            self.transport.write('\r\n> ')
        
        
    def parseCommand(self, command):
        '''
        Разбор команды: выделение функции и аргументов
        '''
        self.request_count += 1
        cmd = ''
        args = []
        for i,chunk in enumerate(command.split()):
            if i == 0:
                cmd = chunk.upper()
            else:
                args.append(chunk)
        
        if cmd.startswith('GET_PEER'):
            return ('getPeer', [])
        elif cmd.startswith('GET_NAME'):
            return ('getName', [])
        elif cmd.startswith('GET_NEWS'):
            return ('getNews', [])
        elif cmd.startswith('GET_HOST'):
            return ('getHost', [])
        elif cmd.startswith('CLOSE'):
            return ('loseConnection', [])    
        else:
            print 'MENU'
            return ('printMenu', [])
    
    def printMenu(self):
        menu = '''This EduSensors Watcher operates via WatcherControlProtocol
Commands available listed below:
    - CLOSE    -- close connection
    - GET_PEER -- print peer information
    - GET_HOST -- print host information
    - GET_NAME -- print name of this watcher
    - GET_NEWS -- print news from http://aspirantura.ifmo.ru/?page1=9
    - MENU     -- print this help'''
        self.writeMultiline(menu)
    
    def loseConnection(self):
        self.transport.write("Bye-Bye\r\n")
        self.transport.loseConnection()  
    
    def getPeer(self):
        addr = self.transport.getPeer()
        self.transport.write('Connection from %s:%d' % (addr.host, addr.port) )
    
    def getNews(self):
        self.transport.write('Breaking News: Busted!')
        def parseBody(body):
            self.transport.write(body.decode('cp1251').encode('utf-8'))
            self.transport.write('\r\n>')
            print body
        d = self.factory.getUrlContent('http://aspirantura.ifmo.ru/?page1=9', parseBody)
        #d.addCallback(parseBody)
        
    
    def getHost(self):
        addr = self.transport.getHost()
        self.transport.write('Server %s listening at %d port\r\n' % (addr.host, addr.port) )    
        self.transport.write('This request was #%d' % (self.request_count,) )    
    
    
    def getFile(self, filepath):
        import os
        if os.access(filepath, os.R_OK):
            self.transport.write('SUCCESS: %s FOUND\r\n' % filepath)
            f = os.open(filepath, os.O_RDONLY)
            self.setRawMode()
            chunk = os.read(f, 1)
            while chunk != '':
                #self.transport.write('Read something\r\n')
                self.transport.write(chunk)
                chunk = os.read(f, 1)
            os.close(f)
            self.setLineMode()
            self.transport.write('\r\n')
            self.transport.write('EDUSENSORS_STOP\r\n')
        else:
            self.transport.write('ERROR: No file or access with path %s\r\n' % filepath)
            
    def getName(self):
        self.transport.write(self.factory.getName())  
        
    
    def writeMultiline(self, multiline):
        lines = multiline.split('\r\n')
        for i,line in enumerate(lines):
            self.transport.write(line)
            if i < len(lines) - 1:
                self.transport.write('\r\n')
