# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import sys

from core import config
from core import logger
from core.item import Item
import channelselector


DEBUG = config.get_setting("debug")

__type__ = "generic"
__title__ = "Buscador"
__channel__ = "buscador"

Threads={}

def isGeneric():
    return True

def mainlist(item):
    logger.info("[buscador.py] mainlist")
    itemlist =[]
    itemlist.append( Item(channel="buscador", action="search", title=config.get_localized_string(30103)+"...", thumbnail="http://pelisalacarta.mimediacenter.info/squares/search.png"))
    itemlist.append( Item(channel="buscador", action="MenuConfig", title="Configuración"))
    itemlist.extend(listar_busquedas())

    return itemlist
    
def MenuConfig(item):
    logger.info("[buscador.py] MenuConfig")
    itemlist =[]
    itemlist.append( Item(channel="buscador", action="Canales", title="Activar/Desactivar Canales"))
    itemlist.append( Item(channel="buscador", action="Reset", title="Resetear estadisticas"))
    if config.get_setting("buscador_resultados", "buscador") =="1":
      itemlist.append( Item(channel="buscador", action="CambiarModo", title="Resultados: Por canales"))
    else:
      itemlist.append( Item(channel="buscador", action="CambiarModo", title="Resultados: Todo junto"))
    if config.get_setting("buscador_multithread", "buscador") =="1":
      itemlist.append( Item(channel="buscador", action="CambiarMultithread", title="Multithread: Activado"))
    else:
      itemlist.append( Item(channel="buscador", action="CambiarMultithread", title="Multithread: Desactivado"))
    return itemlist

def search(item,tecleado):
    logger.info("[buscador.py] search "+tecleado)
    item.url=tecleado
    return por_tecleado(item)
    
def CambiarModo(item):
  itemlist=[]
  if config.get_setting("buscador_resultados", "buscador") =="1":
    config.set_setting("buscador_resultados",'0', "buscador")
    itemlist.append( Item(channel="launcher", action="refresh", title="Cambiado a: Todo junto"))
  else:
    config.set_setting("buscador_resultados",'1', "buscador")
    itemlist.append( Item(channel="launcher", action="refresh", title="Cambiado a: Por canales"))

  return itemlist
  
def CambiarMultithread(item):
  itemlist=[]
  if config.get_setting("buscador_multithread", "buscador") =="1":
    config.set_setting("buscador_multithread",'0', "buscador")
    itemlist.append( Item(channel="launcher", action="refresh", title="Multithread Desactivado"))
  else:
    config.set_setting("buscador_multithread",'1', "buscador")
    itemlist.append( Item(channel="launcher", action="refresh", title="Multithread Activado"))


  return itemlist

def Canales(item):
    logger.info("[buscador.py] Canales")
    itemlist=[]
    Canales =  channelselector.listchannels(Item(category=""))
    Canales.remove(Canales[0])
    itemlist.append(Item(channel="buscador", action="ActivarTodos", title="Activar Todos"))
    itemlist.append(Item(channel="buscador", action="DesactivarTodos", title="Desactivar Todos"))
    for Canal in Canales:
      IndexConfig, ConfigCanales = ExtraerIndice(Canal.channel)  
      if ConfigCanales[IndexConfig].split(",")[1] == "1":
        Titulo = "[x] - " + Canal.title
      else:
        Titulo = "[  ] - " + Canal.title
        
      if ConfigCanales[IndexConfig].split(",")[2] <> "0":
        Titulo =("["+ "%05.2f" % float(float(ConfigCanales[IndexConfig].split(",")[3]) / float(ConfigCanales[IndexConfig].split(",")[2])) +" Seg] - ").replace(".", ",") + Titulo
      else:
        Titulo = "[00,00 Seg] - "+ Titulo 
      itemlist.append(Item(channel="buscador", action="ActivarDesactivar", title=Titulo, url=Canal.channel))

    return itemlist
    
def Reset(item):
    logger.info("[buscador.py] Reset")
    itemlist=[]
    ConfigCanales = []
    if config.get_setting("canales_buscador", "buscador"):
      ConfigCanales.extend(config.get_setting("canales_buscador", "buscador").split("|"))
      IndexConfig = -1
      for x, Config in enumerate(ConfigCanales):
        ConfigCanales[x] = ConfigCanales[x].split(",")[0] + "," + ConfigCanales[x].split(",")[1] + "," +"0" + "," +"0"
      config.set_setting("canales_buscador",'|'.join(ConfigCanales), "buscador")
    
    itemlist.append( Item(channel="launcher", action="alert", title="Estadisticas reseteadas"))
    return itemlist

