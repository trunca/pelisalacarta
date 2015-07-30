# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "A"
__language__ = "ES"
__title__ = "Aquitorrent"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 2
__adult__ = False
__date__ = "25/05/2015"
__creationdate__ = ""
__changes__ = "aquitorret. Madificacion por cambios web "
__thumbnail__ = "http://s6.postimg.org/47c93xmq9/aquitorrent.jpg"
__channel__ = "aquitorrent"

import urlparse,urllib2,urllib,re
import os, sys, random

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

host = "http://www.aquitorrent.com/"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.aquitorrent mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Peliculas" , url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=PELICULAS", thumbnail="http://imgc.allpostersimages.com/images/P-473-488-90/37/3710/L3YAF00Z/posters/conrad-knutsen-cinema.jpg", fanart="http://s6.postimg.org/m8dipognl/aquitorrentfanart2.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Series", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=SERIES", thumbnail="http://s6.postimg.org/nbxn1n1ap/aquitserielogo.jpg", fanart="http://s6.postimg.org/x6os7v58x/aquitorretseries.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Películas HD", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=Peliculas%20HD", thumbnail="http://s6.postimg.org/4uymx2vyp/aquithdlogo.jpg", fanart="http://s6.postimg.org/umxqri72p/aquitphd3.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Películas 3D", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=PELICULAS%203D", thumbnail="http://s6.postimg.org/53rm99jdd/aquit3dlogo.jpg", fanart="http://s6.postimg.org/9i03l3txt/aquit3d.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Películas V.O.S.", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=PELICULAS%20V.O.S.", thumbnail="http://s6.postimg.org/fofbx2s0h/aquitvostub2.jpg", fanart="http://s6.postimg.org/wss1m0aj5/aquitvos.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Docus y TV", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=Docus%20y%20TV",  thumbnail="http://s6.postimg.org/5mnir1w0h/tv_docaquit.jpg", fanart="http://s6.postimg.org/5lrd2uyc1/aquitdoctv3_an.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Clásicos Disney", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=CLASICOS%20DISNEY", thumbnail="http://s6.postimg.org/87xosbas1/Walt_Disney.jpg", fanart="http://s6.postimg.org/5m0jucd3l/aquitwalt.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="F1 2014", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=F1%202014", thumbnail="http://s6.postimg.org/42vyxvrrl/aquitf1tub.png", fanart="http://s6.postimg.org/sbqhvuhjl/aquitf1f.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="MotoGP 2014", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=MotoGP%202014", thumbnail="http://s6.postimg.org/flquwhyz5/aquit_Moto_GP_Logo.jpg", fanart="http://s6.postimg.org/sv06iuyc1/aquitmgpf2.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Mundial 2014", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=Mundial%202014", thumbnail="http://s6.postimg.org/sgyuj9e8h/aquitmundial_TUB.png", fanart="http://s6.postimg.org/7vk2rcwnl/aquitmundiall.jpg"))
    itemlist.append( Item(channel=__channel__, action="search", title="Buscar...", url="", thumbnail="http://s6.postimg.org/gninw2o9d/searchaquittub.jpg", fanart="http://s6.postimg.org/b4kpslglt/searchaquit.jpg"))
    
    

    return itemlist


                

def search(item,texto):
    logger.info("[pelisalacarta.aquitorrent search texto="+texto)
    
    item.url = "http://www.aquitorrent.com/buscar.asp?q=%s" % (texto)
    try:
        
        return buscador(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []


def buscador(item):
    logger.info("pelisalacarta.aquitorrent buscador")
    
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    #quitamos los titulos de los href en enlaces<
    data = re.sub(r'&/[^"]+">','">',data)

    patron = '<h2 class="post-title entry-title">.*?'
    patron += '<a href=".([^"]+)".*?>'
    patron += '([^<]+)</a>.*?'
    patron += '<img src="([^"]+)".*?'
    patron += '<b>([^"]+)</b>'
    
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0 :
        itemlist.append( Item(channel=__channel__, title="[COLOR gold][B]No hay resultados...[/B][/COLOR]", thumbnail ="http://s6.postimg.org/t48ttay4x/aquitnoisethumb.png", fanart ="http://s6.postimg.org/4wjnb0ksx/aquitonoisefan.jpg",folder=False) )
    
    
    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedinfo in matches:
        scrapedinfo = scrapedinfo.replace("<br>","-")
        scrapedinfo = scrapedinfo.replace(scrapedinfo,"[COLOR green]"+scrapedinfo+"[/COLOR]")
        scrapedtitle= scrapedtitle.replace(scrapedtitle,"[COLOR white]"+scrapedtitle+"[/COLOR]")
        scrapedtitle = scrapedtitle + " (" + scrapedinfo + ")"
        # Arregla la url y thumbnail
        #scrapedurl = fix_url(scrapedurl)
        scrapedthumbnail = fix_url(scrapedthumbnail)
        
        
        if "tipo=Docus" in item.url or "tipo=F1" in item.url or "tipo=MotoGP" in item.url or "tipo=Mundia" in item.url:
            action= "findvideos"
        else:
            action = "findvideos"
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url= urlparse.urljoin(host, scrapedurl), action=action, fanart="http://s9.postimg.org/lmwhrdl7z/aquitfanart.jpg", thumbnail=scrapedthumbnail) )

    return itemlist


