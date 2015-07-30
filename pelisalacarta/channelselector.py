# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__version__ = 8
__adult__ = False
__date__ = "28/07/2013"
__changes__ = "Actualizado por cambio en el canal"

import os
import sys
from core import config
from core import logger
from core import updater
from core.item import Item
import urlparse
from core import scrapertools
import re


def getmainlist(item):
    logger.info("[channelselector.py] - getmainlist")
    itemlist = []

    # Obtiene el idioma, y el literal
    idioma = config.get_setting("languagefilter")
    logger.info("[channelselector.py] - getmainlist: Idioma=%s" % idioma)
    langlistv = [config.get_localized_string(30025),config.get_localized_string(30026),config.get_localized_string(30027),config.get_localized_string(30028),config.get_localized_string(30029)]
    try:
        idiomav = langlistv[int(idioma)]
    except:
        idiomav = langlistv[0]
    
    # Añade los canales que forman el menú principal
    itemlist.append( Item(title=config.get_localized_string(30118)+" ("+idiomav+")" , channel="channelselector" , action="channeltypes", thumbnail = urlparse.urljoin(config.get_thumbnail_path(),"channelselector.png") ) )
    itemlist.append( Item(title=config.get_localized_string(30103) , channel="buscador" , action="mainlist" , thumbnail = urlparse.urljoin(config.get_thumbnail_path(),"buscador.png")) )
    itemlist.append( Item(title=config.get_localized_string(30128) , channel="trailertools" , action="mainlist" , thumbnail = urlparse.urljoin(config.get_thumbnail_path(),"trailertools.png")) )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist" , thumbnail = urlparse.urljoin(config.get_thumbnail_path(),"favoritos.png")) )
    if config.get_platform() in ("wiimc","rss") :itemlist.append( Item(title="Wiideoteca (Beta)" , channel="wiideoteca" , action="mainlist", thumbnail = urlparse.urljoin(config.get_thumbnail_path(),"wiideoteca.png")) )
    if config.get_platform()=="rss":itemlist.append( Item(title="pyLOAD (Beta)" , channel="pyload" , action="mainlist" , thumbnail = urlparse.urljoin(config.get_thumbnail_path(),"pyload.png")) )
    itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist", thumbnail = urlparse.urljoin(config.get_thumbnail_path(),"descargas.png")) )
    itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = urlparse.urljoin(config.get_thumbnail_path(),"configuracion.png")) )
    itemlist.append( Item(title=config.get_localized_string(30104) , channel="ayuda" , action="mainlist", thumbnail = urlparse.urljoin(config.get_thumbnail_path(),"ayuda.png")) )
    return itemlist


def channeltypes(item):
    logger.info("[channelselector.py] - channeltypes")
    itemlist = []
    itemlist.append( Item( title=config.get_localized_string(30121) , channel="channelselector" , action="listchannels" , category="*"   , thumbnail=urlparse.urljoin(config.get_thumbnail_path(),"channelselector")))
    itemlist.append( Item( title=config.get_localized_string(30122) , channel="channelselector" , action="listchannels" , category="F"   , thumbnail=urlparse.urljoin(config.get_thumbnail_path(),"peliculas")))
    itemlist.append( Item( title=config.get_localized_string(30123) , channel="channelselector" , action="listchannels" , category="S"   , thumbnail=urlparse.urljoin(config.get_thumbnail_path(),"series")))
    itemlist.append( Item( title=config.get_localized_string(30124) , channel="channelselector" , action="listchannels" , category="A"   , thumbnail=urlparse.urljoin(config.get_thumbnail_path(),"anime")))
    itemlist.append( Item( title=config.get_localized_string(30125) , channel="channelselector" , action="listchannels" , category="D"   , thumbnail=urlparse.urljoin(config.get_thumbnail_path(),"documentales")))
    itemlist.append( Item( title=config.get_localized_string(30136) , channel="channelselector" , action="listchannels" , category="VOS" , thumbnail=urlparse.urljoin(config.get_thumbnail_path(),"versionoriginal")))
    itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="M"   , thumbnail=urlparse.urljoin(config.get_thumbnail_path(),"musica")))
    itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="G"   , thumbnail=urlparse.urljoin(config.get_thumbnail_path(),"servidores")))
    return itemlist
    
