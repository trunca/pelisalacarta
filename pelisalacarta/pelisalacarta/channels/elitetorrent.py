# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para elitetorrent
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F,S,D"
__language__ = "ES"
__title__ = "Elite Torrent"
__fanart__ = ""
__type__ = "xbmc"
__disabled__ = False
__version__ = 0
__adult__ = False
__date__ = ""
__creationdate__ = ""
__changes__ = ""
__thumbnail__ = ""
__channel__ = "elitetorrent"

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")
BASE_URL = 'http://www.elitetorrent.net'

def isGeneric():
    return True

def mainlist(item):
    logger.info("[elitetorrent.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Buscar..."      , action="search"   , url="http://www.elitetorrent.net/busqueda/%s" ))
    itemlist.append( Item(channel=__channel__, title="Docus y TV"     , action="peliculas", url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Estrenos"       , action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Películas"      , action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Peliculas HDRip", action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Peliculas MicroHD", action="peliculas", url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Peliculas VOSE" , action="peliculas", url="http://www.elitetorrent.net/categoria/14/peliculas-vose/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Series"         , action="peliculas", url="http://www.elitetorrent.net/categoria/4/series/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Series VOSE"    , action="peliculas", url="http://www.elitetorrent.net/categoria/16/series-vose/modo:mini"))

    return itemlist

def search( item, texto ):
    logger.info( "[elitetorrent.py] search" )

    item.url = item.url % (texto)

    try:
        return buscar(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
        
def buscar(item):
    logger.info("[elitetorrent.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <li>
    <a href="/torrent/27887/terminator-genesis-ts-screener"><img src="thumb_fichas/27887.jpg" border="0" title="Terminator Genesis (TS-Screener)" alt="IMG: Terminator Genesis (TS-Screener)"/></a>
    <div class="meta"><span class="voto1" title="Valoracion media">5.9</span><span class="voto2" title="Valoracion de la calidad de vídeo/audio" style="background-color:rgb(170,91,0)">3.4</span><a class="nombre" href="/torrent/27887/terminator-genesis-ts-screener" title="Terminator Genesis (TS-Screener)">Terminator Genesis (TS-Screener)</a>				
    <span class="categoria">Estrenos</span>
    <span class="fecha">Hace 4 días</span>
    </div>
    </li>
    '''
    patron =  '<a href="(/torrent/[^"]+)">'
    patron += '<img src="(thumb_fichas/[^"]+)" border="0" title="([^"]+)"[^>]+></a>'
    patron += '.*?<span class="categoria">(.*?)</span>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(BASE_URL, scrapedurl)
        thumbnail = urlparse.urljoin(BASE_URL, scrapedthumbnail)
        plot = "Categoria: " + scrapedplot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=False, viewmode="movie_with_plot") )

    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">Siguiente \&raquo\;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="buscar", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist


def peliculas(item):
    logger.info("[elitetorrent.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <li>
    <a href="/torrent/23471/mandela-microhd-720p"><img src="thumb_fichas/23471.jpg" border="0" title="Mandela (microHD - 720p)" alt="IMG: Mandela (microHD - 720p)"/></a>
    <div class="meta">
    <a class="nombre" href="/torrent/23471/mandela-microhd-720p" title="Mandela (microHD - 720p)">Mandela (microHD - 720p)</a>
    <span class="categoria">Peliculas microHD</span>
    <span class="fecha">Hace 2 sem</span>
    <span class="descrip">Título: Mandela: Del mito al hombre<br />
    '''
    patron =  '<a href="(/torrent/[^"]+)">'
    patron += '<img src="(thumb_fichas/[^"]+)" border="0" title="([^"]+)"[^>]+></a>'
    patron += '.*?<span class="descrip">(.*?)</span>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(BASE_URL, scrapedurl)
        thumbnail = urlparse.urljoin(BASE_URL, scrapedthumbnail)
        plot = re.sub('<[^<]+?>', '', scrapedplot)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=False, viewmode="movie_with_plot") )

    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">Siguiente \&raquo\;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[elitetorrent.py] play")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    #patron para .torrent
    link = scrapertools.get_match(data,'<a href="([^"]+)" class="[^"]+">Descargar el .torrent</a>')
    link = urlparse.urljoin(item.url,link)
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title="Ver en torrent (.torrent)", fulltitle=item.title , url=link , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    #patron para magnet
    link = scrapertools.get_match(data,'<a href="(magnet[^"]+)" class="enlace_torrent[^>]+>Descargar por magnet link</a>')
    link = urlparse.urljoin(item.url,link)
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title="Ver en torrent (magnet)", fulltitle=item.title , url=link , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    return itemlist
