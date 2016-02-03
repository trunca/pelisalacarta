# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import urlparse
import re
import sys
import os

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from lib import requests

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Animeflv"
__channel__ = "animeflv"
__language__ = "ES"

host = "http://animeflv.net/"

'''
### PARA USAR CON TRATK.TV ###

season: debe ir en orden descendente
episode: la "temporada 1" siempre son "0 capitulos", la "temporada 2" es el "numero de capitulos de la temporada 1"

FAIRY TAIL:
    - SEASON 1: EPISODE 48 --> season 1: total_episode: 0
    - SEASON 2: EPISODE 48 --> season 2: total_episode: 48
    - SEASON 3: EPISODE 54 --> season 3: total_episode: 96 ( [48=season2] +[ 48=season1] )
    - SEASON 4: EPISODE 175 --> season 4: total_episode: 150 ( [54=season3] + [48=season2] + [48=season3] )

animeflv.data.json
{
   "SERIES":{
      "Fairy Tail":{
         "season":[
            4,
            3,
            2,
            1
         ],
         "total_episode":[
            150,
            96,
            48,
            0
         ]
      },
      "Fairy Tail (2014)":{
         "season":[
            6,
            5
         ],
         "total_episode":[
            51,
            0
         ]
      }
   }
}

'''


def get_page(url):

    response = requests.get(url)
    return response.status_code, response.content


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.channels.animeflv mainlist")

    itemlist = list([])
    itemlist.append(Item(channel=__channel__, action="novedades", title="Últimos episodios", url=host))
    itemlist.append(Item(channel=__channel__, action="menuseries", title="Series",
                         url=urlparse.urljoin(host, "animes/?orden=nombre&mostrar=series")))
    itemlist.append(Item(channel=__channel__, action="menuovas", title="OVAS",
                         url=urlparse.urljoin(host, "animes/?orden=nombre&mostrar=ovas")))
    itemlist.append(Item(channel=__channel__, action="menupeliculas", title="Películas",
                         url=urlparse.urljoin(host, "animes/?orden=nombre&mostrar=peliculas")))
    itemlist.append(Item(channel=__channel__, action="search", title="Buscar",
                         url=urlparse.urljoin(host, "animes/?buscar=")))

    return itemlist


def menuseries(item):
    logger.info("pelisalacarta.channels.animeflv menuseries")

    itemlist = list([])
    itemlist.append(Item(channel=__channel__, action="letras", title="Por orden alfabético",
                         url=urlparse.urljoin(host, "animes/?orden=nombre&mostrar=series")))
    itemlist.append(Item(channel=__channel__, action="generos", title="Por géneros",
                         url=urlparse.urljoin(host, "animes/?orden=nombre&mostrar=series")))
    itemlist.append(Item(channel=__channel__, action="series", title="En emisión",
                         url=urlparse.urljoin(host, "animes/en-emision/?orden=nombre&mostrar=series")))

    return itemlist


def menuovas(item):
    logger.info("pelisalacarta.channels.animeflv menuovas")

    itemlist = list([])
    itemlist.append(Item(channel=__channel__, action="letras", title="Por orden alfabético",
                         url=urlparse.urljoin(host, "animes/?orden=nombre&mostrar=ovas")))
    itemlist.append(Item(channel=__channel__, action="generos", title="Por géneros",
                         url=urlparse.urljoin(host, "animes/?orden=nombre&mostrar=ovas")))
    itemlist.append(Item(channel=__channel__, action="series", title="En emisión",
                         url=urlparse.urljoin(host, "animes/en-emision/?orden=nombre&mostrar=ovas")))

    return itemlist


def menupeliculas(item):
    logger.info("pelisalacarta.channels.animeflv menupeliculas")

    itemlist = list([])
    itemlist.append(Item(channel=__channel__, action="letras", title="Por orden alfabético",
                         url=urlparse.urljoin(host, "animes/?orden=nombre&mostrar=peliculas")))
    itemlist.append(Item(channel=__channel__, action="generos", title="Por géneros",
                         url=urlparse.urljoin(host, "animes/?orden=nombre&mostrar=peliculas")))
    itemlist.append(Item(channel=__channel__, action="series", title="En emisión",
                         url=urlparse.urljoin(host, "animes/en-emision/?orden=nombre&mostrar=peliculas")))

    return itemlist


