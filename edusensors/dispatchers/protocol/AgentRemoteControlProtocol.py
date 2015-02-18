# -*- coding: utf-8 -*-

from twisted.protocols.basic import LineReceiver
from twisted.internet import defer
import re
#from factory.TestAgentFactory import TestAgentFactoryFromService

class AgentRemoteControlProtocol(LineReceiver):
    
    end = "Bye-Bye\r\n"
    output = []
    isLineMode = True
    rawOutput = []
    currentCommand = None

    def connectionMade(self):
        self.output = []
        for command in self.factory.commands:
            self.currentCommand = command
            if command.startswith('FILE'):
                self.isLineMode = False
            else:
                self.isLineMode = True
            self.sendLine(command)
        #self.sendLine("ROLL A")
        #self.sendLine("GET_PEER")
        #self.sendLine("GET_HOST")
        self.sendLine("CLOSE")


    def lineReceived(self, line):
        junkInBOL = re.compile('(^> )|(\r\n$)')
        line = junkInBOL.sub('', line)
        
        if self.currentCommand.startswith('FILE'):
            ignoreCurrentLine = False
            if line.startswith('SUCCESS'):
                print 'Transfer start'
                self.isLineMode = False
                self.rawOutput = []
                ignoreCurrentLine = True
            
            if line.startswith('ZIPPA'):
                print 'Transfer finish'
                self.isLineMode = True
                
                
            if self.isLineMode == False and ignoreCurrentLine == False:
                reason = ''
                if self.isLineMode == False:
                    reason = 'line mode OFF'
                else:
                    reason = 'ignore line OFF'
                print '[#%s#TO FILE:##] %s' % (reason, line,) 
                self.rawOutput.append(line)    
        else:
             self.output.append(line)
         
        
        
                
                
        #print("receive:", line)
    #def dataReceived(self, data):
    #    print 
        
    def rawDataReceived(self, line):
        import sys
        sys.exit()
        print 'RAW RAW RAW'
        self.output.append('RawData ++')        
    
    def connectionLost(self, reason=None):
        self.factory.output = self.output
        import os
        f = os.open('dump.tmp', os.O_WRONLY)
        for line in self.rawOutput:
            os.write(f, line)
        os.close(f)