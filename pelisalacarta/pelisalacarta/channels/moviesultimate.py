# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para moviesultimate
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F,S,D"
__language__ = "ES"
__title__ = "MoviesUltimate"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 1
__adult__ = False
__date__ = "09/06/2015"
__creationdate__ = "09/06/2015"
__changes__ = "Version Incial"
__thumbnail__ = ""
__channel__ = "moviesultimate"

import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.moviesultimate mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Estrenos"      , action="peliculas", url="http://moviesultimate.com",thumbnail="http://s6.postimg.org/xh61j3glt/muestthum.png", fanart="http://s6.postimg.org/3wnf8xpzl/muextfan.jpg"))
    itemlist.append( Item(channel=__channel__, title="Generos"      , action="generos", url="http://moviesultimate.com" ,thumbnail="http://s6.postimg.org/qt9fwhx3l/mugenthum.png", fanart="http://s6.postimg.org/pppbkjcgh/mugenfan.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar..."      , action="search", url="", thumbnail="http://s6.postimg.org/6ofvr139t/mubuscthum.png", fanart="http://s6.postimg.org/4ilkwiztd/mubuscfan.jpg"))
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.peliculasdk search")
    texto = texto.replace(" ","+")
    
    item.url = "http://moviesultimate.com/?s=%s" % (texto)
    
    try:
        return buscador(item)
    # Se captura la excepciÛn, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscador(item):
    logger.info("pelisalacarta.peliculasdk buscador")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patron = '<img class="imx".*?src="([^"]+)".*?<h3><a href="([^"]+)">([^<]+)'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:      
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=scrapedurl, action="fanart", thumbnail=scrapedthumbnail, fanart="http://s6.postimg.org/40zm85p01/mubackground3.jpg", folder=True) )

    return itemlist

def generos(item):
    logger.info("pelisalacarta.moviesultimate peliculas")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|&#[0-9]","",data)

    patron = '<li id="menu-item-.*?" class="menu-item menu-item-type-taxonomy.*?".*?'
    patron += 'href="([^"]+)">([^"]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl , scrapedtitle in matches:
        if "Accion" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/429k1kqtt/muaccion.png"
        if "Animacion" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/bwa5myymp/animacion.png"
        if "Aventuras" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/qgr8hstld/aventura.png"
        if "Ciencia ficcion" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/4iuro0ekx/cienciaficcion.png"
        if "Comedia" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/4ww3nlyoh/comedia.png"
        if "Documentales" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/n0z488wcx/documentales.png"
        if "Drama" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/9y832pvip/drama.png"
        if "Terror" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/87p218dzl/terror.png"
        if "Familiar" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/eb6ml549d/familiar.png"
        if "Fantasia" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/3qwp2jzrl/fantasia.png"
        if "Infantil" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/li8bh0f69/infantil.png"
        if "Musical" in scrapedtitle:
            thumbnail= "http://s6.postimg.org/urahr4o29/musical.png"
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=scrapedurl, action="peliculas",thumbnail= thumbnail, fanart="http://s6.postimg.org/40zm85p01/mubackground3.jpg", folder=True) )
    return itemlist


def peliculas(item):
    logger.info("pelisalacarta.moviesultimate peliculas")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|&#.*?;","",data)
    
    
    patron = '<div class="item">.*?<a href="([^"]+)".*?'
    patron += 'title="([^<]+)">.*?'
    patron += '<img src="([^"]+)".*?'
    patron += '<span class="calidad">([^<]+)</span>'
   
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)


    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedcalidad in matches:      
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , quality=scrapedcalidad, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, fanart="http://s6.postimg.org/40zm85p01/mubackground3.jpg", folder=True) )
        
    ## Paginación
    patronvideos  = '<div class="paginacion">.*?<span class=\'current\'>.*?href=\'([^\']+)\''
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="siguiente>>" , url=scrapedurl , thumbnail="http://s6.postimg.org/drfhhwrtd/muarrow.png", fanart="http://s6.postimg.org/40zm85p01/mubackground3.jpg",  folder=True) )

    return itemlist

def findvideos(item):
    itemlist = []
    from core import scrapertools
    from servers import servertools
    from servers import longurl
    import copy
    data = scrapertools.cache_page(item.url)
    data=longurl.get_long_urls(data)  
    listavideos = servertools.findvideos(data)  
    for video in listavideos:
        NuevoItem = copy.deepcopy(item)
        if not "youtube" in video[2]:
          NuevoItem.title = "Ver en: ["  + video[2] + "]"
        else:
          NuevoItem.title = "Ver Trailer en: ["  + video[2] + "]"
        NuevoItem.url = video[1]
        NuevoItem.server = video[2]
        NuevoItem.action = "play"
        NuevoItem.folder=False
        if not "youtube" in video[2]:
          itemlist.append(NuevoItem)
        else:
          itemlist.insert(0,NuevoItem)
        
    return itemlist