def ExtraerIndice(Canal):
    logger.info("[buscador.py] ExtraerIndice")
    ConfigCanales = []
    if config.get_setting("canales_buscador", "buscador"):
      ConfigCanales.extend(config.get_setting("canales_buscador", "buscador").split("|"))
    IndexConfig = -1
    for x, Config in enumerate(ConfigCanales):
      if Canal in Config:
        IndexConfig = x
        break
    if IndexConfig == -1: 
      logger.info("[buscador.py] EstraerIndice Creando configuración para: "+ Canal)
      ConfigCanales.append(Canal + "," + "1" + "," + "0" + "," + "0")
      config.set_setting("canales_buscador",'|'.join(ConfigCanales), "buscador")
      IndexConfig = len(ConfigCanales) - 1

    return IndexConfig, ConfigCanales
    
def ActivarDesactivar(item):
    logger.info("[buscador.py] ActivarDesactivar")
    IndexConfig, ConfigCanales = ExtraerIndice(item.url)
    Activo = ConfigCanales[IndexConfig].split(",")[1]
    if Activo == "1":
      Activo ="0"
    else:
      Activo ="1"  
    ConfigCanales[IndexConfig] =  ConfigCanales[IndexConfig].split(",")[0] +","+ Activo+"," + ConfigCanales[IndexConfig].split(",")[2]+"," + ConfigCanales[IndexConfig].split(",")[3]
    config.set_setting("canales_buscador",'|'.join(ConfigCanales), "buscador")
    itemlist=[]
    if Activo =="1":
      itemlist.append( Item(channel="launcher", action="refresh", title="Canal activado"))
    else:
      itemlist.append( Item(channel="launcher", action="refresh", title="Canal desactivado"))
    return itemlist
    
def ActivarTodos(item):
    logger.info("[buscador.py] ActivarTodos")
    itemlist=[]
    ConfigCanales = []
    if config.get_setting("canales_buscador", "buscador"):
      ConfigCanales.extend(config.get_setting("canales_buscador", "buscador").split("|"))
      
    for x, Config in enumerate(ConfigCanales):
      ConfigCanales[x] =  ConfigCanales[x].split(",")[0] +","+ "1" +"," + ConfigCanales[x].split(",")[2]+"," + ConfigCanales[x].split(",")[3]
    config.set_setting("canales_buscador",'|'.join(ConfigCanales), "buscador")
    itemlist.append( Item(channel="launcher", action="refresh", title="Canales Activados"))
    return itemlist

def DesactivarTodos(item):
    logger.info("[buscador.py] DesactivarTodos")
    itemlist=[]
    ConfigCanales = []
    if config.get_setting("canales_buscador", "buscador"):
      ConfigCanales.extend(config.get_setting("canales_buscador", "buscador").split("|"))
      
    for x, Config in enumerate(ConfigCanales):
      ConfigCanales[x] =  ConfigCanales[x].split(",")[0] +","+ "0" +"," + ConfigCanales[x].split(",")[2]+"," + ConfigCanales[x].split(",")[3]
    config.set_setting("canales_buscador",'|'.join(ConfigCanales), "buscador")
    itemlist.append( Item(channel="launcher", action="refresh", title="Canales Activados"))
    return itemlist
    
def GuardarTiempo(Canal,Tiempo):
    logger.info("[buscador.py] GuardarTiempo")
    if not config.get_setting("canales_buscador", "buscador"): Canales(Item())
    ConfigCanales = config.get_setting("canales_buscador", "buscador").split("|")
    for x, Config in enumerate(ConfigCanales):
      if Canal in Config:
        IndexConfig = x
        break
    Busquedas = int(ConfigCanales[x].split(",")[2]) + 1
    Tiempos = float(ConfigCanales[x].split(",")[3]) + Tiempo
    ConfigCanales[x] =  ConfigCanales[x].split(",")[0] +","+ ConfigCanales[x].split(",")[1]+"," + str(Busquedas)+"," + str(Tiempos)
    config.set_setting("canales_buscador",'|'.join(ConfigCanales), "buscador")

