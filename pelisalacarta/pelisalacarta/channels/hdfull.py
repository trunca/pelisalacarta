# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para hdfull
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal
__category__ = "F,S"
__language__ = "ES"
__title__ = "HDFull"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 0
__adult__ = False
__date__ = ""
__creationdate__ = ""
__changes__ = ""
__thumbnail__ = ""
__channel__ = "hdfull"


import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from servers import servertools
import HTMLParser

host = "http://hdfull.tv"

account = ( config.get_setting("hdfullaccount") == "true" )

def isGeneric():
    return True

def openconfig(item):
    config.open_settings( )
    return []

def login():
    logger.info("pelisalacarta.channels.hdfull login")
    data = agrupa_datos( scrapertools.cache_page(host) )
    
    patron = "<input type='hidden' name='__csrf_magic' value=\"([^\"]+)\" />"
    sid = scrapertools.find_single_match(data, patron)

    post = urllib.urlencode({'__csrf_magic':sid})+"&username="+config.get_setting('hdfulluser')+"&password="+config.get_setting('hdfullpassword')+"&action=login"
    data = scrapertools.cache_page(host,post=post)

def mainlist(item):
    logger.info("pelisalacarta.channels.hdfull mainlist")
    itemlist = []

    if not account:
        itemlist.append( Item( channel=__channel__ , title=bbcode_kodi2html("[COLOR orange][B]Habilita tu cuenta para activar los items de usuario...[/B][/COLOR]"), action="openconfig", url="", folder=False ) )
    else:
        login()

    itemlist.append( Item( channel=__channel__, action="menupeliculas", title="Películas", url=host, folder=True ) )
    itemlist.append( Item( channel=__channel__, action="menuseries", title="Series", url=host, folder=True ) )
    itemlist.append( Item( channel=__channel__, action="search", title="Buscar..." ) )

    return itemlist

def menupeliculas(item):
    logger.info("pelisalacarta.channels.hdfull menupeliculas")
    itemlist = []

    if account:
        itemlist.append( Item( channel=__channel__, action="menumispeliculas", title=bbcode_kodi2html("[COLOR orange][B]Mis Peliculas[/B][/COLOR]"), folder=True ) )
    itemlist.append( Item( channel=__channel__, action="fichas", title="ABC", url=host+"/peliculas/abc", folder=True ) )
    itemlist.append( Item( channel=__channel__, action="fichas", title="Últimas películas" , url=host+"/peliculas", folder=True ) )
    itemlist.append( Item( channel=__channel__, action="fichas", title="Películas Estreno", url=host+"/peliculas-estreno", folder=True ) )
    itemlist.append( Item( channel=__channel__, action="fichas", title="Películas Actualizadas", url=host+"/peliculas-actualizadas", folder=True ) )
    itemlist.append( Item( channel=__channel__, action="fichas", title="Rating IMDB", url=host+"/peliculas/imdb_rating", folder=True ) )
    itemlist.append( Item( channel=__channel__, action="generos", title="Películas por Género", url=host, folder=True))

    return itemlist
    
def menumispeliculas(item):
    itemlist = []
    itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Favoritos[/B][/COLOR]"), url=host+"/a/my?target=movies&action=favorite&start=-28&limit=28", folder=True ) )
    itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Vistas[/B][/COLOR]"), url=host+"/a/my?target=movies&action=seen&start=-28&limit=28", folder=True ) )
    itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Pendientes[/B][/COLOR]"), url=host+"/a/my?target=movies&action=pending&start=-28&limit=28", folder=True ) )
    #itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Recomendadas[/B][/COLOR]"), url=host+"/a/my?target=movies&action=recomended&start=-28&limit=28", folder=True ) )
    return itemlist

def menumisseries(item):
    itemlist = []
    itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Para Ver[/B][/COLOR]"), url=host+"/a/my?target=shows&action=watch&start=-28&limit=28", folder=True ) )
    itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Siguiendo[/B][/COLOR]"), url=host+"/a/my?target=shows&action=following&start=-28&limit=28", folder=True ) )
    itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Favoritos[/B][/COLOR]"), url=host+"/a/my?target=shows&action=favorite&start=-28&limit=28", folder=True ) )
    #itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Pendientes[/B][/COLOR]"), url=host+"/a/my?target=shows&action=pending&start=-28&limit=28", folder=True ) )
    #itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Recomendadas[/B][/COLOR]"), url=host+"/a/my?target=shows&action=recomended&start=-28&limit=28", folder=True ) )
    #itemlist.append( Item( channel=__channel__, action="items_usuario", title=bbcode_kodi2html("[COLOR orange][B]Finalizadas[/B][/COLOR]"), url=host+"/a/my?target=shows&action=seen&start=-28&limit=28", folder=True ) )

    return itemlist

def menuseries(item):
    logger.info("pelisalacarta.channels.hdfull menuseries")
    itemlist = []

    if account:
        itemlist.append( Item( channel=__channel__, action="menumisseries", title=bbcode_kodi2html("[COLOR orange][B]Mis Series[/B][/COLOR]"), folder=True ) )

    itemlist.append( Item( channel=__channel__, action="series_abc", title="A-Z", folder=True ) )
    itemlist.append( Item(channel=__channel__, action="novedades_episodios", title="Últimos Emitidos", url=host+"/a/episodes?action=latest&start=-24&limit=24&elang=ALL", folder=True ) )
    itemlist.append( Item(channel=__channel__, action="novedades_episodios", title="Episodios Estreno", url=host+"/a/episodes?action=premiere&start=-24&limit=24&elang=ALL", folder=True ) )
    itemlist.append( Item(channel=__channel__, action="novedades_episodios", title="Episodios Actualizados", url=host+"/a/episodes?action=updated&start=-24&limit=24&elang=ALL", folder=True ) )
    itemlist.append( Item(channel=__channel__, action="fichas", title="Últimas series", url=host+"/series", folder=True ) )
    itemlist.append( Item(channel=__channel__, action="fichas", title="Rating IMDB", url=host+"/series/imdb_rating", folder=True ) )
    itemlist.append( Item(channel=__channel__, action="generos_series", title="Series por Género", url=host, folder=True ) )
    itemlist.append( Item( channel=__channel__, action="listado_series", title="Listado de todas las series", url=host+"/series/list", folder=True ) )

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.hdfull search")
    data = agrupa_datos(scrapertools.cache_page(host))
    texto = texto.replace('+','%20')
    sid = scrapertools.get_match(data, '.__csrf_magic. value="(sid:[^"]+)"')
    item.extra = urllib.urlencode({'__csrf_magic':sid})+'&menu=search&query='+texto
    item.url = host+"/buscar"
    try:
        return fichas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def series_abc(item):
    logger.info("pelisalacarta.channels.hdfull series_abc")
    itemlist=[]

    az = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#"

    for l in az:
        itemlist.append( Item( channel=item.channel, action='fichas', title=l, url=host+"/series/abc/"+l.replace('#' ,'9') ))

    return itemlist

def items_usuario(item):
    logger.info("pelisalacarta.channels.hdfull menupeliculas")

    itemlist = []

    ## Carga estados
    status = jsontools.load_json(scrapertools.cache_page(host+'/a/status/all'))

    ## Fichas usuario
    url = item.url.split("?")[0]
    post = item.url.split("?")[1]

    old_start = scrapertools.get_match(post, 'start=([^&]+)&')
    limit = scrapertools.get_match(post, 'limit=(\d+)')
    target = scrapertools.get_match(post, 'target=([^&]+)')
    start = "%s" % ( int(old_start) + int(limit) )

    post = post.replace("start="+old_start, "start="+start)
    next_page = url + "?" + post

    ## Carga las fichas de usuario
    data = scrapertools.cache_page(url, post=post)
    fichas_usuario = jsontools.load_json( data )

    for ficha in fichas_usuario:
        if "es" in ficha['title']:
          title = ficha['title']['es'].strip().decode("utf8").encode("utf8")
        else:
          title = ficha['title']['en'].strip().decode("utf8").encode("utf8")

        show = title
        
        if "thumbnail" in ficha:
          thumbnail = host+"/thumbs/" + ficha['thumbnail'].decode("utf8").encode("utf8")
        else:
          thumbnail = host+"/thumbs/" + ficha['thumb'].decode("utf8").encode("utf8")
          
        if target == "shows":
            url = urlparse.urljoin( host, '/serie/'+ ficha['permalink'].decode("utf8").encode("utf8") ) + "###" + ficha['id'].decode("utf8").encode("utf8") + ",1"
            action = "episodios"
            estado = get_status(status, 'shows', ficha['id'].decode("utf8").encode("utf8"))
            if "show_title" in ficha:
                action = "findvideos"
                if "es" in ficha['show_title']:
                  serie = ficha['show_title']['es'].strip().decode("utf8").encode("utf8")
                else:
                  serie = ficha['show_title']['en'].strip().decode("utf8").encode("utf8")
                  
                temporada = ficha['season'].decode("utf8").encode("utf8")
                episodio = ficha['episode'].decode("utf8").encode("utf8").zfill(2) 
                serie = bbcode_kodi2html("[COLOR whitesmoke][B]" + serie + "[/B][/COLOR]")
                title = temporada + "x" + episodio + " - " + serie + ": " + title
                url = urlparse.urljoin( host, '/serie/' + ficha['permalink'].decode("utf8").encode("utf8") + '/temporada-' + temporada +'/episodio-' + episodio ) + "###" + ficha['id'].decode("utf8").encode("utf8") + ",3"
                
        elif target == "movies":
            url = urlparse.urljoin( host, '/pelicula/'+ ficha['perma'].decode("utf8").encode("utf8") ) + "###" + ficha['id'].decode("utf8").encode("utf8") + ",2"
            action = "findvideos"
            estado = get_status(status, 'movies', ficha['id'].decode("utf8").encode("utf8"))
        fulltitle = title
        if estado: fulltitle += estado

        itemlist.append( Item( channel=__channel__, action=action, title=title, fulltitle=fulltitle, url=url, thumbnail=thumbnail, show=show, folder=True ) )

    if len(itemlist) == int(limit):
        itemlist.append( Item( channel=__channel__, action="items_usuario", title=">> Página siguiente", url=next_page, folder=True ) )

    return itemlist

def listado_series(item):
    logger.info("pelisalacarta.channels.hdfull listado_series")
    itemlist = []

    data = agrupa_datos( scrapertools.cache_page(item.url) )

    patron = '<div class="list-item"><a href="([^"]+)"[^>]+>([^<]+)</a></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        url = scrapedurl + "###0,1"
        itemlist.append( Item( channel=__channel__, action="episodios", title=scrapedtitle, fulltitle=scrapedtitle, url=url, show=scrapedtitle ) )

    return itemlist

def fichas(item):
    logger.info("pelisalacarta.channels.hdfull series")
    itemlist = []

    ## Carga estados
    status = jsontools.load_json(scrapertools.cache_page(host+'/a/status/all'))

    if item.action == "search":
        data = agrupa_datos( scrapertools.cache_page(item.url,post=item.extra) )
        s_p = scrapertools.get_match(data, '<h3 class="section-title">(.*?)<div id="footer-wrapper">').split('<h3 class="section-title">')
        if len(s_p) == 1:
            data = s_p[0]
            if 'Lo sentimos</h3>' in s_p[0]:
                return []
        else:
            data = s_p[0]+s_p[1]
    else:
        data = agrupa_datos( scrapertools.cache_page(item.url) )

    data = re.sub(
        r'<div class="span-6[^<]+<div class="item"[^<]+' + \
         '<a href="([^"]+)"[^<]+' + \
         '<img.*?src="([^"]+)".*?' + \
         '<div class="left"(.*?)</div>' + \
         '<div class="right"(.*?)</div>.*?' + \
         'title="([^"]+)".*?' + \
         'onclick="setFavorite.\d, (\d+),',
         r"'url':'\1';'image':'\2';'langs':'\3';'rating':'\4';'title':\5;'id':'\6';",
        data
    )

    patron  = "'url':'([^']+)';'image':'([^']+)';'langs':'([^']+)';'rating':'([^']+)';'title':([^;]+);'id':'([^']+)';"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedlangs, scrapedrating, scrapedtitle, scrapedid in matches:

        thumbnail = scrapedthumbnail.replace("/tthumb/130x190/","/thumbs/")
        plot= ""
        title = scrapedtitle.strip()
        show = title

        if scrapedlangs != ">":
            textoidiomas = extrae_idiomas(scrapedlangs)
            
            plot+= "Idiomas: " + bbcode_kodi2html("[COLOR orange][B]" + textoidiomas + "[/B][/COLOR] ") 

        if scrapedrating != ">":
            valoracion = re.sub(r'><[^>]+>(\d+)<b class="dec">(\d+)</b>', r'\1,\2', scrapedrating)
            plot+= "Puntuación: " + bbcode_kodi2html("[COLOR orange][B]" + valoracion + "[/B][/COLOR] ")

        url = urlparse.urljoin(item.url, scrapedurl)

        if "/serie" in url or "/tags-tv" in url:
            action = "episodios"
            url+=  "###" + scrapedid + ",1"
            type = "shows"
        else:
            action = "findvideos"
            url+=  "###" + scrapedid + ",2"
            type = "movies"

        estado = get_status(status, type, scrapedid)
        fulltitle = title
        if estado: fulltitle += estado

        if item.action == "search":
            tag_type = scrapertools.get_match(url,'l.tv/([^/]+)/')
            plot = "Tipo: " +bbcode_kodi2html("[COLOR orange][B]" + tag_type.capitalize() + "[/B][/COLOR] ") + plot

        itemlist.append( Item( channel=__channel__, action=action, title=title, plot=plot, url=url, fulltitle=fulltitle, thumbnail=thumbnail, show=show, folder=True ) )

    ## Paginación
    next_page_url = scrapertools.find_single_match(data,'<a href="([^"]+)">.raquo;</a>')
    if next_page_url!="":
        itemlist.append( Item( channel=__channel__, action="fichas", title=">> Página siguiente", url=urlparse.urljoin(item.url,next_page_url), folder=True ) )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.hdfull episodios")
    itemlist = []

    ## Carga estados
    status = jsontools.load_json(scrapertools.cache_page(host+'/a/status/all'))

    url_targets = item.url

    if "###" in item.url:
        id = item.url.split("###")[1].split(",")[0]
        type = item.url.split("###")[1].split(",")[1]
        item.url = item.url.split("###")[0]

    ## Temporadas
    data = agrupa_datos( scrapertools.cache_page(item.url) )

    if id == "0":
        ## Se saca el id de la serie de la página cuando viene de listado_series
        id = scrapertools.get_match(data, "<script>var sid = '([^']+)';</script>")
        url_targets = url_targets.replace('###0','###' + id)

    
    if account:
        estado = get_status(status, "shows", id)
        if "Siguiendo" in estado: title = bbcode_kodi2html("([COLOR red][B]Abandonar[/B][/COLOR])")
        else: title = bbcode_kodi2html("([COLOR orange][B]Seguir[/B][/COLOR])")
        itemlist.append( Item( channel=__channel__, action="set_status", title=title, fulltitle=title, url=url_targets, thumbnail=item.thumbnail, show=item.show, folder=True ) )
        
        if "Favorito" in estado: title = bbcode_kodi2html("([COLOR red][B]Quitar de Favoritos[/B][/COLOR])")
        else: title = bbcode_kodi2html("([COLOR orange][B]Agregar a Favoritos[/B][/COLOR])")
        itemlist.append( Item( channel=__channel__, action="set_status", title=title, fulltitle=title, url=url_targets, thumbnail=item.thumbnail, show=item.show, folder=True ) )

    patron  = "<li><a href='([^']+)'>[^<]+</a></li>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl in matches:

        ## Episodios
        data = agrupa_datos( scrapertools.cache_page(scrapedurl) )

        sid = scrapertools.get_match(data,"<script>var sid = '(\d+)'")
        ssid = scrapertools.get_match(scrapedurl,"temporada-(\d+)")
        post = "action=season&start=0&limit=0&show=%s&season=%s" % (sid, ssid)

        url = host+"/a/episodes"

        data = scrapertools.cache_page(url,post=post)

        episodes = jsontools.load_json( data )

        for episode in episodes:

            thumbnail = host+"/thumbs/" + episode['thumbnail'].decode("utf8").encode("utf8")

            temporada = episode['season'].decode("utf8").encode("utf8")
            episodio = episode['episode'].decode("utf8").encode("utf8").zfill(2)
            plot=""
            if episode['languages'] != "[]":
                idiomas = "[COLOR orange][B]" + "/".join(episode['languages']).decode("utf8").encode("utf8") + "[/B][/COLOR]"
                idiomas = bbcode_kodi2html(idiomas)
            else: idiomas = ""

            if episode['title']:
                if "es" in episode['title']:
                  title = episode['title']['es'].strip().decode("utf8").encode("utf8")
                else:
                  title = episode['title']['en'].strip().decode("utf8").encode("utf8")


            if len(title) == 0: title = "Temporada " + temporada + " Episodio " + episodio

            title = temporada + "x" + episodio + " - " + title
            plot+= "Idiomas: " + bbcode_kodi2html("[COLOR orange][B]" + idiomas + "[/B][/COLOR] ") 

            estado = get_status(status, 'episodes', episode['id'].decode("utf8").encode("utf8"))
            fulltitle = title
            if estado: fulltitle += estado

            url = urlparse.urljoin( scrapedurl, 'temporada-' + temporada +'/episodio-' + episodio ) + "###" + episode['id'] + ",3"

            itemlist.append( Item( channel=__channel__, action="findvideos", title=title,plot=plot, fulltitle=fulltitle, url=url, thumbnail=thumbnail, show=item.show, folder=True ) )

    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
        itemlist.append( Item( channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show ) )
        itemlist.append( Item( channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=item.show ) )

    return itemlist

