# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para youanimehd creado por Itsuki Minami
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "A"
__language__ = "ES"
__title__ = "YouAnime HD"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 0
__adult__ = False
__date__ = ""
__creationdate__ = "02/02/2013"
__changes__ = ""
__thumbnail__ = ""
__channel__ = "youanimehd"


import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[youanimehd.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="completo"  , title="Portada"                        , url="http://youanimehd.com/" ))
    itemlist.append( Item(channel=__channel__, action="letras"    , title="Listado Alfabetico"             , url="http://youanimehd.com/" ))
    itemlist.append( Item(channel=__channel__, action="completo"  , title="Listado Completo de Animes"     , url="http://youanimehd.com/videos" ))
    itemlist.append( Item(channel=__channel__, action="completo"  , title="Listado Completo de Peliculas"  , url="http://youanimehd.com/tags/pelicula" ))
    itemlist.append( Item(channel=__channel__, action="completo"  , title="Listado Completo de Dibujos"  , url="http://youanimehd.com/tags/cartoon" ))
    itemlist.append( Item(channel=__channel__, action="completo"  , title="Listado Completo de Doramas"    , url="http://youanimehd.com/tags/dorama" ))
    #itemlist.append( Item(channel=__channel__, action="search"  , title="Buscar"                            , url="http://youanimehd.com/buscar/" ))
  
    return itemlist

def completo(item):
    logger.info("[youanimehd.py] completo")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<!-- Video List -->(.*?)<!-- End Video List -->")

    patronvideos = '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)" id="[^"]+" alt="[^"]+"[^<]+</a[^<]+</div[^<]+<div class="videoTitle"[^<]+<a[^>]+>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)    

    for url,plot,thumbnail,title in matches:
        scrapedtitle = title
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = plot

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle, viewmode="movie_with_plot"))

    patronvideos = '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)" alt="[^"]+"[^<]+</a[^<]+</div[^<]+<div class="videoTitle"[^<]+<a[^>]+>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)    

    for url,plot,thumbnail,title in matches:
        scrapedtitle = title
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = plot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle, viewmode="movie_with_plot"))

    patron = '<li><a href="([^"]+)">Next</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches) > 0:
        itemlist.append( Item(channel=__channel__, action="completo", title="Página Siguiente >" , url=matches[0]) )        

    return itemlist

def letras(item):
    logger.info("[youanimehd.py] letras")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<!-- End Of Header -->(.*?)<!-- Page Start -->")

    patronvideos = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)    

    for url,letra in matches:
        itemlist.append( Item(channel=__channel__, action="completo" , title=letra , url=url))
    return itemlist


def serie(item):
    logger.info("[youanimehd.py] serie")
    itemlist = []    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = data.replace('\n',"")
    data = scrapertools.get_match(data,'<div class="sc_menu"[^<]+<ul class="sc_menu">(.*?)<!-- End Main Box -->')

    # Saca el argumento
    patronplot  = '<li class="videoDesc">([^<]+)</li>'
    scrapedplot = scrapertools.get_match(data,patronplot)
    patronvideos = ' <li><a target="vides" href="([^"]+)"[^<]+<img\s+src="([^"]+)"[^<]+<span style="color:red">([^"]+)</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show, folder=False))

    return itemlist

def play(item):
    logger.info("[youanimehd.py] play")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    patronvideos = '<iframe src="http\://educandroid.com/PHP_stream_vk/video_ext.php\?oid=([^&]+)&id=([^&]+)&hash=([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)  
    
    for oid, id, hash in matches:
      url = "http://vk.com/video_ext.php?oid="+oid+"&id="+id+"&hash="+hash+"&hd=1"
      logger.info(url)
      from servers import servertools
      listavideos = servertools.findvideos(url)
      import copy
      for video in listavideos:
          NuevoItem = copy.deepcopy(item)
          NuevoItem.url = video[1]
          NuevoItem.server = video[2]
          NuevoItem.action = "play"
          NuevoItem.folder=False
          itemlist.append(NuevoItem) 

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                return false
    
    # Comprueba si alguno de las series de "Novedades" devuelve mirrors
    portada_items = completo(mainlist_items[0])
    
    bien = False
    for portada_item in portada_items:
        episodios_items = serie(portada_item)
        if len(episodios_items)>0:
            video_item = play(episodios_items[0])
            if len(video_item)>0:
                bien = True
                break
    
    return bien
