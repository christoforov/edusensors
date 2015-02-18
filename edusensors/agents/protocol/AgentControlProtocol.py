# -*- coding: utf-8 -*-

from twisted.protocols.basic import LineReceiver
from twisted.internet import defer
#from factory.TestAgentFactory import TestAgentFactoryFromService

class AgentControlProtocol(LineReceiver):
    
    
    request_count = 0

    def connectionMade(self):
        self.printMenu()
        self.transport.write('> ')
        
    def lineReceived(self, command):
        
        print "ACP: lineReceived:", command
        
        #print d + int(stuff)
        
        result = self.parseCommand(command)
        if result[1]:
            getattr(self, result[0])(result[1])
        else:
            getattr(self, result[0])()
        
        if result[0] != 'loseConnection':
            self.transport.write('> ')
        
        '''
        d = self.factory.doSomething(command)
        def catchError():
            return 'Error occured'
        d.addErrback(catchError)
        
        def react(value):
            print 'REACT'
            result = self.parseCommand(command)
            if result[1]:
                getattr(self, result[0])(result[1])
            else:
                getattr(self, result[0])()
        d.addCallback(react)
        '''
        
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
        elif cmd.startswith('SQL'):
            return ('getDataset', [' '. join(args)])
        elif cmd.startswith('FILE') and len(args) == 1:
            return ('getFile', args[0])
        elif cmd.startswith('GET_HOST'):
            return ('getHost', [])
        elif cmd.startswith('CLOSE'):
            return ('loseConnection', [])    
        else:
            print 'MENU'
            return ('printMenu', [])
    
    def printMenu(self):
        menu = '''
This EduSensors Agent operates via AgentControlProtocol
Commands available listed below:
    - CLOSE    -- close connection
    - FILE     -- download file
    - GET_PEER -- print peer information
    - GET_HOST -- print host information
    - GET_NAME -- print name of this agent
    - MENU     -- print this help
    - SQL      -- run SQL-query
'''
        self.writeMultiline(menu)
    
    def loseConnection(self):
        self.transport.write("Bye-Bye\r\n")
        self.transport.loseConnection()  
    
    def getPeer(self):
        addr = self.transport.getPeer()
        self.transport.write('Connection from %s:%d\r\n' % (addr.host, addr.port) )
    
    def getHost(self):
        addr = self.transport.getHost()
        self.transport.write('Server %s listening at %d port\r\n' % (addr.host, addr.port) )    
        self.transport.write('This request was #%d\r\n' % (self.request_count,) )    
    
    def getDataset(self, args):
        sqlQuery = args[0]
        dataset = self.factory.query(sqlQuery)    
        import json
        result = json.dumps(dataset)
        self.transport.write(result + '\r\n')
    
    def getFile(self, filepath):
        import os
        if os.access(filepath, os.R_OK):
            self.transport.write('SUCCESS: %s FOUND\r\n' % filepath)
            f = os.open(filepath, os.O_RDONLY)
            self.setRawMode()
            chunk = os.read(f, 1024)
            while chunk != '':
                #self.transport.write('Read something\r\n')
                self.transport.write(chunk)
                chunk = os.read(f, 1024)
            os.close(f)
            self.setLineMode()
            self.transport.write('TRANSFER COMPLETED\r\n')
        else:
            self.transport.write('ERROR: No file or access with path %s\r\n' % filepath)
            
    def getName(self):
        self.transport.write(self.factory.getName() + '\r\n')  
        
    
    def writeMultiline(self, multiline):
        lines = multiline.split('\r\n')
        for line in lines:
            self.transport.write(line + '\r\n')