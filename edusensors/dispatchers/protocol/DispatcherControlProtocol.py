# -*- coding: utf-8 -*-

from twisted.protocols.basic import LineReceiver
from twisted.internet import defer,  reactor
from factory.BasicAgentClientFactory import BasicAgentClientFactory
from factory.BasicWatcherClientFactory import BasicWatcherClientFactory

#remote clients



class DispatcherControlProtocol(LineReceiver):
    
    state = {
    }
    
    # EduSensors Agents List
    agents = {'first': {'name': 'first', 'address': '127.0.0.1', 'port': '10001'}}
    # EduSensors Watchers List
    watchers = {'one': {'name': 'one', 'address': '127.0.0.1', 'port': '10501'}}
    
    request_count = 0

    def connectionMade(self):
        self.printMenu()
        self.transport.write('> ')
        
    def lineReceived(self, command):
        print "DCP: lineReceived:", command
        #print d + int(stuff)
        
        result = self.parseCommand(command)
        if result[1]:
            getattr(self, result[0])(*result[1])
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
        elif cmd.startswith('GET_WATCHERS'):
            return ('getWatchers', [])
        elif cmd.startswith('GET_AGENTS'):
            return ('getAgents', [])
        elif cmd.startswith('REG_WATCHER'):
            if len(args) > 3:
                new_args = []
                new_args.append(' '.join(args[:-2])) # name
                new_args.append(args[-2:-1][0]) # addr
                new_args.append(args[-1:][0]) # port
                args = new_args
            return ('registerWatcher', args)
        elif cmd.startswith('DEL_WATCHER'):
            args = [' '.join(args)]
            return ('removeWatcher', args)
        elif cmd.startswith('REG_AGENT'):
            if len(args) > 3:
                new_args = []
                new_args.append(' '.join(args[:-2])) # name
                new_args.append(args[-2:-1][0]) # addr
                new_args.append(args[-1:][0]) # port
                args = new_args
            return ('registerAgent', args)
        elif cmd.startswith('DEL_AGENT'):
            args = [' '.join(args)]
            return ('removeAgent', args)
        elif cmd.startswith('CALL_AGENT_METHOD'):
            return ('remoteCallAgentMethod', [' '.join(args)])
        elif cmd.startswith('CALL_WATCHER_METHOD'):
            return ('remoteCallWatcherMethod', [' '.join(args)])
        elif cmd.startswith('SQL'):
            return ('getDataset', [' '. join(args)])
        elif cmd.startswith('GET_HOST'):
            return ('getHost', [])
        elif cmd.startswith('CLOSE'):
            return ('loseConnection', [])    
        else:
            if not cmd.startswith('MENU'):
                self.transport.write('COMMAND "%s" NOT FOUND!\r\n' % (command,));
            return ('printMenu', [])
    
    def printMenu(self):
        '''
        writes menu with available commands into transport
        '''
        menu = '''
This EduSensors Dispatcher operates via DispatcherControlProtocol
Commands available listed below:
    - CLOSE    -- close connection
    - DEL_AGENT <name> -- remove agent
    - DEL_WATCHER <name> -- remove watcher
    - GET_AGENTS -- print list of agents 
    - GET_HOST -- print host information
    - GET_PEER -- print peer information
    - GET_WATCHERS -- print list of watchers
    - CALL_AGENT_METHOD <name> <cmd>-- print <agent>'s list of methods
    - CALL_WATCHER_METHOD <name> <cmd>-- print <watcher>'s list of methods
    - MENU     -- print this help
    - REG_AGENT <name> <ip> <port> -- register agent
    - REG_WATCHER <name> <ip> <port> -- register watcher
    
'''
        self.writeMultiline(menu)
    
    def loseConnection(self):
        self.transport.write("Bye-Bye\r\n")
        self.transport.loseConnection()  
    
    def getAgents(self):
        '''
        writes list of available EduSensors Agents into transport
        '''
        if len(self.agents) > 0:
            for i, agent in enumerate(self.agents.itervalues()):
                self.transport.write("%d - Agent \"%s\" listening at %s:%s\r\n" % ((i+1), agent['name'], agent['address'], agent['port']))
        else:
            self.transport.write("No agents assigned")
    
    def getWatchers(self):
        '''
        writes list of available EduSensors Watchers into transport 
        '''
        if len(self.watchers) > 0:
            for i, watcher in enumerate(self.watchers.itervalues()):
                self.transport.write("%d - Watcher \"%s\" listening at %s:%s\r\n" % ((i+1), watcher['name'], watcher['address'], watcher['port']))
        else:
            self.transport.write("No watchers assigned")
    
    def registerWatcher(self, name, address, port):
        '''
        add EduSensors Watcher into the corresponding list
        prints list of watchers after registration
        @param string: name - name of new watcher
        @param string: address - ip-address or domain name
        @param int: port - port for socket connection  
        '''
        watcher = { 'name': name, 'address' : address, 'port' : port }
        self.watchers[name] = watcher
        self.getWatchers()
    
    def removeWatcher(self, name):
        '''
        remove EduSensors Watcher from the corresponding list
        prints list of watchers after removing the watcher
        @param string: name - name of watcher to remove
        '''
        if name in self.watchers.keys():
            watcher = self.watchers[name]
            self.transport.write("Watcher \"%s\"[%s:%s] is unassigned \r\n" % (watcher['name'], watcher['address'], watcher['port']))
            del self.watchers[name]
    
    
    def registerAgent(self, name, address, port):
        '''
        add EduSensors Agent into the corresponding list
        prints list of agents after registration
        @param string: name - name of new agent
        @param string: address - ip-address or domain name
        @param int: port - port for socket connection  
        '''
        agent = { 'name': name, 'address' : address, 'port' : port }
        self.agents[name] = agent
        self.getAgents()
    
    def removeAgent(self, name):
        '''
        remove EduSensors Agent from the corresponding list
        prints list of agents after removing the agent
        @param string: name - name of agent to remove
        '''
        if name in self.agents.keys():
            agent = self.agents[name]
            self.transport.write("Agent \"%s\"[%s:%s] is unassigned \r\n" % (agent['name'], agent['address'], agent['port']))
            del self.agents[name]
            
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
    
    def remoteCallAgentMethod(self, command):
        def react_func(agent, command):
            f = BasicAgentClientFactory([command])
            reactor.connectTCP(agent['address'], int(agent['port']), f)                   
            return f.done
        
        def write_to_transport(output):
            for line in output[1:-1]:
                self.writeMultiline(line)
            self.transport.write('\r\n> ')
        
        name = ''
        for agent_name in self.agents.keys():
            if command.startswith(agent_name) and len(name) < len(agent_name):
                name = agent_name
        
        if name == '':
            self.transport.write("Agent \"%s\" not found in list\r\n" % (command,))
            return
        
        cmd = command.replace(name, '').strip()
        
        agent = self.agents[name]
        self.transport.write("Agent \"%s\"[%s:%s] found! Wait... \r\n" % (agent['name'], agent['address'], agent['port']))
        df = react_func(agent, cmd)
        df.addCallback(write_to_transport)
    
    '''
    def remoteCallWatcherMethod(self, command):
        name = ''
        for watcher_name in self.watchers.keys():
            if command.startswith(watcher_name) and len(name) < len(watcher_name):
                name = watcher_name
        
        if name == '':
            self.transport.write("Watcher \"%s\" not found in list\r\n" % (command,))
            return
        cmd = command.replace(name, '').strip()
        
        def cbResponse(response):
            print 'cbRESPONSE:', response
            pass
        
        def cbError(reason):
            print 'cbError', reason
            pass
        
        f = BasicWatcherClientFactory([command])
        reactor.connectTCP(watcher['address'], int(watcher['port']), f)
        
        for d in f.defers:
            d.addCallback(cbResponse)
            d.addErrback(cbError) 
        
        pass
    '''
    def remoteCallWatcherMethod(self, command):
        def react_func(watcher, command):
            f = BasicWatcherClientFactory([command])
            reactor.connectTCP(watcher['address'], int(watcher['port']), f)                   
            return f.done
        
        def write_to_transport(output):
            for line in output[1:-1]:
                self.writeMultiline(line)
            self.transport.write('\r\n> ')
        
        name = ''
        for watcher_name in self.watchers.keys():
            if command.startswith(watcher_name) and len(name) < len(watcher_name):
                name = watcher_name
        
        if name == '':
            self.transport.write("Watcher \"%s\" not found in list\r\n" % (command,))
            return
        
        cmd = command.replace(name, '').strip()
        
        watcher = self.watchers[name]
        self.transport.write("Watcher \"%s\"[%s:%s] found! Wait... \r\n" % (watcher['name'], watcher['address'], watcher['port']))
        df = react_func(watcher, cmd)
        df.addCallback(write_to_transport)        
        
    def writeMultiline(self, multiline):
        lines = multiline.split('\r\n')
        for line in lines:
            self.transport.write(line + '\r\n')