def peliculas(item):
    logger.info("pelisalacarta.aquitorrent peliculas")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    #quitamos los titulos de los href en enlaces<
    data = re.sub(r'&/[^"]+">','">',data)
    
    
    patron = '<div class="sompret-image">'
    patron += '<a href=".([^"]+)".*?>'
    patron += '<img src="([^"]+)".*?'
    patron += 'title="(.*?) -.*?'
    patron += '<b>([^"]+)</b>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
   
    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedinfo in matches:
        scrapedinfo = scrapedinfo.replace("<br>","-")
        scrapedinfo = scrapedinfo.replace(scrapedinfo,"[COLOR green]"+scrapedinfo+"[/COLOR]")
        scrapedtitle= scrapedtitle.replace(scrapedtitle,"[COLOR white]"+scrapedtitle+"[/COLOR]")
        scrapedtitle = scrapedtitle + " (" + scrapedinfo + ")"
        # Arregla la url y thumbnail
        #scrapedurl = fix_url(scrapedurl)
        scrapedthumbnail = fix_url(scrapedthumbnail)
        
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=urlparse.urljoin(host, scrapedurl), action="findvideos", fanart="http://s9.postimg.org/lmwhrdl7z/aquitfanart.jpg", thumbnail=scrapedthumbnail) )

    ## Paginación
    pagina = int(scrapertools.get_match(item.url,"pagina=(\d+)"))+1
    pagina = "pagina=%s" % (pagina)
    next_page = re.sub(r"pagina=\d+", pagina, item.url)
    title= "[COLOR green]Pagina siguiente>>[/COLOR]"
    if pagina in data:
        itemlist.append( Item(channel=__channel__, title=title, url=next_page, fanart="http://s9.postimg.org/lmwhrdl7z/aquitfanart.jpg", thumbnail="http://s6.postimg.org/4hpbrb13l/texflecha2.png",
            action="peliculas", folder=True) )


    
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.aquitorrent findvideos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    # Torrent en zip
    patron = '<h1 class="post-title entry-title">([^<]+)</h1>.*?</b><br><br>.*?'
    patron+= 'href="(.*?\.zip)".*?'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        for scrapedtitle, scrapedzip in matches:
            # Arregla la url y extrae el torrent
            scrapedtorrent = unzip(fix_url(scrapedzip))
            
            itemlist.append( Item(channel=__channel__, title =item.title+"[COLOR red][B] [magnet][/B][/COLOR]" , url=scrapedtorrent,  action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.fanart , folder=False) )

    #Vamos con el normal

    patron = '<h1 class="post-title entry-title">([^<]+)</h1>.*?'
    patron+= 'href="(magnet[^"]+)".*?'


    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedtitle, scrapedmagnet in matches:
        itemlist.append( Item(channel=__channel__, title =item.title+"[COLOR red][B] [magnet][/B][/COLOR]" , url=scrapedmagnet,  action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.fanart , folder=False) )
    
    #nueva variacion
    if len(itemlist) == 0:
       patron = '<h1 class="post-title entry-title">([^<]+)</h1>.*?<br><br>.*?'
       patron+= 'href="([^"]+)".*?'
       
       matches = re.compile(patron,re.DOTALL).findall(data)
    
       for scrapedtitle, scrapedtorrent in matches:
           itemlist.append( Item(channel=__channel__, title =scrapedtitle+"[COLOR green][B] [magnet][/B][/COLOR]", url=scrapedtorrent, action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.fanart , folder=False) )


    
    return itemlist


def fix_url(url):
    if url.startswith("/"):
        url = url[1:]
        if not url.startswith("http://"):
            url = host+url
    return url

def unzip(url):
    import zipfile
    
    # Path para guardar el zip como tem.zip los .torrent extraidos del zip
    torrents_path = config.get_library_path()+'/torrents'
    if not os.path.exists(torrents_path):
        os.mkdir(torrents_path)

    ## http://stackoverflow.com/questions/4028697/how-do-i-download-a-zip-file-in-python-using-urllib2
    # Open the url
    try:
        f = urllib2.urlopen(url)
        with open( torrents_path+"/temp.zip", "wb") as local_file:
            local_file.write(f.read())
        
        # Open our local file for writing
        fh = open(torrents_path+"/temp.zip", 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            z.extract(name, torrents_path)
        fh.close()

    #handle errors
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url

    torrent = "file:///"+torrents_path+"/"+name

    if not torrents_path.startswith("/"):
        torrents_path = "/"+torrents_path
    
    torrent = "file://"+torrents_path+"/"+name
    
    return torrent