def por_tecleado(item):
    logger.info("[buscador.py] por_tecleado")
    import time
    tecleado =item.url
    itemlist = []
    salvar_busquedas(item)
    channels =  channelselector.listchannels(Item(category=""))
    channels.remove(channels[0])
    from threading import Thread
    from core import guitools
    progreso = guitools.Dialog_Progress("Buscador","Buscando '"+item.url+"'")
    x = 0
    for channel in channels:
      x+=1
      IndexConfig, ConfigCanales = ExtraerIndice(channel.channel)  
      if ConfigCanales[IndexConfig].split(",")[1] == "1":
        if config.get_setting("buscador_multithread", "buscador") =="1":
          time.sleep(0.1)
          Trd = Thread(target=buscar,args=[itemlist,channel,tecleado])
          progreso.Actualizar(x*100/len(channels),"Lanzando búsqueda: '"+item.url+"' \nEn canal: "+channel.channel)
          Threads[Trd.name] =None
          Trd.start()
          if progreso.IsCanceled(): break
        else:
           Inicio = time.time()
           progreso.Actualizar(x*100/len(channels),"Buscando: '"+item.url+"' \nEn canal: "+channel.channel)
           buscar(itemlist, channel, tecleado)
           GuardarTiempo(channel.channel, time.time()-Inicio)
           if progreso.IsCanceled(): break
    
    if config.get_setting("buscador_multithread", "buscador") =="1":  
      for busqueda in Threads:
        while Threads[busqueda]["Tiempo"] ==None:
          time.sleep(0.5)
          progreso.Actualizar(100,"Esperando resultados de: "+Threads[busqueda]["Canal"])
          if progreso.IsCanceled(): break
        if not progreso.IsCanceled():
          GuardarTiempo(Threads[busqueda]["Canal"], Threads[busqueda]["Tiempo"])
        else:
          break
        
    itemlist.sort(key=lambda item: item.title.lower().strip())
    progreso.Cerrar()
    return itemlist
    
def buscar(Globalitemlist,modulo, texto):
    logger.info("Lanzando búseda en: "+ modulo.channel)
    import threading
    import urlparse
    Threads[threading.current_thread().name] = {"Canal":modulo.channel,"Tiempo":None}
    ListaCanales = []
    import time
    Inicio = time.time()
    try:
      exec "from pelisalacarta.channels import "+modulo.channel+" as channel"
      mainlist_itemlist = channel.mainlist(Item())
      for item in mainlist_itemlist:
          if item.action =="search":
            url = item.url
            itemlist = []
            itemlist.extend(channel.search(item, texto))
            if config.get_setting("buscador_resultados", "buscador") =="1":
              if len(itemlist)>0:  
                cantidad = str(len(itemlist))
                if len(itemlist) >1:
                  if itemlist[len(itemlist)-1].action <> itemlist[len(itemlist)-2].action:
                    cantidad = str(len(itemlist)) + "+"
                ListaCanales.append( Item(channel=__channel__ , thumbnail=urlparse.urljoin(config.get_thumbnail_path(),modulo.channel+".png"),action='buscar_canal', url=modulo.channel +"{}"+ url +"{}"+ texto, title=modulo.title + " (" + cantidad + ")" ))
            else:
              
              if len(itemlist) >1:
                if itemlist[len(itemlist)-1].action <> itemlist[len(itemlist)-2].action:
                    itemlist.remove(itemlist[len(itemlist)-1])
              ListaCanales.extend(itemlist)
              
    except:
      logger.info("No se puede buscar en: "+ modulo.channel)  
    Globalitemlist.extend( ListaCanales)
    if config.get_setting("buscador_multithread", "buscador") =="1":
      Threads[threading.current_thread().name]["Tiempo"]=time.time()-Inicio
    
def buscar_canal(item):
    itemlist = []
    logger.info("[buscador.py] buscar_canal")
    exec "from pelisalacarta.channels import "+item.url.split("{}")[0]
    exec "itemlist.extend("+item.url.split("{}")[0]+".search(Item(url=item.url.split('{}')[1]), item.url.split('{}')[2]))"

    return itemlist
    
def salvar_busquedas(item):
    logger.info("[buscador.py] salvar_busquedas")
    limite_busquedas =int(config.get_setting( "limite_busquedas", "" ))
    presets = config.get_setting("presets_buscados", "buscador" ).split("|")
    if item.url in presets: presets.remove(item.url) 
    presets.insert(0,item.url)     
    if limite_busquedas>0:
          presets = presets[:limite_busquedas]
    config.set_setting("presets_buscados",'|'.join(presets), "buscador")
        
def listar_busquedas():
    logger.info("[buscador.py] listar_busquedas")
    itemlist=[]
    presets = config.get_setting("presets_buscados", "buscador" ).split("|")
    for preset in presets:
        if preset <> "": itemlist.append( Item(channel=__channel__ , context="Borrar,borrar_busqueda", action="por_tecleado", title="- " + preset ,  url=preset))       
    return itemlist
    
def borrar_busqueda(item):
    logger.info("[buscador.py] borrar_busqueda")
    itemlist = []
    presets = config.get_setting("presets_buscados", "buscador" ).split("|")
    presets.remove(item.url)
    config.set_setting("presets_buscados",'|'.join(presets), "buscador")
    itemlist.append( Item(channel="launcher", action="refresh", title="Registro borrado"))
    return itemlist