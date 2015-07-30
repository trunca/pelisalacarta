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
from core import platform_name
from core.item import Item
PLATFORM_NAME = platform_name.PLATFORM_NAME


 
def ExtraerItem():
  if "xbmc" in PLATFORM_NAME:
    itemserializado = sys.argv[2].replace("?","")
  elif "mediaserver" in PLATFORM_NAME:
    import threading
    itemserializado = sys.argv[sys.argv[threading.current_thread().name]["Socket"]]["Request"]

  item = Item()
  if itemserializado:
    item.deserialize(itemserializado)
  else:
    item = Item(channel="channelselector", action="getmainlist")
  return item



class DialogoProgreso(object):
  Progreso=""
  Titulo=""
  Closed=False
  def __init__(self, Progreso, Titulo):
    self.Progreso = Progreso
    self.Titulo = Titulo
    self.Closed = False
  def IsCanceled(self):
      if "xbmc" in PLATFORM_NAME:
        return (self.Progreso.iscanceled() or self.Closed)
      
      elif "mediaserver" in PLATFORM_NAME:
        from platformcode.mediaserver import cliente
        return self.Progreso.ProgresoIsCanceled()
  
  def Actualizar(self,Porcentaje, Texto):
      if "xbmc" in PLATFORM_NAME:
        import xbmcgui
        Linea1=" "
        Linea2=" "
        Linea3=" "
        if len(Texto.split("\n"))>0:
          Linea1= Texto.split("\n")[0]
        if len(Texto.split("\n"))>1:
          Linea2= Texto.split("\n")[1]
        if len(Texto.split("\n"))>2:
          Linea3= Texto.split("\n")[2]
        self.Progreso.update(Porcentaje,Linea1,Linea2,Linea3)
      
      elif "mediaserver" in PLATFORM_NAME:
        from platformcode.mediaserver import cliente
        self.Progreso.ProgresoActualizar(self.Titulo,Texto,Porcentaje)
  
  def Cerrar(self):
      if "xbmc" in PLATFORM_NAME:
        import xbmcgui
        self.Progreso.close()
        self.Closed = True
      
      elif "mediaserver" in PLATFORM_NAME:
        from platformcode.mediaserver import cliente
        self.Progreso.ProgresoCerrar()


def isPlaying():
  if "xbmc" in PLATFORM_NAME:
    import xbmc
    return xbmc.Player().isPlaying()
  elif "mediaserver" in PLATFORM_NAME:
    from platformcode.mediaserver import cliente
    return cliente.Acciones().isPlaying()
    
    
def Dialog_Progress(title, Texto):
  if "xbmc" in PLATFORM_NAME:
    import xbmcgui
    progreso = xbmcgui.DialogProgress()
    progreso.create(title , Texto)
    Progreso = DialogoProgreso(progreso,title)
    return Progreso
  
  elif "mediaserver" in PLATFORM_NAME:
    from platformcode.mediaserver import cliente
    progreso = cliente.Dialogo().ProgresoAbrir(title,Texto,0)
    Progreso = DialogoProgreso(progreso,title)
    return Progreso
    



def Dialog_OK(title, text):

  if "xbmc" in PLATFORM_NAME:
    import xbmcgui
    xbmcgui.Dialog().ok(title,text)
 
  elif "mediaserver" in PLATFORM_NAME:
    from platformcode.mediaserver import cliente
    cliente.Dialogo().MostrarOK(title,text)

def Dialog_YesNo(title, text):

  if "xbmc" in PLATFORM_NAME:
    import xbmcgui
    return xbmcgui.Dialog().yesno(title,text)
 
  elif "mediaserver" in PLATFORM_NAME:
    from platformcode.mediaserver import cliente
    return cliente.Dialogo().MostrarSiNo(title,text)
    
def Dialog_Select(title, opciones): #----------------------------------OK

  if "xbmc" in PLATFORM_NAME:
    import xbmcgui
    resultado = xbmcgui.Dialog().select(title, opciones)
    if resultado ==-1: resultado = None
    return resultado
  
  elif "mediaserver" in PLATFORM_NAME:
    from platformcode.mediaserver import cliente
    resultado = cliente.Dialogo().Select(title,opciones)
    if resultado ==-1: resultado = None
    return resultado

