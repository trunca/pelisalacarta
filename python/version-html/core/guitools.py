# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de vídeos descargados
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys
import config
import logger
from core import config
from core.item import Item
 

class DialogoProgreso(object):
  Progreso=""
  Titulo=""
  Closed=False
  def __init__(self, Progreso, Titulo):
    self.Progreso = Progreso
    self.Titulo = Titulo
    self.Closed = False
  def IsCanceled(self):
    from platformcode import cliente
    return self.Progreso.ProgresoIsCanceled()
  
  def Actualizar(self,Porcentaje, Texto):
    from platformcode import cliente
    self.Progreso.ProgresoActualizar(self.Titulo,Texto,Porcentaje)
  
  def Cerrar(self):
    from platformcode import cliente
    self.Progreso.ProgresoCerrar()

class DialogoProgresoBG(object):
  Progreso=""
  Titulo=""
  def __init__(self, Progreso, Titulo):
    self.Progreso = Progreso
    self.Titulo = Titulo
  def IsCanceled(self):
    return False
  
  def Actualizar(self,Porcentaje, Texto):
    from platformcode import cliente
    self.Progreso.ProgresoBGActualizar(self.Titulo,Texto,Porcentaje)
  
  def Cerrar(self):
    from platformcode import cliente
    self.Progreso.ProgresoBGCerrar()


def isPlaying():
    from platformcode import cliente
    return cliente.Acciones().isPlaying()
    
    
def Dialog_Progress(title, Texto):
    from platformcode import cliente
    progreso = cliente.Dialogo().ProgresoAbrir(title,Texto,0)
    Progreso = DialogoProgreso(progreso,title)
    return Progreso
    
def Dialog_ProgressBG(title, Texto):
    from platformcode import cliente
    progreso = cliente.Dialogo().ProgresoBGAbrir(title,Texto,0)
    Progreso = DialogoProgresoBG(progreso,title)
    return Progreso


def Dialog_OK(title, text):
    from platformcode import cliente
    cliente.Dialogo().MostrarOK(title,text)

def Dialog_YesNo(title, text):
    from platformcode import cliente
    return cliente.Dialogo().MostrarSiNo(title,text)
    
def Dialog_Select(title, opciones):
    from platformcode import cliente
    resultado = cliente.Dialogo().Select(title,opciones)
    if resultado ==-1: resultado = None
    return resultado

def AddItem(item, titulo, thumbnail, mode): #----------------------------------OK
#Añade información adicional al title.  
    contextCommands=[]   
    for menuitem in item.context:
        if not "title" in menuitem or not "action" in menuitem or not "channel" in menuitem:
          continue
        if menuitem["channel"]=="": menuitem["channel"] = item.channel 
        
        Menu = item.clone()
        Menu.action = menuitem["action"]
        Menu.channel = menuitem["channel"]
        Menu.refered_action = item.action
        contextCommands.append([menuitem["title"],ConstruirURL(Menu)])
    from platformcode import cliente
    cliente.Acciones().AddItem(titulo,thumbnail,item.fanart,item.plot, item.tourl(),contextCommands, mode, item.action)
      

def CloseDirectory(refereditem): #----------------------------------OK
    from platformcode import cliente
    cliente.Acciones().EndItems()
    
    
    
def Refresh(): #----------------------------------OK
    from platformcode import cliente
    cliente.Acciones().Refrescar()
    
def Keyboard(Texto, Title="", Password=False): #----------------------------------OK
    from platformcode import cliente  
    retorno = cliente.Dialogo().MostrarTeclado(Texto, Title, Password) 
    if retorno <>"-1": 
      return retorno
    else:
      return None
    
    
    
def play(item, ItemVideo):
    if not ItemVideo == None:
      from platformcode import cliente  
      url = ItemVideo.url[1]
      cliente.Acciones().Play(item.title, item.plot, url, item.url)
          
def Update(item):
    from platformcode import cliente  
    cliente.Acciones().Update(ConstruirURL(item))

def UpdateLibrary(item):
    pass
    
def ConstruirURL(item):
    return "?" + item.tourl()
    
def ConstruirStrm(item):
    return "?" + item.tourl()
