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
            self.currentCommand = command.upper()
            if self.currentCommand.startswith('FILE'):
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
            
            if line.startswith('EDUSENSORS_STOP'):
                #print 'Transfer finish'
                self.isLineMode = True
                
            if self.isLineMode == False and ignoreCurrentLine == False:
                self.rawOutput.append(line)    
        else:
            self.output.append(line)
                
    def connectionLost(self, reason=None):
        self.factory.output = self.output
        import os
        
        path = '/tmp/dump.tmp'
        #if not os.path.exists(path):
        #    f = os.open(path, os.O_CREAT)
        #    os.close(f)
            
        os.remove(path)
        f = os.open(path, os.O_WRONLY | os.O_CREAT)
        for line in self.rawOutput:
            os.write(f, line)
        os.close(f)