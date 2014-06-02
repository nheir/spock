from spock.client import Client
from spock.plugins import DefaultPlugins
from demoplugin import DemoPlugin
#Open login.py and put in your username and password
from login import username, password
from spock.plugins.helpers.clientinfo import ClientInfoPlugin
from spock.plugins.helpers.move import MovementPlugin

settings = {
    'username': "Bot",
    'authenticated': False, #Authenticate with authserver.mojang.com
    'bufsize': 4096,       #Size of socket buffer
    'sock_quit': True,     #Stop bot on socket error or hangup
    'sess_quit': True,     #Stop bot on failed session login
    'thread_workers': 5,   #Number of workers in the thread pool
    'packet_trace': True,
    'plugins': DefaultPlugins,         #Plugins
    'plugin_settings': {}, #Extra settings for plugins
}

plugins = DefaultPlugins
plugins.append(ClientInfoPlugin)
plugins.append(MovementPlugin)
# plugins.append(DemoPlugin)

client = Client(plugins = plugins, settings = settings)
client.start(host="192.168.2.19", port=25565)