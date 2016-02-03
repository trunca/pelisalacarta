# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys

from core import config
from core import logger
from core.item import Item
from core import library
from core import guitools

directorio = os.path.join(config.get_library_path(),"SERIES")
if not os.path.exists(directorio):
    os.mkdir(directorio)
seriesxml = os.path.join( config.get_data_path() , "series.xml" )

if os.path.exists(seriesxml):
  if config.get_setting("updatelibrary")=="true":
      logger.info("Actualizando series...")
      
      f = open(seriesxml, "r")
      
      for serie in f.readlines():
          item = Item()
          item.deserialize(serie)
          carpeta=library.LimpiarNombre(item.show)
          ruta = os.path.join( config.get_library_path() , "SERIES" , carpeta )
          
          logger.info("Actualizando serie: "+item.show)
          logger.info("Ruta: "+ruta )
          
          if os.path.exists(ruta):
              try:
                exec "from pelisalacarta.channels import "+item.channel
                exec "itemlist = "+item.channel+"."+item.action+"(item)"
              except:
                  import traceback
                  logger.error(traceback.format_exc())
                  itemlist = []
          else:
              logger.info("Serie: "+item.show+" No actualizada, no existe el directorio")
              itemlist=[]

          for episodio in itemlist:
                if episodio.action!="add_serie_to_library" and episodio.action!="download_all_episodes":
                  episodio.category="Series"
                  library.Guardar(episodio)
      guitools.UpdateLibrary(Item())
  else:
      logger.info("No actualiza la biblioteca, está desactivado en la configuración de pelisalacarta")