def listchannels(item):
    itemlist = []
    try:
        idioma = config.get_setting("languagefilter")
        logger.info("channelselector.filterchannels idioma=%s" % idioma)
        langlistv = ["","ES","EN","IT","PT"]
        idiomav = langlistv[int(idioma)]
        logger.info("channelselector.filterchannels idiomav=%s" % idiomav)
    except:
        idiomav=""

    folderchannels =  []
    disabledchannels =  []
    channelslist =[]
    hiddenchannels = ["__init__.py","ayuda.py"]
    
    for channel in os.listdir(os.path.join(config.get_runtime_path(),"pelisalacarta","channels")):
      if channel.endswith(".py") and not channel in  hiddenchannels:

          f = open(os.path.join(config.get_runtime_path(),"pelisalacarta","channels",channel),"r")
          txt = f.read(1024)
          f.close()
          patron = '(__([^_]+)__[ ]*=[ ]*["]*[\']*([^"\r\n]*)["]*[\']*[\r]*[\n]*)'
          matches = re.compile(patron,re.DOTALL).findall(txt)
          Propiedades = {}
          for Todo, key, valor in matches:
            try:
              Propiedades[key] =  int(valor)
            except:
              if valor == "True":
                Propiedades[key] =  True
              elif valor == "False":
                Propiedades[key] =  False
              else:
                Propiedades[key] =  valor

          
          #Filtro canales desactivados
          if not Propiedades["disabled"]:
            #Filtro Canales adultos
            if (Propiedades["adult"] and (config.get_setting("enableadultmode") == "true")) or not Propiedades["adult"]:
            #Filtro Categoria
              if item.category=="*" or item.category in Propiedades["category"]:
                #Filtro Idioma
                if Propiedades["language"]=="" or idiomav=="" or idiomav in Propiedades["language"]:
                  #Canal TengoUrl al principio de trodo
                  if Propiedades["channel"]=="tengourl":
                    channelslist.append(Item(title=Propiedades["title"], channel=Propiedades["channel"],action="mainlist", thumbnail=Propiedades["thumbnail"], fanart=Propiedades["fanart"], type=Propiedades["type"], category=Propiedades["category"], language=Propiedades["language"] ))
                  else:
                    folderchannels.append(Item(title=Propiedades["title"], channel=Propiedades["channel"],action="mainlist", thumbnail=Propiedades["thumbnail"], fanart=Propiedades["fanart"], type=Propiedades["type"], category=Propiedades["category"], language=Propiedades["language"] ))
                    
    if config.get_setting("personalchannel")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname") ,action="mainlist", channel="personal" ,thumbnail=config.get_setting("personalchannellogo"), language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel2")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname2") ,action="mainlist", channel="personal2" ,thumbnail=config.get_setting("personalchannellogo2"), language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel3")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname3") ,action="mainlist", channel="personal3" ,thumbnail=config.get_setting("personalchannellogo3"), language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel4")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname4") ,action="mainlist", channel="personal4" ,thumbnail=config.get_setting("personalchannellogo4"), language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel5")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname5") ,action="mainlist", channel="personal5" ,thumbnail=config.get_setting("personalchannellogo5"), language="" , category="F,S,D,A" , type="generic"  ))

    folderchannels.sort(key=lambda item: item.title.lower().strip())
    channelslist.extend(folderchannels)

    for channel in channelslist:
        if channel.thumbnail == "": channel.thumbnail = urlparse.urljoin(config.get_thumbnail_path(),channel.channel+".png")
        channel.plot = channel.category.replace("VOS","Versión original subtitulada").replace("F","Películas").replace("S","Series").replace("D","Documentales").replace("A","Anime").replace(",",", ")
        itemlist.append(channel)

    return itemlist