def letras(item):
    logger.info("pelisalacarta.channels.animeflv letras")

    itemlist = []

    status_code, data = get_page(item.url)
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(status_code))

    if status_code == requests.codes.ok:

        data = scrapertools.get_match(data, '<div class="alfabeto_box"(.*?)</div>')
        patron = '<a href="([^"]+)[^>]+>([^<]+)</a>'
        matches = re.compile(patron, re.DOTALL).findall(data)

        for scrapedurl, scrapedtitle in matches:
            title = scrapertools.entityunescape(scrapedtitle)
            url = urlparse.urljoin(item.url, scrapedurl)
            thumbnail = ""
            plot = ""
            if DEBUG:
                logger.info("title=[{0}], url=[{1}], thumbnail=[{2}]".format(title, url, thumbnail))

            itemlist.append(Item(channel=__channel__, action="series", title=title, url=url, thumbnail=thumbnail,
                                 plot=plot))

    else:
        itemlist.append(Item(channel=__channel__, action="mainlist",
                             title="No se ha podido cargar la pagina ERROR:{0}".format(status_code), url="",
                             thumbnail="", plot=""))

    return itemlist


def generos(item):
    logger.info("pelisalacarta.channels.animeflv generos")

    itemlist = []

    status_code, data = get_page(item.url)
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(item.url))
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(status_code))

    if status_code == requests.codes.ok:

        data = scrapertools.get_match(data, '<div class="generos_box"(.*?)</div>')
        patron = '<a href="([^"]+)[^>]+>([^<]+)</a>'
        matches = re.compile(patron, re.DOTALL).findall(data)

        for scrapedurl, scrapedtitle in matches:
            title = scrapertools.entityunescape(scrapedtitle)
            url = urlparse.urljoin(item.url, scrapedurl)
            thumbnail = ""
            plot = ""
            if DEBUG:
                logger.info("title=[{0}], url=[{1}], thumbnail=[{2}]".format(title, url, thumbnail))

            itemlist.append(Item(channel=__channel__, action="series", title=title, url=url, thumbnail=thumbnail,
                                 plot=plot))

    else:
        itemlist.append(Item(channel=__channel__, action="mainlist",
                             title="No se ha podido cargar la pagina ERROR:{0}".format(status_code), url="",
                             thumbnail="", plot=""))

    return itemlist


def search(item, texto):
    logger.info("pelisalacarta.channels.animeflv search")
    if item.url == "":
        item.url = urlparse.urljoin(host, "animes/?buscar=")
    texto = texto.replace(" ", "+")
    item.url = "{0}{1}".format(item.url, texto)
    try:
        return series(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []


def novedades(item):
    logger.info("pelisalacarta.channels.animeflv novedades")

    itemlist = []

    status_code, data = get_page(item.url)
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(item.url))
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(status_code))

    if status_code == requests.codes.ok:

        '''
        <div class="not">
            <a href="/ver/cyclops-shoujo-saipu-12.html" title="Cyclops Shoujo Saipu 12">
            <img class="imglstsr lazy" src="http://cdn.animeflv.net/img/mini/957.jpg" border="0">
            <span class="tit_ep"><span class="tit">Cyclops Shoujo Saipu 12</span></span>
            </a>
        </div>
        '''

        patronvideos = '<div class="not"[^<]+<a href="([^"]+)" title="([^"]+)"[^<]+<img class="[^"]+" ' \
                       'src="([^"]+)"[^<]+<span class="tit_ep"><span class="tit">([^<]+)<'
        matches = re.compile(patronvideos, re.DOTALL).findall(data)
        itemlist = []

        for match in matches:
            scrapedtitle = scrapertools.entityunescape(match[3])
            fulltitle = scrapedtitle
            # directory = match[1]
            scrapedurl = urlparse.urljoin(item.url, match[0])
            scrapedthumbnail = urlparse.urljoin(item.url, match[2].replace("mini", "portada"))
            scrapedplot = ""
            if DEBUG:
                logger.info("title=[{0}], url=[{1}], thumbnail=[{2}]".format(scrapedtitle, scrapedurl,
                                                                             scrapedthumbnail))

            itemlist.append(Item(channel=__channel__, action="findvideos", title=scrapedtitle, url=scrapedurl,
                                 thumbnail=scrapedthumbnail, plot=scrapedplot, fulltitle=fulltitle, viewmode="movie"))

    else:
        itemlist.append(Item(channel=__channel__, action="mainlist",
                             title="No se ha podido cargar la pagina ERROR:{0}".format(status_code), url="",
                             thumbnail="", plot=""))

    return itemlist