def AddItem(item, totalitems=0): #----------------------------------OK
    #Añade información adicional al title.
    item.title = unicode(item.title,"utf-8","ignore").encode("utf8")
    item.fulltitle = unicode(item.fulltitle,"utf-8","ignore").encode("utf8")
    item.plot = unicode(item.plot,"utf-8","ignore").encode("utf8")
    titulo = item.title
    
    import time   
    if item.duration:
      if item.duration > 3599: 
        Tiempo = time.strftime("%H:%M:%S", time.gmtime(item.duration))
      else:
        Tiempo= time.strftime("%M:%S", time.gmtime(item.duration))
    if item.action <> "mainlist":
      if config.get_setting("duracionentitulo")=="true" and item.duration: titulo = titulo + " [COLOR gold](" + Tiempo + ")[/COLOR]" 
      if config.get_setting("calidadentitulo")=="true" and item.quality: titulo = titulo + " [COLOR orange][" + item.quality + "][/COLOR]"   
      if config.get_setting("idiomaentitulo")=="true" and item.language: titulo = titulo + " [COLOR green][" + item.language + "][/COLOR]"
      
    #Si el item tiene fulltitle este manda sobre lo anterior, se mostrara este. 
    if item.fulltitle:
      titulo=item.fulltitle
      
    contextCommands=[]   
    if "," in item.context:
      for menuitem in item.context.split("|"):
        if "," in menuitem:
          from copy import deepcopy
          Menu = deepcopy(item)
          if len(menuitem.split(",")) == 2:
            Titulo = menuitem.split(",")[0]
            Menu.action = menuitem.split(",")[1]
          elif len(menuitem.split(",")) == 3:
            Titulo = menuitem.split(",")[0]
            Menu.channel = menuitem.split(",")[1]
            Menu.action =menuitem.split(",")[2]
          Menu.refered_action = item.action
          contextCommands.append([Titulo,ConstruirURL(Menu)])
          
    if "xbmc" in PLATFORM_NAME:
      import xbmcgui
      import xbmcplugin
      listitem = xbmcgui.ListItem( titulo, iconImage="DefaultFolder.png", thumbnailImage=item.thumbnail)
      listitem.setInfo( "video", { "Title" : item.title, "Plot" : item.plot, "Studio" : item.channel} )
      if item.fanart!="":
        listitem.setProperty('fanart_image',item.fanart) 
        xbmcplugin.setPluginFanart(int(sys.argv[1]), item.fanart)
      listitem.addContextMenuItems (contextCommands, replaceItems=False)
      
      if item.folder:
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = sys.argv[ 0 ] + "?" + item.serialize() , listitem=listitem, isFolder=True, totalItems=totalitems)
      else:
        if config.get_setting("player_mode")=="1": # SetResolvedUrl debe ser siempre "isPlayable = true"
          listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = sys.argv[ 0 ] + "?" + item.serialize() , listitem=listitem, isFolder=False, totalItems=totalitems)

    elif "mediaserver" in PLATFORM_NAME:
      from platformcode.mediaserver import cliente
      if item.thumbnail =="":
        if item.folder:
            item.thumbnail = "http://pelisalacarta.mimediacenter.info/squares/folder.png"
        else:
            item.thumbnail = "http://pelisalacarta.mimediacenter.info/squares/file.png"
      import urllib
      import base64
      cliente.Acciones().AddItem(titulo,item.thumbnail,item.fanart,item.plot, item.serialize(),contextCommands )
      

def CloseDirectory(refereditem): #----------------------------------OK

  if "xbmc" in PLATFORM_NAME:
    import xbmc
    import xbmcplugin
    xbmcplugin.endOfDirectory( handle=int(sys.argv[1]), succeeded=True )
    if config.get_setting("forceview")=="true":
      if refereditem.viewmode=="list":
          xbmc.executebuiltin("Container.SetViewMode(50)")
      elif refereditem.viewmode=="movie_with_plot":
          xbmc.executebuiltin("Container.SetViewMode(503)")
      elif refereditem.viewmode=="movie":
          xbmc.executebuiltin("Container.SetViewMode(500)")
  
  elif "mediaserver" in PLATFORM_NAME:
    from platformcode.mediaserver import cliente
    cliente.Acciones().EndItems()
    
    
    
def Refresh(): #----------------------------------OK
  if "xbmc" in PLATFORM_NAME:
    import xbmc
    xbmc.executebuiltin( "Container.Refresh" )
  
  elif "mediaserver" in PLATFORM_NAME:
    from platformcode.mediaserver import cliente
    cliente.Acciones().Refrescar()
    
def Keyboard(Texto, Title="", Password=False): #----------------------------------OK
  if "xbmc" in PLATFORM_NAME:
    import xbmc

    keyboard = xbmc.Keyboard(Texto, Title, Password)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return keyboard.getText()
    else:
        return None
  
  elif "mediaserver" in PLATFORM_NAME:
    from platformcode.mediaserver import cliente  
    retorno = cliente.Dialogo().MostrarTeclado(Texto, Title, Password) 
    if retorno <>"-1": 
      return retorno
    else:
      return None
    
    
    
