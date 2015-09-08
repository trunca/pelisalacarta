# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newpct1
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F,S,A"
__language__ = "EN"
__title__ = "KickassTorrents"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 1
__adult__ = False
__date__ = "27/08/15"
__creationdate__ = "27/08/2015"
__changes__ = ""
__thumbnail__ = "http://i.ytimg.com/vi/GNEERk4qbBc/maxresdefault.jpg"
__channel__ = "kickasstorrents"


import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
import json

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[kickasstorrents.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Peliculas"          , action="peliculas", url="https://kat.cr/movies/"))
    itemlist.append( Item(channel=__channel__, title="Series"             , action="peliculas", url="https://kat.cr/tv/"))
    itemlist.append( Item(channel=__channel__, title="Buscar Peliculas"   , action="search"    , url="https://kat.cr/usearch/%s category:movies/" ))
    itemlist.append( Item(channel=__channel__, title="Buscar Series"      , action="search"    , url="https://kat.cr/usearch/%s category:tv/" ))
    
    return itemlist

def search(item,texto):
    item.url = item.url %(texto)
    logger.info("[kickasstorrents.py] "+item.url+" search")
    itemlist = []
    try:
        
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []


def peliculas(item):
  itemlist = [] 
  data = scrapertools.cachePage(item.url)
  
  items = scrapertools.get_match(data,'<th class="width100perc nopad">torrent name</th>(.*?)</table>')
  patron  = '<div class="iaconbox center floatright">.*?<a data-nop title="Torrent magnet link" href="([^"]+)".*?<a data-download title="Download torrent file" href="([^"]+)".*?<a href="([^"]+)" class="cellMainLink">(.*?)</a>.*?<td class="nobr center">(.*?)</span></td>'
  matches = re.compile(patron,re.DOTALL).findall(items)
  logger.info(items)
  for magnet, torrent, url, title, size in matches:
      url = urlparse.urljoin(item.url,url)
      title = title.replace('<strong class="red">','').replace('</strong>','')
      itemlist.append( Item(channel=__channel__, action="pelicula", server="torrent", title=title, url=url, thumbnail="", plot="", folder=False) )  
      
  #Paginador
  matches = re.compile('<a class="turnoverButton siteButton bigButton active">[0-9]+</a><a rel="nofollow" href="([^"]+)"',re.DOTALL).findall(data)  
  if len(matches):
    url = urlparse.urljoin(item.url,matches[0])
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Página Siguiente >>" , url=url, folder=True) )

  return itemlist

def pelicula(item):
  itemlist = [] 
  data = scrapertools.cachePage(item.url)

  if "<li><strong>Episode title:</strong>" in data:
    show = scrapertools.get_match(data,'<li><a href="[^"]+">View all <strong>([^<]+)</strong> episodes</a></li>')
    episode_title = scrapertools.get_match(data,'<li><strong>Episode title:</strong>([^<]+)</li>').strip()
    episodio = scrapertools.get_match(data,'<li><strong>Episode:</strong>([^<]+)</li>').strip()
    c,e = episodio = scrapertools.get_match(episodio,'S([0-9]+)E([0-9]+)')
    title = show + " " + c + "x" + e + " " + episode_title
    quality = ""
  else:
    title = scrapertools.get_match(data,'<li><strong>Movie:</strong> <a href="[^"]+"><span>([^<]+)</span></a></li>')
    quality = scrapertools.get_match(data,'<li><strong>Detected quality:</strong> <span id="[^"]+">([^<]+)</span></li>')
  thumbnail = scrapertools.get_match(data,'<a class="movieCover" href="[^"]+"><img src="([^"]+)" /></a>')
  url = scrapertools.get_match(data,'<a class="movieCover" href="([^"]+)"><img src="[^"]+" /></a>')
  url = urlparse.urljoin(item.url,url)
  plot = scrapertools.get_match(data,'<div id="summary">.*?<div>(.*?)<br />').strip()
  seeders = scrapertools.get_match(data,'<div class="seedBlock"><span class="seedLeachIcon"></span>seeders: <strong>([^<]+)</strong></div>')
  leechers = scrapertools.get_match(data,'<div class="leechBlock"><span class="seedLeachIcon"></span>leechers: <strong>([^<]+)</strong></div>')
  size = scrapertools.get_match(data,'<div class="widgetSize"><span class="torType filmType"></span> <strong>([^<]+)<span>([^<]+)</span></strong></div>')
  torrent = scrapertools.get_match(data,'<a class="siteButton giantButton" href="([^"]+)">')
  torrent =  urlparse.urljoin(item.url,torrent)
  
  fulltitle = title                                    
  if quality:
    fulltitle += " [COLOR green](" + quality + ")[/COLOR]"
  fulltitle += " [COLOR skyblue](" + size[0] + size[1] + ")[/COLOR]"
  fulltitle += " [COLOR orange](L: " + leechers + " S: " + seeders + ")[/COLOR]"
			
  itemlist.append( Item(channel=__channel__, action="play", fulltitle=fulltitle, server="torrent", title=title, url=torrent, thumbnail=thumbnail, plot=plot, folder=False) )  
  return itemlist


def bbcode_kodi2html(text):
    if config.get_platform().startswith("plex") or config.get_platform().startswith("mediaserver"):
        import re
        text = re.sub(r'\[COLOR\s([^\]]+)\]',
                      r'<span style="color: \1">',
                      text)
        text = text.replace('[/COLOR]','</span>')
        text = text.replace('[CR]','<br>')
        text = re.sub(r'\[([^\]]+)\]',
                      r'<\1>',
                      text)
        text = text.replace('"color: white"','"color: auto"')

    return text