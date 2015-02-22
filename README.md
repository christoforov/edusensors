# edusensors
EduSensors Public Repository

<b>EduSensors</b> is a system to make gathering information from different sources easier. The system should be capable to observe a local network of educational organization. The network is supposed
to consist of some informational systems located on independent servers. The target information to be gathered is decided by endpoint user. 

In other words, <b>EduSensors</b> is a system for Educational Data Mining. Lots of unprocessed information is stored on different servers and EDM-researchers should be able to select, gather and preprocess it.

Components of EduSensors:
<ul>
<li>EduSensors Agent</li>
<li>EduSensors Dispatcher</li>
<li>EduSensors Watcher (not implemented yet)</li>
<li>EduSensors Worker (not implemented yet)</li>
<li>EduSensors Backend (not implemented yet)</li>
</ul>

<h3>Agent</h3>

The Agent resides on server and works in background as system service. Default port is 10001.
Commands supported by the Agent:
<ul>
<li>MENU</li>
<li>GET_HOST</li>
<li>GET_PEER</li>
<li>GET_NAME</li>
<li>SQL</li>
<li>FILE</li>
<li>CLOSE</li>
</ul>

<h3>Dispatcher</h3>

The Dispatcher is listening to 20000 port and provides list of registred Agents and provides following functions:
<ul>
<li>MENU</li>
<li>GET_HOST</li>
<li>GET_PEER</li>
<li>REG_AGENT</li>
<li>REG_WATCHER</li>
<li>DEL_AGENT</li>
<li>DEL_WATCHER</li>
<li>GET_AGENTS</li>
<li>CALL_AGENT_METHOD</li>
<li>CALL_WATCHER_METHOD</li>
<li>CLOSE</li>
</ul>

<h3>Watcher</h3>

The Watcher is listening to 10501 port.
List of supported functions:
<ul>
<li>CLOSE</li>
<li>GET_PEER</li>
<li>GET_HOST</li>
<li>GET_NAME</li>
<li>GET_NEWS</li>
<li>MENU</li>
</ul>

<h3>How to install</h3>

Installation guide will come in a better day.