def play(item, ItemVideo):
  if "xbmc" in PLATFORM_NAME:
    import xbmc
    import xbmcgui
    import xbmcplugin
    if not ItemVideo == None:
      mediaurl = ItemVideo.url[1]
      if len(ItemVideo.url)>2:
          wait_time = ItemVideo.url[2]
      else:
          wait_time = 0

      if wait_time>0:
        handle_wait(wait_time,server,"Cargando vídeo...")
        
      xlistitem = xbmcgui.ListItem( item.title, iconImage="DefaultVideo.png", thumbnailImage=item.thumbnail, path=mediaurl)
      xlistitem.setInfo( "video", { "Title": item.title, "Plot" : item.plot , "Studio" : item.channel , "Genre" : item.category } )

      if item.subtitle!="":
          import os
          ficherosubtitulo = os.path.join( config.get_data_path(), 'subtitulo.srt' )
          if os.path.exists(ficherosubtitulo):
                os.remove(ficherosubtitulo)
      
          from core import scrapertools
          data = scrapertools.cache_page(item.subtitle)
          fichero = open(ficherosubtitulo,"w")
          fichero.write(data)
          fichero.close()
          

      if item.channel=="library": #Si es un fichero strm no hace falta el play
        xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),True,xlistitem)
        
      else:
        if config.get_setting("player_mode")=="3": #download_and_play
          import download_and_play
          download_and_play.download_and_play( mediaurl , "download_and_play.tmp" , config.get_setting("downloadpath"))
          
        elif config.get_setting("player_mode")=="0" or (config.get_setting("player_mode")=="3" and mediaurl.startswith("rtmp")): #Direct
        
          playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
          playlist.clear()
          playlist.add(mediaurl, xlistitem)
          playersettings = config.get_setting('player_type')
          player_type = xbmc.PLAYER_CORE_AUTO
          if playersettings == "0":
              player_type = xbmc.PLAYER_CORE_AUTO
              logger.info("[xbmctools.py] PLAYER_CORE_AUTO")
          elif playersettings == "1":
              player_type = xbmc.PLAYER_CORE_MPLAYER
              logger.info("[xbmctools.py] PLAYER_CORE_MPLAYER")
          elif playersettings == "2":
              player_type = xbmc.PLAYER_CORE_DVDPLAYER
              logger.info("[xbmctools.py] PLAYER_CORE_DVDPLAYER")
          xbmcPlayer = xbmc.Player(player_type)
          xbmcPlayer.play(playlist)
          
        elif config.get_setting("player_mode")=="1": #setResolvedUrl
          xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=mediaurl))
      
        elif config.get_setting("player_mode")=="2": #Built-in
          xbmc.executebuiltin( "PlayMedia("+mediaurl+")" )
    else:
      listitem = xbmcgui.ListItem( item.title, iconImage="DefaultVideo.png", thumbnailImage=item.thumbnail)
      xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),False,listitem)    # JUR Added
  elif "mediaserver" in PLATFORM_NAME:
    if not ItemVideo == None:
      from platformcode.mediaserver import cliente  
      url = ItemVideo.url[1]
      cliente.Acciones().Play(item.title, item.plot, url, item.url)
          
def Update(item):
  if "xbmc" in PLATFORM_NAME:
    import xbmc
    if item.folder == True and "strm" in item.extra:
      listitem = xbmcgui.ListItem( None, iconImage="DefaultVideo.png", thumbnailImage=item.thumbnail)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]),False,listitem)    # JUR Added
    xbmc.executebuiltin(ConstruirURL(item).replace("XBMC.RunPlugin","Container.Update"))
  
  elif "mediaserver" in PLATFORM_NAME:
    from platformcode.mediaserver import cliente  
    cliente.Acciones().Update(ConstruirURL(item))

def UpdateLibrary(item):
  if "xbmc" in PLATFORM_NAME:
    import xbmc
    xbmc.executebuiltin('UpdateLibrary(video)')
  
  elif "mediaserver" in PLATFORM_NAME:
    pass
    
def ConstruirURL(item):
  if "xbmc" in PLATFORM_NAME:
    return "XBMC.RunPlugin("+sys.argv[ 0 ] + "?" + item.serialize()+")" 
  
  elif "mediaserver" in PLATFORM_NAME:
    return "?" + item.serialize()
    
def ConstruirStrm(item):
  if "xbmc" in PLATFORM_NAME:
    return sys.argv[ 0 ] + "?" + item.serialize() 
  
  elif "mediaserver" in PLATFORM_NAME:
    return "?" + item.serialize()
