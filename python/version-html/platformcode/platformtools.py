# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# platformtools
# Herramienta para trabajar con la plataforma, Version KODI
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
'''
Dialogos:
  ProgressDialog:
    Descripcion:
      Muestra un cuadro de dialgo de progreso, con un boton para cancelar.
    Uso:
      dialogo = ProgressDialog(title, text, percent)      <- Muestra el dialogo
      dialogo.update(percent, text)                       <- Actualiza el progreso
      dialogo.iscanceled()                                <- Devuelve True si el usuario ha cancelado
      dialogo.close()                                     <- Cierra el dialogo

  ProgressDialogBG
    Descripcion:
      Muestra un cuadro de dialgo de progreso en segundo plano.
    Uso:
      dialogo = ProgressDialogBG(title, text, percent)    <- Muestra el dialogo
      dialogo.update(percent, text)                       <- Actualiza el progreso
      dialogo.iscanceled()                                <- Devuelve siempre False, creado para mantener la estructura del ProgressDialog
      dialogo.close()                                     <- Cierra el dialogo

  AlertDialog
    Descripcion:
      Muestra un cuadro de dialgo con un boton para Aceptar.
    Uso:
      AlertDialog(title, text)                            <- Muestra el dialogo

  YesNoDialog
    Descripcion:
      Muestra un cuadro de dialgo con dos botones, Si / No.
    Uso:
      resultado = YesNoDialog(title, text)                <- Muestra el dialogo y devuelve True si presiona en SI y False si presiona en No

  SelectDialog
    Descripcion:
      Muestra un cuadro de dialgo con una lista de opciones para seleccionar.
    Uso:
      resultado = YesNoDialog(title, text)                <- Muestra el dialogo y devuelve la opcion seleccionada, -1 si no se selecciona nada

  InputDialog
    Descripcion:
      Muestra un cuadro de dialgo para introducir texto. Si password = True, oculta los caracteres
    Uso:
      resultado = InputDialog(title, default, password)   <- Muestra el dialogo y devuelve el texto introducido, None si se presiona en cancelar

Itemlist:
  ItemlistRefresh
    Descripcion:
      Vuelve a cargar la ultima petición
    Uso:
      ItemlistRefresh()                                   <- Recargarga el listado

  ItemlistUpdate
    Descripcion:
      Ejecuta el item pasado y carga el resultado
    Uso:
      ItemlistUpdate(item)                                <- Carga el item

  renderItems
    Descripcion:
      Función encargada de cargar el itemlist, hay que pasarle el itemlist y el item "padre"
    Uso:
      renderItems(itemlist, parentitem)                                <- Carga el listado

Video:
  IsPlaying
    Descripcion:
      Devuelve True si se esta reproduciendo un video
    Uso:
      IsPlaying()                                   <- Devuelve True si se esta reproduciendo un video


  PlayVideo
    Descripcion:
     función encargada de reproducir un vídeo, despues de pasar por el conector, cuando ya tengamos la url reproducible del video.
     la url del video deve ponerse en item.video_url
    Uso:
      PlayVideo(item)                                   <- Reproduce el vídeo

'''

import os
import sys
import cliente
from core import config
from core import logger

'''
Funciones relacionadas con los dialogos
'''


# Progress dialog
def ProgressDialog(title, text, percent=0):
    class Dialog(object):
        def __init__(self, title, text, percent, PObject):
            self.PObject = PObject
            self.closed = False
            self.title = title
            self.PObject.ProgresoAbrir(title, text,0)

        def iscanceled(self):
            return self.PObject.ProgresoIsCanceled() or self.closed

        def update(self, percent, text):
            self.PObject.ProgresoActualizar(self.title, text, percent)

        def close(self):
            self.PObject.ProgresoCerrar()
            self.closed = True

    return Dialog(title, text, percent, cliente.Dialogo())


# Background Progress dialog
def ProgressDialogBG(title, text, percent=0):
    class Dialog(object):
        def __init__(self, title, text, percent, PObject):
            self.PObject = PObject
            self.title = title
            self.PObject.ProgresoBGAbrir(title, text,0)

        def iscanceled(self):
            return False

        def update(self, percent, text):
            self.PObject.ProgresoBGActualizar(self.title, text, percent)

        def close(self):
            self.PObject.ProgresoBGCerrar()

    return Dialog(title, text, percent, cliente.Dialogo())


# Dialog Alert
def AlertDialog(title, text):
    cliente.Dialogo().MostrarOK(title,text)


