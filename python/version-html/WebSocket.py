# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# HTTPServer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import sys
import os
from core import logger
from core import config
from threading import Thread
import WebSocketServer

MostrarInfo= None
ProcessRequest = None
data = open(os.path.join(config.get_runtime_path(),"version.xml"),"r").read()
version = data.split("<tag>")[1].split("</tag>")[0]
fecha = data.split("<date>")[1].split("</date>")[0]

class HandleWebSocket(WebSocketServer.WebSocket):
   def handleMessage(self):
      if self.data is None: self.data = ''
      if self.data:
        import json
        JSONData = json.loads(str(self.data))
        
      if "request" in JSONData:        
        sys.argv[JSONData["id"]]["request"]=JSONData["request"].encode("utf8")
        global ProcessRequest
        Thread(target=ProcessRequest,args=[JSONData["id"]], name=JSONData["id"] ).start()  
                 
      elif "data" in JSONData:
        if type(JSONData["data"]["result"]) == unicode:
          JSONData["data"]["result"]=JSONData["data"]["result"].encode("utf8")

        sys.argv[JSONData["id"]]["data"]=JSONData["data"]
 
      

   def handleConnected(self):
      import random
      ID = "%032x" %(random.getrandbits(128))
      sys.argv[ID]={"socket": self, "request":"", "data":"","host":""}
      self.sendMessage('{"action": "connect", "data":{"version": "pelisalacarta '+version+'", "date":"'+fecha+'"}, "id": "'+ ID +'"}')
      from platformcode import launcher
      Thread(target=launcher.start, name=ID ).start()  
      global MostrarInfo
      MostrarInfo()

   def handleClose(self):
    for ID in sys.argv:
      if sys.argv[ID]["socket"] == self:
        del sys.argv[ID]
        break
          
    global MostrarInfo
    MostrarInfo()



WebsocketPort=int(config.get_setting("websocket.port"))
server = WebSocketServer.SimpleWebSocketServer("",WebsocketPort,HandleWebSocket)

def start(Request, Info):
    global ProcessRequest
    global MostrarInfo
    ProcessRequest=Request
    MostrarInfo = Info
    Thread(target=server.serveforever).start()
 
def stop():
    server.close()
