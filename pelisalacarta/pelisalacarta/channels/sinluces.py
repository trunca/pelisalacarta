# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para sinluces
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F,S"
__language__ = "ES"
__title__ = "Sinluces"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 0
__adult__ = False
__date__ = ""
__creationdate__ = ""
__changes__ = ""
__thumbnail__ = "http://s14.postimg.org/cszkmr7a9/sinluceslogo.jpg"
__channel__ = "sinluces"

import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

host = "http://www.sinluces.com/"


def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.sinluces mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"   , action="peliculas", url="http://sinluces.com/page/1/", fanart="http://s17.postimg.org/rnup1a333/sinlestfan.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series"      , action="peliculas", url="http://sinluces.com/series", fanart="http://s17.postimg.org/rnup1a333/sinlestfan.jpg"))

    itemlist.append( Item(channel=__channel__, title="Buscar Películas"      , action="search", url = "http://sinluces.com/?s=%s", fanart="http://s22.postimg.org/3tz2v05ap/sinlbufan.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar Series"      , action="search", url = "http://sinluces.com/series/?s=%s", fanart="http://s22.postimg.org/3tz2v05ap/sinlbufan.jpg"))
    
    return itemlist
    
def search(item,texto):
    logger.info("pelisalacarta.sinluces search")
    texto = texto.replace(" ","+")
    item.url = item.url % (texto)
    
    try:
        return peliculas(item)
    # Se captura la excepciÛn, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item,paginacion=True):
    logger.info("pelisalacarta.sinluces peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    patron  = '<div class="movie">.*?<div class="imagen">.*?<img src="([^"]+)" alt="[^"]+".*?/>.*?'
    patron += '<a href="([^"]+)"><span class="player"></span></a>.*?'
    patron += '<div class="imdb"><span class="icon-grade"></span>([^<]+)</div>.*?'
    patron += '<h2>([^<]+)</h2>.*?'
    patron += '<span class="year">([^<]+)</span>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedthumbnail, scrapedurl, scrapedrate, scrapedtitle, scrapedyear in matches:     
        plot  = "Año: [COLOR orange][B]" + scrapedyear + "[/B][/COLOR]"
        plot += " Puntuacuón: [COLOR orange][B]" + scrapedrate + "[/B][/COLOR]"
        if not "/series/" in scrapedurl:
          itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle, plot=plot , url=scrapedurl , thumbnail=scrapedthumbnail ,  viewmode="movie",  fanart="http://s30.postimg.org/4gugdsygx/sinlucesfan.jpg") )      
        else:
          itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle, plot=plot , url=scrapedurl , thumbnail=scrapedthumbnail ,  viewmode="movie",  fanart="http://s30.postimg.org/4gugdsygx/sinlucesfan.jpg") )
 
    # Extrae el paginador
    matches = re.compile('<div class="siguiente"><a href="([^"]+)" >Siguiente <span class="icon-caret-right"></span>',re.DOTALL).findall(data)
    if len(matches):
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página Siguiente >>" , url=matches[0], fanart="http://s30.postimg.org/4gugdsygx/sinlucesfan.jpg" , folder=True) )

    return itemlist


def findvideos(item):
    logger.info("pelisalacarta.sinluces findvideos")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    patron  = '<div id="([^"]+)" class="player-content">(<iframe[^>]+></iframe>)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    plot = scrapertools.get_match(data,'<h2>Sinopsis</h2>.*?<p>(.*?)</p>')
    for id, iframe in matches:
      idioma = scrapertools.get_match(data,'<li[^>]*><a href="#'+id+'">(.*?) [0-9]+.*?</a></li>').strip()
      from servers import servertools
      videoitems = servertools.find_video_items(data=iframe)
      for videoitem in videoitems:
        videoitem.title ="Ver en: " + videoitem.server + " ("+idioma+")"
        videoitem.fanart="http://s30.postimg.org/4gugdsygx/sinlucesfan.jpg"
        videoitem.thumbnail=item.thumbnail
        videoitem.plot=plot
        itemlist.append(videoitem)

    return itemlist
    
def findvideosseries(item):
    logger.info("pelisalacarta.sinluces findvideos")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    patron  = '<div id="([^"]+)" class="player-content"><p>(<iframe[^>]+></iframe>)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    plot = scrapertools.get_match(data,'<div class="datos episodio">.*?<i></i></p>.*?<p>(.*?)</p>')
    for id, iframe in matches:
      idioma = scrapertools.get_match(data,'<li[^>]*><a href="#'+id+'">(.*?)</a></li>')
      from servers import servertools
      videoitems = servertools.find_video_items(data=iframe)
      for videoitem in videoitems:
        videoitem.title ="Ver en: " + videoitem.server + " ("+idioma+")"
        videoitem.fanart="http://s30.postimg.org/4gugdsygx/sinlucesfan.jpg"
        videoitem.thumbnail=item.thumbnail
        videoitem.plot=plot
        itemlist.append(videoitem)

    return itemlist
    
def episodios(item):
    logger.info("pelisalacarta.sinluces findvideos")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    patron  = '<li>.*?<a href="([^"]+)" target="_blank">.*?<span class="datex">([^<]+)</span>.*?<span class="datix"><b class="icon-chevron-right"></b>([^<]+)</span>.*?<i><b class="icon-query-builder"></b>([^<]+)</i>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for url, episode, title, duration in matches:
      episode = "%01dx%02d" % (int(episode.split("-")[0].strip()), int(episode.split("-")[1].strip()))
      title = episode + " - " + title
      itemlist.append( Item(channel=__channel__, action="findvideosseries", title=title, plot="" , url=url , thumbnail=item.thumbnail, fanart="http://s30.postimg.org/4gugdsygx/sinlucesfan.jpg") )      


    return itemlist