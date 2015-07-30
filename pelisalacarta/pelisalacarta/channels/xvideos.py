# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para xvideos.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F"
__language__ = "EN"
__title__ = "xvideos"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 1
__adult__ = True
__date__ = "22/07/2015"
__creationdate__ = ""
__changes__ = "version inicial"
__thumbnail__ = ""
__channel__ = "xvideos"

import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[xvideos.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="videos"            , title="Útimos videos"       , url="http://www.xvideos.com/"))
    itemlist.append( Item(channel=__channel__, action="listcategorias"    , title="Listado categorias"  , url="http://www.xvideos.com/"))
    itemlist.append( Item(channel=__channel__, action="search"            , title="Buscar"              , url="http://www.xvideos.com/?k=" ))
    return itemlist

def videos(item):
    logger.info("[xvideos.py] videos")
    data = scrapertools.cache_page(item.url)
    itemlist = []

    patron = '<div class="thumbInside">.*?<div class="thumb">.*?<a href="[^"]+"><img src="([^"]+)" id="[^"]+".*?/></a>'
    patron +='.*?<a href="([^"]+)" title="([^"]+)"[^<]+</a></p>.*?<span class="duration">\(([0-9]+) min\)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for thumbnail, url, title, duration in matches:
      url = "http://www.xvideos.com" + url           
      itemlist.append( Item(channel=__channel__, server="xvideos", action="play" , title=title, duration=int(duration)*60 , url=url, thumbnail=thumbnail, folder=False))


    #Paginador
    patron = '<li><a class="nP" href="([^"]+)">Next</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)  
    if len(matches) >0:
      scrapedurl = "http://www.xvideos.com"+matches[0]
      itemlist.append( Item(channel=__channel__, action="videos", title="Página Siguiente" , url=scrapedurl , thumbnail="" , folder=True) )
    
    return itemlist
  
  
  
def listcategorias(item):
    logger.info("[xvideos.py] listcategorias")
    data = scrapertools.cache_page(item.url)
    
    data = scrapertools.get_match(data,'<div id="categories" class="pagination lighter">(.*?)</div> <!-- #categories -->')
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    for url, categoria in matches:
      url= "http://www.xvideos.com" + url
      itemlist.append( Item(channel=__channel__, action="videos" , title=categoria, url=url))
    itemlist.sort(key=lambda item: item.title.lower().strip())  
    return itemlist
  
def search(item,texto):
    logger.info("[xvideos.py] search")
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        return videos(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    # mainlist
    mainlist_items = mainlist(Item())
    videos_items = videos(mainlist_items[0])
    play_items = play(videos_items[0])

    if len(play_items)==0:
        return False

    return True
