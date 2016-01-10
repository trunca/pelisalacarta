# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Módulo para acciones en el cliente HTML
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import sys, os
import json

import threading
import urllib
import base64
from core.config import get_localized_string

ItemList = []

def getThread():
  return threading.current_thread().name
  
def SendMessage(Data):
  import random
  ID = "%032x" %(random.getrandbits(128))
  Data["id"] = ID
  try:
    sys.argv[getThread()]["socket"].sendMessage(json.dumps(Data))
    return ID
  except:
    pass

def GetData(ID):
  try:
    if sys.argv[getThread()]["data"]["id"] == ID:
      data = sys.argv[getThread()]["data"]["result"]
    else:
      data = None
  except:
    data = ""
  return data
  
def GetHost():
  try:
    data = sys.argv[getThread()]["host"]
  except:
    data = ""
  return data
  
class Dialogo(object):
  def ProgresoBGAbrir(self,Titulo="",Mensaje="", Porcentaje=0):
    JsonData = {}
    JsonData["action"]="ProgressBG" 
    JsonData["data"]={}
    JsonData["data"]["title"]=Titulo
    JsonData["data"]["text"]=Mensaje
    JsonData["data"]["percent"]=Porcentaje
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue
      
    return self
    
  def ProgresoBGActualizar(self,Titulo="",Mensaje="",Porcentaje=0):
    JsonData = {}
    JsonData["action"]="ProgressBGUpdate" 
    JsonData["data"]={}
    JsonData["data"]["title"]=Titulo
    JsonData["data"]["text"]=Mensaje
    JsonData["data"]["percent"]=Porcentaje
    SendMessage(JsonData)
          
  def ProgresoBGCerrar(self):
    JsonData = {}
    JsonData["action"]="ProgressBGClose" 
    JsonData["data"]={}
    SendMessage(JsonData)

  def ProgresoAbrir(self,Titulo="",Mensaje="", Porcentaje=0):
    JsonData = {}
    JsonData["action"]="Progress" 
    JsonData["data"]={}
    JsonData["data"]["title"]=Titulo
    JsonData["data"]["text"]=Mensaje
    JsonData["data"]["percent"]=Porcentaje
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue

    return self
    
  def ProgresoActualizar(self,Titulo="",Mensaje="",Porcentaje=0):
    JsonData = {}
    JsonData["action"]="ProgressUpdate" 
    JsonData["data"]={}
    JsonData["data"]["title"]=Titulo
    JsonData["data"]["text"]=Mensaje
    JsonData["data"]["percent"]=Porcentaje
    SendMessage(JsonData)
      
  def ProgresoIsCanceled(self):
    JsonData = {}
    JsonData["action"]="ProgressIsCanceled" 
    JsonData["data"]={}
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue
      
    return GetData(ID)

  def ProgresoCerrar(self):
    JsonData = {}
    JsonData["action"]="ProgressClose" 
    JsonData["data"]={}
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue

  def MostrarOK(self,Titulo="",Mensaje=""):
    JsonData = {}
    JsonData["action"]="Alert" 
    JsonData["data"]={}
    JsonData["data"]["title"]=Titulo
    JsonData["data"]["text"]=unicode(Mensaje ,"utf8","ignore").encode("utf8")
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue
    
  def MostrarSiNo(self,Titulo="",Mensaje=""):
    JsonData = {}
    JsonData["action"]="AlertYesNo" 
    JsonData["data"]={}
    JsonData["data"]["title"]=Titulo
    JsonData["data"]["text"]=unicode(Mensaje ,"utf8","ignore").encode("utf8")
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue

    return GetData(ID)

    
  def MostrarTeclado(self,Texto="",Titulo="", Password=False):
    JsonData = {}
    JsonData["action"]="Keyboard" 
    JsonData["data"]={}
    JsonData["data"]["title"]=Titulo
    JsonData["data"]["text"]=Texto
    JsonData["data"]["password"]=Password
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue
    return GetData(ID)

  def Select(self,Titulo,Elementos=[]):
    JsonData = {}
    JsonData["action"]="List"
    JsonData["data"]={}
    JsonData["data"]["title"]=Titulo
    JsonData["data"]["list"]=[]
    for Elemento in Elementos:
      JsonData["data"]["list"].append(Elemento)
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue
    return GetData(ID)


class Acciones(object):

  def Refrescar(self,Scroll=False):
    JsonData = {}
    JsonData["action"]="Refresh" 
    JsonData["data"]={}
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue
    
  def AddItem(self,Title="",Thumbnail="", Fanart="", Plot="",Url="",ContextMenu=[], Action=""):
    global ItemList
    JsonItem = {}
    JsonItem["title"]=Title
    JsonItem["thumbnail"]= Thumbnail
    JsonItem["fanart"]=Fanart
    JsonItem["plot"]=Plot
    JsonItem["action"]=Action
    JsonItem["url"]=Url
    JsonItem["context"]=[]
    for Comando in ContextMenu:
      JsonItem["context"].append({"title":Comando[0],"url": Comando[1]})
    ItemList.append(JsonItem)


  def EndItems(self, Mode=0):
    global ItemList
    JsonData = {}
    JsonData["action"]="EndItems"
    JsonData["data"]={}
    JsonData["data"]["itemlist"]=ItemList
    JsonData["data"]["mode"]=Mode   
    JsonData["data"]["host"]=GetHost()   
    ID = SendMessage(JsonData)
    ItemList= []
    while GetData(ID) == None:
      continue

    
  def Play(self,Title="",Plot="",Url="", ServerURL=""):
    JsonData = {}
    JsonData["action"]="Play" 
    JsonData["data"]={}
    JsonData["data"]["title"]= Title
    JsonData["data"]["plot"]= Plot
    JsonData["data"]["video_url"] =  Url
    JsonData["data"]["url"] =  ServerURL
    JsonData["data"]["host"] =  GetHost()
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue

  def AbrirConfig(self,items):
    from core import config
    JsonData = {}
    JsonData["action"]="OpenConfig"   
    JsonData["data"]={}
    JsonData["data"]["items"]=[]
    
    for item in items:
      for key in item:
        if key in ["lvalues", "label", "category"]:
          try:
            ops = item[key].split("|")
            for x, op in enumerate(ops):
              ops[x] = get_localized_string(int(ops[x])) 
            item[key] = "|".join(ops)
          except:
            pass

      JsonData["data"]["items"].append(item)
    ID = SendMessage(JsonData)

    while GetData(ID) == None:
      pass
      
    if GetData(ID):
      from core import config
      config.set_settings(GetData(ID))
      JsonData = {}
    JsonData["action"]="HideLoading"
    JsonData["data"] = {}
    SendMessage(JsonData)
      
   
 
  def Update(self,url):
    JsonData = {}
    JsonData["action"]="Update" 
    JsonData["data"]={}
    JsonData["data"]["url"]=url
    ID = SendMessage(JsonData)

    while GetData(ID) == None:
      continue

    
  def isPlaying(self):
    JsonData = {}
    JsonData["action"]="isPlaying" 
    JsonData["data"]={}
    ID = SendMessage(JsonData)
    while GetData(ID) == None:
      continue
    return GetData(ID)

  
    