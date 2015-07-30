# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para ver un vídeo conociendo su URL
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F,S,D,A"
__language__ = ""
__title__ = "Tengo una URL"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 1
__adult__ = False
__date__ = "22/02/2012"
__creationdate__ = ""
__changes__ = "Ya puedes poner una url cualquiera!"
__thumbnail__ = ""
__channel__ = "tengourl"

import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tengourl.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="search", title="Entra aquí y teclea la URL"))

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto):
    logger.info("[tengourl.py] search texto="+texto)
    itemlist = []
    item.url=texto
    data=scrapertools.cache_page(item.url)
    
    from servers import servertools
    
    #Primer intento: la url
    itemlist = servertools.find_video_items(data=item.url)

    #Segundo intento: el contenido
    if len(itemlist)==0 and not data is None:
      itemlist = servertools.find_video_items(data=scrapertools.cache_page(item.url))
    

    return itemlist

def test():
    return True