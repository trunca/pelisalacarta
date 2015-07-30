# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para zentorrents
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F,S"
__language__ = "ES"
__title__ = "Zentorrents"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 3
__adult__ = False
__date__ = "17/05/2015"
__creationdate__ = ""
__changes__ = "Version generica"
__thumbnail__ = ""
__channel__ = "zentorrents"

import urlparse,urllib2,urllib,re
import os, sys
import HTMLParser
from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"      , action="peliculas"    , url="http://www.zentorrents.com/peliculas"))
    itemlist.append( Item(channel=__channel__, title="MicroHD"        , action="peliculas"    , url="http://www.zentorrents.com/tags/microhd"))
    itemlist.append( Item(channel=__channel__, title="HDrip"          , action="peliculas"    , url="http://www.zentorrents.com/tags/hdrip"))
    itemlist.append( Item(channel=__channel__, title="Series"         , action="peliculas"))
    itemlist.append( Item(channel=__channel__, title="Buscar..."      , action="search"       , url="http://www.zentorrents.com/buscar"))
    return itemlist

def search(item,texto):
    logger.info("search")
    itemlist = []
    
    try:
        texto = texto.replace(" ","+")
        item.url = item.url+"/buscar?searchword=%s&ordering=&searchphrase=all&limit=\d+"
        item.url = item.url % texto
        itemlist.extend(buscador(item))
        
        return itemlist
    
    except:
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscador(item):
    logger.info("buscador")
    itemlist = []
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    if "highlight" in data:
        searchword = scrapertools.get_match(data,'<span class="highlight">([^<]+)</span>')
        data = re.sub(r'<span class="highlight">[^<]+</span>',searchword,data)
        
    patron = '<div class="moditemfdb">'       # Empezamos el patrón por aquí para que no se cuele nada raro
    patron+= '<a title="([^"]+)" '                       # scrapedtitulo
    patron+= 'href="([^"]+)".*?'                         # scrapedurl
    patron+= 'src="([^"]+)".*?'                          # scrapedthumbnail
    patron+= '<p>([^<]+)</p>'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedtitulo, scrapedurl, scrapedthumbnail, scrapedplot in matches:
        scrapedurl = "http://zentorrents.com" + scrapedurl
        scrapedplot = HTMLParser.HTMLParser().unescape(scrapedplot)
        itemlist.append( Item(channel=__channel__, title=scrapedtitulo, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, fulltitle=scrapedtitulo, plot=scrapedplot, fanart="http://s6.postimg.org/4j8vdzy6p/zenwallbasic.jpg", folder=True) )
    return itemlist




def peliculas(item):
    logger.info("pelisalacarta.zentorrents peliculas")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|</p>|<p>|&amp;|amp;","",data)
    patron =  '<div class="blogitem[^>]+>'
    patron += '<a title="([^"]+)" '
    patron += 'href="([^"]+)".*?'
    patron += 'src="([^"]+)".*?'
    patron += '<div class="createdate">([^<]+)</div>'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedtitulo, scrapedurl, scrapedthumbnail, scrapedcreatedate in matches:
        scrapedurl = "http://zentorrents.com" + scrapedurl
        itemlist.append( Item(channel=__channel__, title=scrapedtitulo + " ("+scrapedcreatedate+")", url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, fanart="http://s6.postimg.org/4j8vdzy6p/zenwallbasic.jpg", folder=True) )
        
        
    # 1080,720 y seies
    patron =  '<div class="blogitem[^>]+>'
    patron += '<a href="([^"]+)".*? '
    patron += 'title="([^"]+)".*? '
    patron += 'src="([^"]+)".*?'
    patron += '<div class="createdate">([^<]+)</div>'

    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl, scrapedtitulo, scrapedthumbnail, scrapedcreatedate in matches:
        scrapedurl = "http://zentorrents.com" + scrapedurl
        itemlist.append( Item(channel=__channel__, title=scrapedtitulo + " ("+scrapedcreatedate+")", url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, fanart="http://s6.postimg.org/4j8vdzy6p/zenwallbasic.jpg", folder=True) )

    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" title="Siguiente">Siguiente</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title= "Página Siguiente >" , url=scrapedurl, fanart="http://s11.postimg.org/qu66qpjz7/zentorrentsfanart.jpg", folder=True) )
    
    return itemlist


def findvideos(item):
    logger.info("pelisalacarta.zentorrents findvideos")
    
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|</p>|<p>|&amp;|amp;","",data)
    
    patron = '<div class="descargatext">.*?'
    patron += '<img alt="([^<]+)" '
    patron += 'src="([^"]+)".*?'
    patron += 'type.*?href="([^"]+)"'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedtitulo, scrapedthumbnail, scrapedurl in matches:
      data = scrapertools.cache_page(scrapedurl)
      link = scrapertools.get_match(data,"{ window.open\('([^']+)'")
      itemlist.append( Item(channel=__channel__, title =scrapedtitulo + " (Torrent)" , thumbnail=scrapedthumbnail, url=link, server="torrent", action="play", folder=False) )
    
    
    return itemlist

def test():
    return True
    
        
