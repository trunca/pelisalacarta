# -*- coding: utf8 -*-
#----------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# ayuda - Videos de ayuda y tutoriales para pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# contribución de jurrabi
#----------------------------------------------------------------------
import re
from core import scrapertools
from core import config
from core import logger
from core.item import Item

#Propiedades del Canal:
__category__ = "*"
__language__ = "ES"
__title__ = "Ayuda"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 0
__adult__ = False
__date__ = "25/05/2015"
__creationdate__ = ""
__changes__ = "Ayuda: "
__thumbnail__ = ""
__channel__ = "ayuda"



def isGeneric():
    return True

def mainlist(item):
    itemlist=[]
    info="Los cambios son: \n"
    info += "- Canal HDFull modificado\n"
    info += "- Canal HDFull modificado\n"
    info += "- Canal HDFull modificado\n"
    info += "- Canal HDFull modificado\n"
    itemlist.append( Item(channel=__channel__, action="", title="Novedades en esta versión", plot=info))

    return itemlist
