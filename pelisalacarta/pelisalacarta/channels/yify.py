# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newpct1
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F"
__language__ = "EN"
__title__ = "YIFY"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 1
__adult__ = False
__date__ = "07/08/15"
__creationdate__ = "07/08/2015"
__changes__ = ""
__thumbnail__ = "https://s.ynet.io/assets/images/website/logo-YTS.svg"
__channel__ = "yify"


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
    logger.info("[yify.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Peliculas"          , action="peliculas"))
    itemlist.append( Item(channel=__channel__, title="Por Calidad"        , action="calidad"))
    itemlist.append( Item(channel=__channel__, title="Por Genero"         , action="genero"))
    itemlist.append( Item(channel=__channel__, title="Por Puntuacion"     , action="puntuacion"))
    itemlist.append( Item(channel=__channel__, title="Buscar..."          , action="search"    , url="https://yts.to/api/v2/list_movies.json?query_term=%s" ))
    
    return itemlist
    
def peliculas(item):
  itemlist = []
  api_url="https://yts.to/api/v2/list_movies.json"
  if item.url: api_url=item.url
  
  data = scrapertools.cachePage(api_url)
  try:
    JsonResponse = json.loads(data)
    open("c:\\asd.json","w").write(json.dumps(JsonResponse, indent=4, sort_keys=True))  
  except:
    return []
    
  if JsonResponse["status"] == "ok":
    for Movie in JsonResponse["data"]["movies"]:
      Calidades = []
      for Torrent in Movie["torrents"]:
        Calidades.append(Torrent["quality"].encode("utf8"))
        
      title = Movie["title"].encode("utf8") 
      fulltitle = title + " [COLOR green](" + " | ".join(Calidades) + ")[/COLOR]"
      url = Movie["id"]
      thumbnail = Movie["medium_cover_image"].encode("utf8")
      categorias = ", ".join(Movie["genres"]).encode("utf8")
      plot= "Año: [COLOR orange][B]" + str(Movie["year"]) + "[/B][/COLOR] Rating: [COLOR orange][B]" + str(Movie["rating"]) + "[/B][/COLOR] Categorias: [COLOR orange][B]" + categorias + "[/B][/COLOR]"
      plot = bbcode_kodi2html(plot)
      title = bbcode_kodi2html(title)
      itemlist.append( Item(channel=__channel__, action="findvideos", title=title, fulltitle=fulltitle, url=url, thumbnail=thumbnail, plot=plot, folder=True) )  
  
  return itemlist
  
def findvideos(item):
  itemlist = []
  api_url="https://yts.to/api/v2/movie_details.json?movie_id=%s&with_images=%s&with_cast=%s" % (item.url, False, False)
  data = scrapertools.cachePage(api_url)
  try:
    JsonResponse = json.loads(data)
  except:
    return []
    
  if JsonResponse["status"] == "ok":
      Movie = JsonResponse["data"]     
      thumbnail = item.thumbnail
      plot = Movie["description_full"].encode("utf8")
      for Torrent in Movie["torrents"]:
        url = Torrent["url"].encode("utf8")
        fulltitle = item.title + " [COLOR green](" + Torrent["quality"].encode("utf8") + ")[/COLOR] [COLOR skyblue](" + Torrent["size"].encode("utf8") + ")[/COLOR] "
        fulltitle += " [COLOR orange](P: " + str(Torrent["peers"]) + " S: " + str(Torrent["seeds"]) + ")[/COLOR]"
        itemlist.append( Item(channel=__channel__, server="torrent", action="play", title=fulltitle, fulltitle=item.title, url=url, thumbnail=thumbnail, plot=plot, folder=True) )  
  
  return itemlist
    
def search(item,texto):
    logger.info("[yify.py] search:" + texto)
    item.url = item.url % texto

    try:
        return peliculas(item)
	# Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
        
def calidad(item):
    logger.info("[yify.py] calidad")
    itemlist = []
    for x in ["720p", "1080p", "3D"]:
        api_url="https://yts.to/api/v2/list_movies.json?quality="+ x
        itemlist.append( Item(channel=__channel__, action="peliculas", title=x , url=api_url , folder=True))
    return itemlist

def genero(item):
    logger.info("[yify.py] genero")
    itemlist = []
    for x in ["Action" , "Adventure" , "Animation" , "Biography" , "Comedy" , "Crime" , "Documentary" , "Drama" , "Family" , "Fantasy" , "Film-Noir" , "History" , "Horror" , "Music" , "Musical" , "Mystery" , "News" , "Romance" , "Sci-Fi" , "Short" , "Sport" , "Thriller" , "War" , "Western"]:
        api_url="https://yts.to/api/v2/list_movies.json?genre="+ x
        itemlist.append( Item(channel=__channel__, action="peliculas", title=x , url=api_url , folder=True))
    return itemlist

def puntuacion(item):
    logger.info("[yify.py] puntuacion")
    itemlist = []
    for x in range(0,10):
        api_url="https://yts.to/api/v2/list_movies.json?minimum_rating="+ str(x)
        itemlist.append( Item(channel=__channel__, action="peliculas", title=str(x)+"+" , url=api_url , folder=True))
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