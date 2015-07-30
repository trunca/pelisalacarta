# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelispekes
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F"
__language__ = "ES"
__title__ = "PelisPekes"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 5
__adult__ = False
__date__ = "08/06/2015"
__creationdate__ = "24/08/2013"
__changes__ = "Actualizado"
__thumbnail__ = ""
__channel__ = "pelispekes"

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[pelispekes.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=__channel__ , action="novedades"  , title="Novedades"          , url="http://pelispekes.com/"))
    itemlist.append( Item(channel=__channel__ , action="categorias" , title="Categorias"         , url="http://pelispekes.com/"))
    itemlist.append( Item(channel=__channel__, action="search"      , title="Buscar"             , url="http://pelispekes.com/?s="))

    return itemlist

def search(item,texto):
    logger.info("[pelispekes.py] search")
    texto = texto.replace(" ", "+")
    item.url = item.url + texto
    return buscar(item)
    
    
def novedades(item):
    logger.info("[pelispekes.py] novedades")
    itemlist = []

    # Extrae las entradas (carpetas)
    data = scrapertools.cachePage(item.url)
    patron = '<div class="poster-media-card">\n<a href="([^"]+)" title="([^"]+)">\n<div class="poster">\n<div class="title">\n<span class="under-title">([^<]+)</span>.*?<img width="300" height="428" src="([^"]+)" title="[^"]+" alt="[^"]+"/>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle, scrapedyear, scrapedthumbnail in matches:
        scrapedurl = unicode(scrapedurl, "utf8", errors="replace").encode("utf8")
        scrapedtitle = unicode(scrapedtitle, "utf8", errors="replace").encode("utf8")
        scrapedyear = unicode(scrapedyear, "utf8", errors="replace").encode("utf8")
        scrapedthumbnail = unicode(scrapedthumbnail, "utf8", errors="replace").encode("utf8")
        scrapedplot = ""
        itemlist.append( Item(channel=item.channel , action="findvideos" , title=scrapedtitle + " ("+scrapedyear+")" , url=scrapedurl , thumbnail=scrapedthumbnail, fanart=scrapedthumbnail, plot=scrapedplot , viewmode="movie_with_plot"))
    
    # Extrae la pagina siguiente
    patron  = '<a href="([^"]+)"><i class="glyphicon glyphicon-chevron-right" aria-hidden="true">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if matches:
        itemlist.append( Item(channel=item.channel , action="novedades"   , title="Pagina Siguiente >>" , url=matches[0] ))

    return itemlist
    
def buscar(item):
    logger.info("[pelispekes.py] buscar")
    itemlist = []

    # Extrae las entradas (carpetas)
    data = scrapertools.cachePage(item.url)
    patron = '<img src="([^"]+)".*?<div class="col-xs-10">\n<a href="([^"]+)" title="([^"]+)">.*?<p class="main-info-list">Película de ([^<]+)</p>\n<p class="text-list">([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for  scrapedthumbnail, scrapedurl, scrapedtitle, scrapedyear, scrapedplot in matches:
        scrapedurl = unicode(scrapedurl, "utf8", errors="replace").encode("utf8")
        scrapedtitle = unicode(scrapedtitle, "utf8", errors="replace").encode("utf8")
        scrapedyear = unicode(scrapedyear, "utf8", errors="replace").encode("utf8")
        scrapedthumbnail = unicode(scrapedthumbnail, "utf8", errors="replace").encode("utf8")
        scrapedplot = unicode(scrapedplot, "utf8", errors="replace").encode("utf8")
        itemlist.append( Item(channel=item.channel , action="findvideos"   , title=scrapedtitle + " ("+scrapedyear+")" , url=scrapedurl , thumbnail=scrapedthumbnail, fanart=scrapedthumbnail, plot=scrapedplot , viewmode="movie_with_plot"))
    
    # Extrae la pagina siguiente
    patron  = '<a href="([^"]+)"><i class="glyphicon glyphicon-chevron-right" aria-hidden="true">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if matches:
        itemlist.append( Item(channel=item.channel , action="novedades"   , title="Pagina Siguiente >>" , url=matches[0] ))

    return itemlist

def categorias(item):
    logger.info("[pelispekes.py] categorias")

    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<li class="cat-item cat-item-15">(.*?)</aside> </div>')
    # Extrae las entradas (carpetas)
   
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    for scrapedurl, scrapedtitle in matches:
        scrapedurl = scrapedurl.decode("iso-8859-1").encode("utf8")
        scrapedtitle = scrapedtitle.decode("iso-8859-1").encode("utf8")
        itemlist.append( Item(channel=item.channel , action="novedades" , title=scrapedtitle , url=scrapedurl))

    return itemlist
    
def findvideos(item):
    data = scrapertools.cachePage(item.url)
    from servers import servertools 
    import copy    
    itemlist = []
    patronvideos  = '</div>\n<div class="tab-pane reproductor repron" id="([^"]+)">\n<div class="calishow">([^<]+)</div>\n'
    patronvideos += '<iframe[^>]+src="([^"]+)"[^>]+></iframe>\n'
    patronvideos += '<div class="clear"></div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for id, server, url in matches:
      print id
      patroncalidad = '<a href="#'+id+'" data-toggle="tab" alt="[^"]+" title="[^"]+">\n<span class="[^"]+" style="margin-right:5px"></span>\n([^\n]+)\n</a>'
      calidad = re.compile(patroncalidad,re.DOTALL).findall(data)
      print calidad
      if server == "netu":
        url = "http://netu.tv/watch_video.php?v="+ url.split("=")[1]
        listavideos = servertools.findvideos(url)
      else:
        listavideos = servertools.findvideos(url)
        
      for video in listavideos:
          NuevoItem = copy.deepcopy(item)
          NuevoItem.title = "Ver en: ["  + video[2] + "]" + " ("+calidad[0] + ")"
          NuevoItem.url = video[1]
          NuevoItem.server = video[2]
          NuevoItem.action = "play"
          NuevoItem.folder=False
          itemlist.append(NuevoItem) 
    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = novedades(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien