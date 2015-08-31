# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasdk
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
#Propiedades del Canal:
__category__ = "F,S,D,A"
__language__ = "ES"
__title__ = "Moviesultimate"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 7
__adult__ = False
__date__ = "10/03/15"
__creationdate__ = "02/11/2014"
__changes__ = ""
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
try:
    import xbmc
    import xbmcgui
except: pass

DEBUG = config.get_setting("debug")

host = "http://moviesultimate.com"
fanart = ""

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.moviesultimate mainlist")
    itemlist = []
    title ="Estrenos"
    title = title.replace(title,bbcode_kodi2html("[COLOR white][B]"+title+"[/B][/COLOR]"))
    itemlist.append( Item(channel=__channel__, title=title      , action="peliculas", url="http://moviesultimate.com",thumbnail="http://s6.postimg.org/xh61j3glt/muestthum.png", fanart="http://s6.postimg.org/3wnf8xpzl/muextfan.jpg"))
    title ="Generos"
    title = title.replace(title,bbcode_kodi2html("[COLOR white][B]"+title+"[/B][/COLOR]"))
    itemlist.append( Item(channel=__channel__, title=title      , action="generos", url="http://moviesultimate.com" ,thumbnail="http://s6.postimg.org/qt9fwhx3l/mugenthum.png", fanart="http://s6.postimg.org/pppbkjcgh/mugenfan.jpg"))
    title ="Buscar..."
    title = title.replace(title,bbcode_kodi2html("[COLOR white][B]"+title+"[/B][/COLOR]"))
    itemlist.append( Item(channel=__channel__, title=title      , action="search", url="", thumbnail="http://s6.postimg.org/6ofvr139t/mubuscthum.png", fanart="http://s6.postimg.org/4ilkwiztd/mubuscfan.jpg"))
    
    
    

    return itemlist

def bbcode_kodi2html(text):
    
    if config.get_platform().startswith("plex") or config.get_platform().startswith("mediaserver"):
        import re
        text = re.sub(r'\[COLOR\s([^\]]+)\]',
                      r'<span style="color: \1">',
                      text)
        text = text.replace('[/COLOR]','</span>')
        text = text.replace('[CR]','<br>')
        text = text.replace('[B]','<b>')
        text = text.replace('[/B]','</b>')
        text = text.replace('"color: yellow"','"color: gold"')
        text = text.replace('"color: white"','"color: auto"')
    
    return text

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
        scrapedtitle= scrapedtitle.replace(scrapedtitle,bbcode_kodi2html("[COLOR skyblue]"+scrapedtitle+"[/COLOR]"))
        
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
        scrapedtitle= scrapedtitle.replace(scrapedtitle,bbcode_kodi2html("[COLOR white]"+scrapedtitle+"[/COLOR]"))
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
        
        scrapedtitle= scrapedtitle.replace(scrapedtitle,bbcode_kodi2html("[COLOR skyblue]"+scrapedtitle+"[/COLOR]"))
        scrapedcalidad= scrapedcalidad.replace(scrapedcalidad,bbcode_kodi2html("[COLOR sandybrown]"+scrapedcalidad+"[/COLOR]"))
        title = scrapedtitle + " (" +scrapedcalidad + ")"
       
        itemlist.append( Item(channel=__channel__, title =title , url=scrapedurl, action="fanart", thumbnail=scrapedthumbnail, fanart="http://s6.postimg.org/40zm85p01/mubackground3.jpg", folder=True) )
    ## Paginación
    patronvideos  = '<div class="paginacion">.*?<span class=\'current\'>.*?href=\'([^\']+)\''
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        title ="siguiente>>"
        title = title.replace(title,bbcode_kodi2html("[COLOR slate]"+title+"[/COLOR]"))
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=scrapedurl , thumbnail="http://s6.postimg.org/drfhhwrtd/muarrow.png", fanart="http://s6.postimg.org/40zm85p01/mubackground3.jpg",  folder=True) )
    

    return itemlist

def fanart(item):
    logger.info("pelisalacarta.moviesultimate fanart")
    itemlist = []
    url = item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|&#[0-9];","",data)
    title= scrapertools.get_match(data,'<html lang.*?<title>(.*?) \|')
    title= re.sub(r"3D|SBS|-|","",title)
    title= title.replace('Reparado','')
    title= title.replace(' ','%20')
    url="http://api.themoviedb.org/3/search/movie?api_key=57983e31fb435df4df77afb854740ea9&query=" + title + "&language=es&include_adult=false"
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patron = '"page":1.*?"backdrop_path":"(.*?)".*?,"id":(.*?),'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
       extra=item.thumbnail
       show= item.thumbnail
       category= item.thumbnail
       itemlist.append( Item(channel=__channel__, title=item.title, url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.thumbnail,extra = extra, show= show, category= category,folder=True) )
    else:
        for fan, id in matches:
            fanart="https://image.tmdb.org/t/p/original" + fan
            item.extra= fanart
    #clearart, fanart_2 y logo
            url ="http://assets.fanart.tv/v3/movies/"+id+"?api_key=6fa42b0ef3b5f3aab6a7edaa78675ac2"
            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            patron = '"hdmovielogo":.*?"url": "([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            if '"moviedisc"' in data:
                disc = scrapertools.get_match(data,'"moviedisc":.*?"url": "([^"]+)"')
            if '"movieposter"' in data:
                poster = scrapertools.get_match(data,'"movieposter":.*?"url": "([^"]+)"')
            if '"moviethumb"' in data:
                thumb = scrapertools.get_match(data,'"moviethumb":.*?"url": "([^"]+)"')
            if '"moviebanner"' in data:
                banner= scrapertools.get_match(data,'"moviebanner":.*?"url": "([^"]+)"')
                    
            if len(matches)==0:
               extra=  item.thumbnail
               show = item.extra
               category = item.extra
               itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=item.thumbnail, fanart=item.extra, extra=extra, show=show, category= category, folder=True) )
        for logo in matches:
            if '"hdmovieclearart"' in data:
                clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                if '"moviebackground"' in data:
                    fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                    extra=clear
                    show= fanart_2
                    if '"moviedisc"' in data:
                        category= disc
                    else:
                         category= clear
                    itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category,folder=True) )
                else:
                      extra= clear
                      show=item.extra
                      if '"moviedisc"' in data:
                          category= disc
                      else:
                          category= clear
                      itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category, folder=True) )

            if '"moviebackground"' in data:
                fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                if '"hdmovieclearart"' in data:
                    clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                    extra=clear
                    show= fanart_2
                    if '"moviedisc"' in data:
                        category= disc
                    else:
                         category= clear
                else:
                     extra=logo
                     show= fanart_2
                     if '"moviedisc"' in data:
                        category= disc
                     else:
                          category= logo
                     itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category, folder=True) )
                
                
                
                
            if not '"hdmovieclearart"' in data and not '"moviebackground"' in data:
                    extra= logo
                    show=  item.extra
                    if '"moviedisc"' in data:
                        category= disc
                    else:
                         category= item.extra
                    itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show ,  category= category, folder=True) )
    title ="Info"
    title = title.replace(title,bbcode_kodi2html("[COLOR gold]"+title+"[/COLOR]"))
    if len(item.extra)==0:
       fanart=item.thumbnail
    else:
         fanart = item.extra
             
    if '"movieposter"' in data:
        thumbnail= poster
    elif '"tvposter"' in data:
         thumbnail= tvposter
    else:
         thumbnail = item.thumbnail
             
                                                                                            
    itemlist.append( Item(channel=__channel__, action="info" , title=title , url=item.url, thumbnail=thumbnail, fanart=fanart, extra= extra, category = category, show= show, folder=False ))

    return itemlist
def findvideos(item):
    logger.info("pelisalacarta.peliculasdk findvideos")
    
    itemlist = []
    data = re.sub(r"<!--.*?-->","",scrapertools.cache_page(item.url))
    
    patronvideos = '<div id="usual1" class="usual">(.*?)<script type="text/javascript">'
    matchesvideos = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for bloque_videos in matchesvideos:
        if (DEBUG): logger.info("bloque_videos"+bloque_videos)

    patron = '<div id="tab.*?">.*?'
    patron+= '<iframe.*?src="([^"]+)".*?scrolling='
    matches = re.compile(patron,re.DOTALL).findall(bloque_videos)
    scrapertools.printMatches(matches)

    for  url in matches:
        if "waaw.tv" in url:
            url = url
            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            patron = '<div class="player_container" id="normal_player_cont" style="height:563px">.*?src="([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            for qqtv in matches:
                url = qqtv
                server = bbcode_kodi2html(" [COLOR skyblue][B]Netu[/B][/COLOR]")
        if "nowvideo" in url :
            server =bbcode_kodi2html(" [COLOR skyblue][B]Nowvideo[/B][/COLOR]")
        elif "netu" in url:
            server = bbcode_kodi2html(" [COLOR skyblue][B]Netu[/B][/COLOR]")

        title =  bbcode_kodi2html("[COLOR white]Ver en [/COLOR]") + server
        itemlist.append( Item(channel=__channel__, title =title , thumbnail=item.extra, url=url, fanart=item.show, action="play", folder=False) )
    #qqtv
    patron = "<script src='http://hqq.tv.*?hash.*?=([^<]+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for vid in matches:
        url = "http://hqq.tv/player/embed_player.php?vid=" + vid
        title = bbcode_kodi2html("[COLOR white]Ver en [/COLOR]") + bbcode_kodi2html(" [COLOR skyblue][B]Netu[/B][/COLOR]")
        itemlist.append( Item(channel=__channel__, title =title , thumbnail=item.extra, url=url, fanart=item.show, action="play", folder=False) )



    return itemlist



    



def play(item):
    logger.info("pelisalacarta.bricocine findvideos")
    media_url = scrapertools.get_header_from_response(item.url,header_to_get="location")
    itemlist = servertools.find_video_items(data=media_url)
    
    if len(itemlist) == 0:
    
    
       itemlist = servertools.find_video_items(data=item.url)
       data = scrapertools.cache_page(item.url)
    
    
    
    listavideos = servertools.findvideos(data)
    
    for video in listavideos:
        videotitle = item.title
        url =item.url
        server = video[2]
        
        
    
    
   

    return itemlist

def info(item):
    logger.info("pelisalacarta.zentorrents info")
    
    url=item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|\d+x\d+|&nbsp;|&#.*?;|<span.*?>|<\/span>","",data)
    title= scrapertools.get_match(data,'<html lang.*?<title>(.*?) \|')
    calidad= scrapertools.get_match(data,'<p><i>Calidad</i>.*?"tag">([^<]+)</a>')
    calidad= calidad.replace(calidad,bbcode_kodi2html("[COLOR sandybrown]"+calidad+"[/COLOR]"))
    title = title.replace(title,bbcode_kodi2html("[COLOR grey][B]"+title+"[/B][/COLOR]"))
    title = title + " ("+calidad+")"
    plot = scrapertools.get_match(data,'<p><p>(.*?)<\/p><\/p>')
    plot = plot.replace(plot,bbcode_kodi2html("[COLOR skyblue]"+plot+"[/COLOR]"))
    foto = item.show
    photo= item.extra
    ventana2 = TextBox1(title=title, plot=plot, thumbnail=photo, fanart=foto)
    ventana2.doModal()
try:
    class TextBox1( xbmcgui.WindowDialog ):
            """ Create a skinned textbox window """
            def __init__( self, *args, **kwargs):
            
                self.getTitle = kwargs.get('title')
                self.getPlot = kwargs.get('plot')
                self.getThumbnail = kwargs.get('thumbnail')
                self.getFanart = kwargs.get('fanart')
            
                self.background = xbmcgui.ControlImage( 70, 20, 1150, 630, 'http://s6.postimg.org/58jknrvtd/backgroundventana5.png')
                self.title = xbmcgui.ControlTextBox(140, 60, 1130, 50)
                self.plot = xbmcgui.ControlTextBox( 140, 180, 1035, 600 )
                self.thumbnail = xbmcgui.ControlImage( 813, 43, 390, 100, self.getThumbnail )
                self.fanart = xbmcgui.ControlImage( 140, 351, 1035, 250, self.getFanart )
            
                self.addControl(self.background)
                self.addControl(self.title)
                self.addControl(self.plot)
                self.addControl(self.thumbnail)
                self.addControl(self.fanart)
            
                self.title.setText( self.getTitle )
                self.plot.setText(  self.getPlot )
        
            def get(self):
                self.show()
        
            def onAction(self, action):
                self.close()

    def test():
        return True
except: pass