# Dialog Yes/No
def YesNoDialog(title, text):
    return cliente.Dialogo().MostrarSiNo(title,text)


# Dialog select
def SelectDialog(title, options):
    return cliente.Dialogo().Select(title,options)


# Dialog input
def InputDialog(title="", default="", password=False):
    return cliente.Dialogo().MostrarTeclado(default, title, password) 


'''
Funciones relacionadas con la generacion de los itemlist
'''


# Refresh
def ItemlistRefresh():
    cliente.Acciones().Refrescar()


# Update
def ItemlistUpdate(item):
    cliente.Acciones().Update(item.tourl())


# RenderItems
def renderItems(itemlist, parentitem):
    from core.item import Item
        
    if (parentitem.channel=="channelselector" and parentitem.action=="mainlist") or (parentitem.channel=="novedades" and parentitem.action=="mainlist") or (parentitem.channel=="buscador" and parentitem.action=="mainlist") or (parentitem.channel=="channelselector" and parentitem.action=="channeltypes"):
      WindowMode = 0
    elif parentitem.channel=="channelselector" and parentitem.action=="listchannels":
      WindowMode = 1
    else:
      WindowMode = 2
    
    if not (parentitem.channel=="channelselector" and parentitem.action=="mainlist") and not itemlist[0].action=="go_back":
      if WindowMode !=2:
        itemlist.insert(0,Item(title="Atrás", action="go_back",thumbnail=os.path.join(config.get_runtime_path(),"resources","images","bannermenu","thumb_atras.png")))
      else:
        itemlist.insert(0,Item(title="Atrás", action="go_back",thumbnail=os.path.join(config.get_runtime_path(),"resources","images","squares","thumb_atras.png")))
        
    import channelselector
    for item in itemlist:
        if item.thumbnail == "" and item.action == "search": item.thumbnail = channelselector.get_thumbnail_path() + "thumb_buscar.png"
        if item.thumbnail == "" and item.folder == True: item.thumbnail = channelselector.get_thumbnail_path() + "thumb_folder.png"
        if item.thumbnail == "" and item.folder == False: item.thumbnail = channelselector.get_thumbnail_path() + "thumb_nofolder.png"
        
        if "http://media.tvalacarta.info/" in item.thumbnail and WindowMode != 2: item.thumbnail = channelselector.get_thumbnail_path("bannermenu") + os.path.basename(item.thumbnail)

        if item.fanart == "":
            channel_fanart = os.path.join(config.get_runtime_path(), 'resources', 'images', 'fanart',
                                          item.channel + '.jpg')
            if os.path.exists(channel_fanart):
                item.fanart = channel_fanart
            else:
                item.fanart = os.path.join(config.get_runtime_path(), "fanart.jpg")

        if item.category == "":
            item.category = parentitem.category

        if item.fulltitle == "":
            item.fulltitle = item.title

        if item.fanart == "":

            channel_fanart = os.path.join(config.get_runtime_path(), 'resources', 'images', 'fanart',
                                          item.channel + '.jpg')

            if os.path.exists(channel_fanart):
                item.fanart = channel_fanart
            else:
                item.fanart = os.path.join(config.get_runtime_path(), "fanart.jpg")

        AddNewItem(item, totalItems=len(itemlist))
        
    


    cliente.Acciones().EndItems(WindowMode)


# AddnewItem
def AddNewItem(item, totalItems=0):
    item.title = unicode(item.title, "utf8", "ignore").encode("utf8")
    item.fulltitle = unicode(item.fulltitle, "utf8", "ignore").encode("utf8")
    item.plot = unicode(item.plot, "utf8", "ignore").encode("utf8")

    contextCommands = []
    if type(item.context) == list:
      for context in item.context:
        contextitem = item.clone()
        contextitem.action = context["action"]
        contextitem.item_action = item.action
        if "channel" in context and context["channel"]:
          contextitem.channel = context["channel"]
        contextCommands.append([context["title"],contextitem.tourl()])
   

    cliente.Acciones().AddItem(item.title,item.thumbnail,item.fanart,item.plot, item.tourl(),contextCommands, item.action)


'''
Funciones relacionadas con la reproduccion del vídeo
'''


# IsPlaying
def IsPlaying():
    return cliente.Acciones().isPlaying()


# PlayVideo:
def PlayVideo(item):
    if item.server == "torrent":
      return
      
    cliente.Acciones().Play(item.title, item.plot, item.video_url, item.url)
 