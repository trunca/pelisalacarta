# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta
# librerias libtorrent para Linux x86
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from ctypes import *
import os
libs = os.listdir(os.path.join(os.path.dirname(__file__),"libs"))
for lib in libs:
  cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),"libs",lib))
from libtorrent import *
