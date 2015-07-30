# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Logger multiplataforma
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Historial de cambios:
#------------------------------------------------------------

import platform_name
import os
import config

if os.path.exists(os.path.join( config.get_runtime_path(),"platformcode",platform_name.PLATFORM_NAME,"logger.py")):
  exec "import platformcode."+platform_name.PLATFORM_NAME+".logger as platformlogger"
  default = False
else:
  default = True

def info(texto):
    if config.get_setting("debug")=="true":
        if not default:
            platformlogger.info(texto)
        else:
            print texto

def debug(texto):
    if config.get_setting("debug")=="true":
        if not default:
            platformlogger.debug(texto)
        else:
            print texto

def error(texto):

        if not default:
            platformlogger.error(texto)
        else:
            print texto