def novedades_episodios(item):
    logger.info("pelisalacarta.channels.hdfull novedades_episodios")
    itemlist = []

    ## Carga estados
    status = jsontools.load_json(scrapertools.cache_page(host+'/a/status/all'))

    ## Episodios
    url = item.url.split("?")[0]
    post = item.url.split("?")[1]

    old_start = scrapertools.get_match(post, 'start=([^&]+)&')
    start = "%s" % ( int(old_start) + 24 )

    post = post.replace("start="+old_start, "start="+start)
    next_page = url + "?" + post

    data = scrapertools.cache_page(url, post=post)

    episodes = jsontools.load_json(data)

    for episode in episodes:

        thumbnail = host+"/thumbs/" + episode['thumbnail'].decode("utf8").encode("utf8")

        temporada = episode['season'].decode("utf8").encode("utf8")
        episodio = episode['episode'].decode("utf8").encode("utf8").zfill(2)
        plot=""
        
        if episode['languages'] != "[]":
            idiomas = "[COLOR orange][B]" + "/".join(episode['languages']).decode("utf8").encode("utf8") + "[/B][/COLOR]"
        else: idiomas = ""
        if "es" in episode['show']['title']:
          show = "".join(episode['show']['title']['es']).decode("utf8").encode("utf8")
        else:
          show = "".join(episode['show']['title']['en']).decode("utf8").encode("utf8")

        show = bbcode_kodi2html("[COLOR whitesmoke][B]" + show + "[/B][/COLOR]")

        if episode['title']:
          if "es" in episode['title']:
            title = "".join(episode['title']['es']).decode("utf8").encode("utf8")
          else:
            title = "".join(episode['title']['en']).decode("utf8").encode("utf8")

        if len(title) == 0: title = "Temporada " + temporada + " Episodio " + episodio

        title = temporada + "x" + episodio + " - " + show + ": " + title
        
        plot+= "Idiomas: " + bbcode_kodi2html("[COLOR orange][B]" + idiomas + "[/B][/COLOR] ") 

        estado = get_status(status, 'episodes', episode['id'])
        fulltitle = title
        if estado: fulltitle += estado

        url = urlparse.urljoin( host, '/serie/'+ episode['permalink'].decode("utf8").encode("utf8") +'/temporada-' + temporada +'/episodio-' + episodio ) + "###" + episode['id'].decode("utf8").encode("utf8") + ",3"

        itemlist.append( Item( channel=__channel__, action="findvideos", title=title,plot=plot, fulltitle=fulltitle, url=url, thumbnail=thumbnail, folder=True ) )

    if len(itemlist) == 24:
        itemlist.append( Item( channel=__channel__, action="novedades_episodios", title=">> Página siguiente", url=next_page, folder=True ) )

    return itemlist

def generos(item):
    logger.info("pelisalacarta.channels.hdfull generos")
    itemlist = []

    data = agrupa_datos( scrapertools.cache_page(item.url) )
    data = scrapertools.find_single_match(data,'<li class="dropdown"><a href="http://hdfull.tv/peliculas"(.*?)</ul>')

    patron  = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""

        itemlist.append( Item( channel=__channel__, action="fichas", title=title, url=url, folder=True ) )

    return itemlist