def series(item):
    logger.info("pelisalacarta.channels.animeflv series")

    itemlist = []

    status_code, data = get_page(item.url)
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(item.url))
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(status_code))

    if status_code == requests.codes.ok:

        '''
        <div class="aboxy_lista">
            <a href="/ova/nurarihyon-no-mago-ova.html" title="Nurarihyon no Mago OVA">
                <img class="lazy portada" src="/img/blank.gif"
                    data-original="http://cdn.animeflv.net/img/portada/1026.jpg" alt="Nurarihyon no Mago OVA"/>
            </a>
            <span style="float: right; margin-top: 0px;" class="tipo_1"></span>
            <a href="/ova/nurarihyon-no-mago-ova.html" title="Nurarihyon no Mago OVA" class="titulo">
                Nurarihyon no Mago OVA
            </a>
            <div class="generos_links">
                <b>Generos:</b>
                <a href="/animes/genero/accion/">Acci&oacute;n</a>,
                <a href="/animes/genero/shonen/">Shonen</a>,
                <a href="/animes/genero/sobrenatural/">Sobrenatural</a>
            </div>
            <div class="sinopsis">
                La historia empieza en alrededor de 100 a&ntilde;os despu&eacute;s de la desaparici&oacute;n de
                Yamabuki Otome, la primera esposa Rihan Nura. Rihan por fin recobr&oacute; la compostura y la vida
                vuelve a la normalidad. A medida que la cabeza del Clan Nura, est&aacute; ocupado trabajando en la
                construcci&oacute;n de un mundo armonioso para los seres humanos y youkai. Un d&iacute;a, &eacute;l
                ve a Setsura molesta por lo que decide animarla tomando el clan para ir a disfrutar de las aguas
                termales &hellip;
            </div>
        </div>
        '''

        patron = '<div class="aboxy_lista"[^<]+'
        patron += '<a href="([^"]+)"[^<]+<img class="[^"]+" src="[^"]+" data-original="([^"]+)"[^<]+</a[^<]+'
        patron += '<span[^<]+</span[^<]+'
        patron += '<a[^>]+>([^<]+)</a.*?'
        patron += '<div class="sinopsis">(.*?)</div'
        matches = re.compile(patron, re.DOTALL).findall(data)
        itemlist = []

        for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
            title = scrapertools.unescape(scrapedtitle)
            fulltitle = title
            url = urlparse.urljoin(item.url, scrapedurl)
            thumbnail = urlparse.urljoin(item.url, scrapedthumbnail)
            plot = scrapertools.htmlclean(scrapedplot)
            show = title
            if DEBUG:
                logger.info("title=[{0}], url=[{1}], thumbnail=[{2}]".format(title, url, thumbnail))
            itemlist.append(Item(channel=__channel__, action="episodios", title=title, url=url, thumbnail=thumbnail,
                                 plot=plot, show=show, fulltitle=fulltitle, fanart=thumbnail,
                                 viewmode="movies_with_plot", folder=True))

        patron = '<a href="([^"]+)">\&raquo\;</a>'
        matches = re.compile(patron, re.DOTALL).findall(data)
        for match in matches:
            if len(matches) > 0:
                scrapedurl = urlparse.urljoin(item.url, match)
                scrapedtitle = ">> Pagina Siguiente"
                scrapedthumbnail = ""
                scrapedplot = ""

                itemlist.append(Item(channel=__channel__, action="series", title=scrapedtitle, url=scrapedurl,
                                     thumbnail=scrapedthumbnail, plot=scrapedplot, folder=True))

    else:
        itemlist.append(Item(channel=__channel__, action="mainlist",
                             title="No se ha podido cargar la pagina ERROR:{0}".format(status_code), url="",
                             thumbnail="", plot=""))

    return itemlist


def episodios(item):
    logger.info("pelisalacarta.channels.animeflv episodios")
    itemlist = []

    status_code, data = get_page(item.url)
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(item.url))
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(status_code))

    if status_code == requests.codes.ok:

        '''
        <div class="tit">Listado de episodios <span class="fecha_pr">Fecha Pr&oacute;ximo: 2013-06-11</span></div>
        <ul class="anime_episodios" id="listado_epis">
            <li><a href="/ver/aiura-9.html">Aiura 9</a></li>
            <li><a href="/ver/aiura-8.html">Aiura 8</a></li>
            <li><a href="/ver/aiura-7.html">Aiura 7</a></li>
            <li><a href="/ver/aiura-6.html">Aiura 6</a></li>
            <li><a href="/ver/aiura-5.html">Aiura 5</a></li>
            <li><a href="/ver/aiura-4.html">Aiura 4</a></li>
            <li><a href="/ver/aiura-3.html">Aiura 3</a></li>
            <li><a href="/ver/aiura-2.html">Aiura 2</a></li>
            <li><a href="/ver/aiura-1.html">Aiura 1</a></li>
        </ul>
        '''

        data = scrapertools.get_match(data, '<div class="tit">Listado de episodios.*?</div>(.*?)</ul>')
        patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
        matches = re.compile(patron, re.DOTALL).findall(data)

        for scrapedurl, scrapedtitle in matches:
            title = scrapertools.unescape(scrapedtitle)
            url = urlparse.urljoin(item.url, scrapedurl)
            thumbnail = item.thumbnail
            plot = item.plot

            # TODO crear funcion que pasandole el titulo y buscando en un array de series establezca el valor el nombre
            # y temporada / capitulo para que funcione con trak.tv

            season = 1
            episode = 1
            patron = "{0}{1}".format(re.escape(item.show), "\s+(\d+)")
            # logger.info("title {0}".format(title))
            # logger.info("patron {0}".format(patron))

            try:
                episode = scrapertools.get_match(title, patron)
                episode = int(episode)
                # logger.info("episode {0}".format(episode))
            except IndexError:
                pass
            except ValueError:
                pass

            season, episode = numbered_for_tratk(item.show, season, episode)

            if len(str(episode)) == 1:
                title = "{0}x0{1}".format(season, episode)
            else:
                title = "{0}x{1}".format(season, episode)

            title = "{0} {1}".format(item.show, title)

            if DEBUG:
                logger.info("title=[{0}], url=[{1}], thumbnail=[{2}]".format(title, url, thumbnail))

            itemlist.append(Item(channel=__channel__, action="findvideos", title=title, url=url,
                                 thumbnail=thumbnail, plot=plot, show=item.show, fulltitle="{0} {1}"
                                 .format(item.show, title), fanart=thumbnail, viewmode="movies_with_plot", folder=True))

    else:
        itemlist.append(Item(channel=__channel__, action="mainlist",
                             title="No se ha podido cargar la pagina ERROR:{0}".format(status_code), url="",
                             thumbnail="", plot=""))

    if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=__channel__, title="Añadir esta serie a la biblioteca de XBMC", url=item.url,
                             action="add_serie_to_library", extra="episodios", show=item.show))
        itemlist.append(Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url,
                             action="download_all_episodes", extra="episodios", show=item.show))

    return itemlist


