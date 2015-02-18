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
        self.output.append(line)
        if self.currentCommand.startswith('FILE'):
            if line.startswith('SUCCESS'):
                print 'Transfer start'
                self.isLineMode = False
            else:
                self.rawOutput.append(line)    
            if line.startswith('TRANSFER COMPLETED'):
                print 'Transfer finish'
                self.isLineMode = True
                
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
        f = os.open('/home/knell/dump.dat', os.O_WRONLY)
        for line in self.rawOutput:
            os.write(f, line)
        os.close(f)