def generos_series(item):
    logger.info("pelisalacarta.channels.hdfull generos_series")
    itemlist = []

    data = agrupa_datos( scrapertools.cache_page(item.url) )
    data = scrapertools.find_single_match(data,'<li class="dropdown"><a href="http://hdfull.tv/series"(.*?)</ul>')

    patron  = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""

        itemlist.append( Item( channel=__channel__, action="fichas", title=title, url=url, folder=True ) )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.hdfull findvideos")
    itemlist=[]

    ## Carga estados
    status = jsontools.load_json(scrapertools.cache_page(host+'/a/status/all'))

    url_targets = item.url

    ## Vídeos
    if "###" in item.url:
        id = item.url.split("###")[1].split(",")[0]
        type = item.url.split("###")[1].split(",")[1]
        item.url = item.url.split("###")[0]
        
    
    if type == "2" and account and not item.extra:
        estado = get_status(status, "movies", id)
        
        if "Favorito" in estado: title = bbcode_kodi2html("([COLOR red][B]Quitar de Favoritos[/B][/COLOR])")
        else: title = bbcode_kodi2html("([COLOR orange][B]Agregar a Favoritos[/B][/COLOR])")
        itemlist.append( Item( channel=__channel__, action="set_status", title=title, fulltitle=title, url=url_targets, thumbnail=item.thumbnail, show=item.show, folder=True ) )
        
        if "Visto" in estado: title = bbcode_kodi2html("([COLOR red][B]Marcar como no visto[/B][/COLOR])")
        elif "Pendiente" in estado: title = bbcode_kodi2html("([COLOR green][B]Marcar como visto[/B][/COLOR])")
        else: title = bbcode_kodi2html("([COLOR orange][B]Marcar como pendiente[/B][/COLOR])")
        itemlist.append( Item( channel=__channel__, action="set_status", title=title, fulltitle=title, url=url_targets, thumbnail=item.thumbnail, show=item.show, folder=True ) )
  
    if type == "3" and account and not item.extra:
        estado = get_status(status, "episodes", id)

        if "Visto" in estado: title = bbcode_kodi2html("([COLOR red][B]Marcar como no visto[/B][/COLOR])")
        elif "Pendiente" in estado: title = bbcode_kodi2html("([COLOR green][B]Marcar como visto[/B][/COLOR])")
        else: title = bbcode_kodi2html("([COLOR orange][B]Marcar como pendiente[/B][/COLOR])")
        itemlist.append( Item( channel=__channel__, action="set_status", title=title, fulltitle=title, url=url_targets, thumbnail=item.thumbnail, show=item.show, folder=True ) )
   
    data = agrupa_datos( scrapertools.cache_page(item.url) )

    data = HTMLParser.HTMLParser().unescape(data.decode("utf8")).encode("utf8")
    patron  = '<div class="embed-selector"[^<]+'
    patron += '<h5 class="left"[^<]+'
    patron += '<span[^<]+<b class="key">\s*Idioma.\s*</b>\s*([^<]+)\s*</span[^<]+'
    patron += '<span[^<]+<b class="key">\s*Servidor.\s*</b><b[^>]+>\s*([^<]+)\s*</b[^<]+</span[^<]+'
    patron += '<span[^<]+<b class="key">\s*Calidad.\s*</b>\s*([^<]+)\s*</span[^<]+</h5.*?'
    patron += '<a href="(http[^"]+)".*?'
    patron += '</i>\s*(.*?)\s*</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    opciones =[]
    for idioma,servername,calidad,url,opcion in matches:
        print opcion
        if opcion != "Descargar": opcion = "Ver"
        
        title = opcion+": "+servername.lower()
        calidades = "("+ calidad+") ("+ idioma+")"
        title = scrapertools.htmlclean(title)
        thumbnail = item.thumbnail
        plot = item.title+"\n\n"+scrapertools.find_single_match(data,'<meta property="og:description" content="([^"]+)"')
        plot = scrapertools.htmlclean(plot)
        fanart = scrapertools.find_single_match(data,'<div style="background-image.url. ([^\s]+)')
        url+= "###" + id + "," + type
        
        if item.extra == "" and not calidades in opciones:
          opciones.append(calidades)
          itemlist.append( Item( channel=__channel__, action="findvideos", title="Opción: " + calidades, extra=calidades, url=url_targets, folder=True ) )
          
        elif item.extra == calidades:
          itemlist.append( Item( channel=__channel__, action="play", title=title, url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, show=item.show, folder=True ) )
        
    return itemlist