def findvideos(item):
    logger.info("pelisalacarta.channels.animeflv findvideos")

    itemlist = []

    status_code, data = get_page(item.url)
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(item.url))
    logger.info("pelisalacarta.channels.animeflv **** {0}".format(status_code))

    if status_code == requests.codes.ok:

        data = scrapertools.get_match(data, "var videos \= (.*?)$")
        # logger.info("data={0}".format(data))

        itemlist = []

        data = data.replace("\\\\", "")
        data = data.replace("\\/", "/")
        logger.info("data={0}".format(data))

        from servers import servertools
        itemlist.extend(servertools.find_video_items(data=data))
        for videoitem in itemlist:
            videoitem.channel = __channel__
            videoitem.folder = False

    else:
        itemlist.append(Item(channel=__channel__, action="mainlist",
                             title="No se ha podido cargar la pagina ERROR:{0}".format(status_code), url="",
                             thumbnail="", plot=""))

    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True

    # mainlist
    mainlist_items = mainlist(Item())

    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action != "search":
            exec("itemlist = "+mainlist_item.action+"(mainlist_item)")
            if len(itemlist) == 0:
                return false

    # Comprueba si alguno de los vídeos de "Novedades" devuelve mirrors
    episodios_items = novedades(mainlist_items[0])

    bien = False
    for episodio_item in episodios_items:
        mirrors = findvideos(episodio_item)
        if len(mirrors) > 0:
            bien = True
            break

    return bien


def numbered_for_tratk(show, season, episode):
    """
    Devuelve la temporada y episodio convertido para que se marque correctamente en tratk.tv

    :param show: Nombre de la serie a comprobar
    :type show: str
    :param season: Temporada que devuelve el scrapper
    :type season: int
    :param episode: Episodio que devuelve el scrapper
    :type episode: int
    :return: season, episode
    :rtype: int, int
    """
    logger.info("pelisalacarta.channels.animeflv numbered_for_tratk")
    show = show.lower()

    new_season = season
    new_episode = episode
    SERIES = {}

    name_file = os.path.splitext(os.path.basename(__file__))[0]
    fname = os.path.join(config.get_data_path(), "channels", name_file + ".data.json")

    if os.path.isfile(fname):
        infile = open(fname, "rb")
        data = infile.read()
        infile.close()
        json_data = jsontools.load_json(data)

        if 'SERIES' in json_data:
            SERIES = json_data['SERIES']

        # ponemos en minusculas el key, ya que previamente hemos hecho lo mismo con show.
        for key in SERIES.keys():
            new_key = key.lower()
            if new_key != key:
                SERIES[new_key] = SERIES[key]
                del SERIES[key]

    if show in SERIES:
        logger.info("ha encontrado algo: {0}".format(SERIES[show]))

        if SERIES[show]['total_episode']:
            for idx, valor in enumerate(SERIES[show]['total_episode']):

                if new_episode > valor:
                    new_episode -= valor
                    new_season = SERIES[show]['season'][idx]
                    break

        else:
            new_season = SERIES[show]['season']

    logger.info("pelisalacarta.channels.animeflv numbered_for_tratk: {0}:{1}".format(new_season, new_episode))
    return new_season, new_episode
