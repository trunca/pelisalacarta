# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para txibitsoft
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "S,F"
__language__ = "ES"
__title__ = "Txibitsoft (Torrent)"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 2
__adult__ = False
__date__ = "08/04/2015"
__creationdate__ = ""
__changes__ = "Version sencilla"
__thumbnail__ = "http://s27.postimg.org/hx5ohryxf/tblogo.jpg"
__channel__ = "txibitsoft"


import urlparse,urllib2,urllib,re
import os, sys
from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

host = "http://www.txibitsoft.com/"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.txibitsoft mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Peliculas"  , action="peliculas"           , url="http://www.txibitsoft.com/torrents.php?procesar=1&categorias='Peliculas'&pagina=1", thumbnail="http://s27.postimg.org/nbbeles4j/tbpelithu.jpg", fanart="http://s14.postimg.org/743jqty35/tbpelifan.jpg"))
    itemlist.append( Item(channel=__channel__, title="1080"       , action="peliculas"           , url="http://www.txibitsoft.com/torrents.php?procesar=1&categorias='Cine%20Alta%20Definicion%20HD'&subcategoria=1080p&pagina=1", thumbnail="http://s4.postimg.org/t4i9vgjgd/tb1080th.jpg", fanart="http://s17.postimg.org/7z5pnf5tb/tb1080fan.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series"     , action="peliculas"           , url="http://www.txibitsoft.com/torrents.php?procesar=1&categorias='Series'&pagina=1", thumbnail="http://s12.postimg.org/4ao5ekygd/tbseriethu.jpg", fanart="http://s12.postimg.org/oymstbjot/tbseriefan.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscador"   , action="search"               , url="", fanart="http://s1.postimg.org/f5mnv2pcf/tbbusfan.jpg", thumbnail="http://s28.postimg.org/r2911z0rx/tbbusthu.png"))

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.txibitsoft search")
    texto = texto.replace(" ","+")
    
    item.url = "http://www.txibitsoft.com/torrents.php?procesar=1&texto=%s" % (texto)
    try:
        return buscador(item)
    # Se captura la excepciÛn, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("pelisalacarta.txibitsoft buscador")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    data = data.replace("&amp;","&")
    # corrige la falta de imagen
    data = re.sub(r'<img src="<!doctype html><html xmlns="','</div><img src="http://s30.postimg.org/8n4ej5j0x/noimage.jpg" texto ><p>',data)
    patron =  '<dl class=".*?dosColumnasDobles"><dt>'
    patron += '<a href="([^"]+)" '
    patron += 'title.*?:([^\["]+)([^"]*)".*?'
    patron += '<img src="([^"]+)".*?'
    patron += 'Idioma: <span class="categoria">([^<]+).*?'
    patron += 'Tama&ntilde;o: <span class="categoria">([^<]+)'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl, scrapedtitle,scrapedplot, scrapedthumbnail, scrapedlenguage, scrapedsize in matches:
        scrapedurl = "http://www.txibitsoft.com" + scrapedurl
        scrapedplot += " Tamaño: " + scrapedsize
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, plot=scrapedplot, url=scrapedurl, action="play", thumbnail=scrapedthumbnail, folder=True) )
    
    #Paginador
    patron = '<ul class="paginacion">(?:.*?)<li>[0-9]+</li><li><a title="[^"]+" href="([^"]+)">([0-9]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)  
    if len(matches) >0:
      scrapedurl = urlparse.urljoin(item.url,matches[0][0])
      
      itemlist.append( Item(channel=__channel__, action="peliculas", title="Página Siguiente " + matches[0][1], url=scrapedurl , thumbnail="" , folder=True) )

    
    return itemlist

def play(item):
    logger.info("pelisalacarta.txibitsoft findvideos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    patron = '<form name="frm" id="frm" method="get" action="torrent.php">.*?'
    patron += 'alt="([^<]+)".*?'
    patron += '<p class="limpiar centro"><a class="torrent" href="([^"]+)"'
    
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedtitle, scrapedurl in matches:
      scrapedurl = "http://www.txibitsoft.com" + scrapedurl
      itemlist.append( Item(channel=__channel__, title=item.title, url=scrapedurl, action="play", server="torrent", thumbnail=item.thumbnail, folder=False) ) 
    return itemlist
    
def test():
    return True
