def play(item):
    logger.info("pelisalacarta.channels.hdfull play")

    if "###" in item.url:
        id = item.url.split("###")[1].split(",")[0]
        type = item.url.split("###")[1].split(",")[1]
        item.url = item.url.split("###")[0]

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__
        if account:
          post = "target_id=%s&target_type=%s&target_status=1" % (id, type)
          data = scrapertools.cache_page(host+"/a/status",post=post)

    return itemlist    

## --------------------------------------------------------------------------------
## --------------------------------------------------------------------------------

def agrupa_datos(data):
    ## Agrupa los datos
    data = re.sub(r'\n|\r|\t|&nbsp;|<br>|<!--.*?-->','',data)
    data = re.sub(r'\s+',' ',data)
    data = re.sub(r'>\s<','><',data)
    return data

def extrae_idiomas(bloqueidiomas):
    logger.info("idiomas="+bloqueidiomas)
    patronidiomas = '([a-z0-9]+).png"'
    idiomas = re.compile(patronidiomas,re.DOTALL).findall(bloqueidiomas)
    textoidiomas= "/".join(idiomas).upper()

    return textoidiomas

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



def set_status(item):

    if "###" in item.url:
        id = item.url.split("###")[1].split(",")[0]
        type = item.url.split("###")[1].split(",")[1]
        #item.url = item.url.split("###")[0]

    if "Abandonar" in item.title or "Abandonar" in item.fulltitle:
        path = "/a/status"
        post = "target_id=" + id + "&target_type=" + type + "&target_status=0"
        
    elif "Marcar como visto" in item.title or "Marcar como visto" in item.fulltitle:
        path = "/a/status"
        post = "target_id=" + id + "&target_type=" + type + "&target_status=1"
        
    elif "Marcar como no visto pendiente" in item.title or "Marcar como pendiente" in item.fulltitle:
        path = "/a/status"
        post = "target_id=" + id + "&target_type=" + type + "&target_status=2"
        
    elif "Marcar como no visto" in item.title or "Marcar como no visto" in item.fulltitle:
        path = "/a/status"
        post = "target_id=" + id + "&target_type=" + type + "&target_status=0"
                
    elif "Seguir" in item.title or "Seguir" in item.fulltitle:
        target_status = "3"
        path = "/a/status"
        post = "target_id=" + id + "&target_type=" + type + "&target_status=3"

    elif "Agregar a Favoritos" in item.title or "Agregar a Favoritos" in item.fulltitle:
        path = "/a/favorite"
        post = "like_id=" + id + "&like_type=" + type + "&like_comment=&vote=1"

    elif "Quitar de Favoritos" in item.title or "Quitar de Favoritos" in item.fulltitle:
        path = "/a/favorite"
        post = "like_id=" + id + "&like_type=" + type + "&like_comment=&vote=-1"

    data = scrapertools.cache_page(host + path, post=post)
    
    title = bbcode_kodi2html("[COLOR green][B]OK[/B][/COLOR]")
    return [ Item( channel=__channel__, action="episodios", title=title, fulltitle=title, url=item.url, thumbnail=item.thumbnail, show=item.show, folder=False ) ]

def get_status(status,type,id):
    retorno =""
    if account:
      if type == 'shows':
          state = {'0':'','1':'Finalizada','2':'Pendiente','3':'Siguiendo'}
      else:
          state = {'0':'','1':'Visto','2':'Pendiente'}

      
      favoritos =""
      estado =""
      if status:
        if id in status['favorites'][type]:
            favoritos = bbcode_kodi2html("[COLOR orange][B]Favorito[/B][/COLOR]" )

        if id in status['status'][type]:
            estado = state[status['status'][type][id]]
            if estado: estado = bbcode_kodi2html( "[COLOR green][B]" + estado + "[/B][/COLOR]" )

        if favoritos:
            retorno += " (" + favoritos +")"
        if estado:
            retorno += " (" + estado +")"

    return retorno

