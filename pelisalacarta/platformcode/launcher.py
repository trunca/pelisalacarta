# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# Generic Launcher
# http://blog.tvalacarta.info/plugin-xbmc/
#------------------------------------------------------------

#Imports:

import os,sys
from core import logger
from core import config
from core.item import Item
from core import guitools


#Funcion principal.----------->OK
def run():
    logger.info("[launcher.py] run")
    config.verify_directories_created()
    itemlist=[]
    item = guitools.ExtraerItem()
    logger.info("-----------------------------------------------------------------------")
    logger.info("Item Recibido: " + item.tostring())
    logger.info("-----------------------------------------------------------------------")
    itemlist = EjecutarFuncion(item)
    # Mostrar los resultados, si los hay
    if type(itemlist)==list:  #Utilizado para no devolver ningun Item en funciones que no tienen que devolver nada (p.e play)
      MostrarResultado(itemlist, item)
      
    if item.channel=="channelselector" and item.action == "getmainlist": 
      from core import updater
      updater.checkforupdates()

#Sección encargada de recoger el Item y ejecutar su accion:----------->OK
def EjecutarFuncion(item):
    logger.info("[launcher.py] EjecutarFuncion")
    logger.info("-----------------------------------------------------------------------")
    logger.info("EjecutarFuncion: Canal=" + item.channel + " Acción=" + item.action)    
    logger.info("-----------------------------------------------------------------------")
    itemlist = []
    
    #Los strm no pueden contener items, porque da error, asi que intentamos reproducirlo, y luego 
    if item.folder == True and "strm" in item.extra:
      item.extra =""
      guitools.Update(item)
      return


    # Importa el canal
    if item.channel: channelmodule = ImportarCanal(item.channel)
    
#######################################################################
#        Aqui se ejecuta cada función segun el canal                  #
#  si no se cumple ninguna condición se ejecuta la funcion generica:  #
#               itemlist = canal.accion(item)                         #
#######################################################################

    
    #Si no hay canal, ejecuta la función dentro de este launcher
    if item.channel=="":
      exec "itemlist = "+item.action+"(item)"
    
    else:
      # play - es el menú de reproducción de un vídeo
      if item.action=="play":
          logger.info("ACCION PLAY")
          if hasattr(channelmodule, 'play'):
              logger.info("[launcher.py] executing channel 'play' method")
              logger.info(channelmodule.__file__)
              itemlist = channelmodule.play(item)
          else:
              logger.info("[launcher.py] no channel 'play' method, executing core method")
              itemlist.append(item)
              
          if len(itemlist)>0:
              itemlist = play(itemlist[0])
              
      elif item.action=="findvideos":
          if hasattr(channelmodule, 'findvideos'):
              itemlist = channelmodule.findvideos(item)
              itemlist = findvideos(item,itemlist)
          else:
              itemlist = findvideos(item,None)

      # search - es para abrir el teclado y enviar el texto
      elif item.action=="search":
          logger.info("ACCION SEARCH")
          tecleado= guitools.Keyboard("")
          if (tecleado):
              itemlist = channelmodule.search(item,tecleado)
          else:
              itemlist = []

      # Todas las demas Funciones
      else:
          #Si existe la funcion en el canal la ejecuta
          if hasattr(channelmodule, item.action):
              logger.info("[launcher.py] - Ejectuando accion: " + item.channel + "." + item.action + "(item)")
              exec "itemlist = channelmodule." + item.action + "(item)"
          #Si existe la funcion en el launcher la ejecuta
          elif hasattr(sys.modules[__name__], item.action):
              logger.info("[launcher.py] - Ejectuando accion: " + item.action + "(item)")
              exec "itemlist =" + item.action + "(item)"
          #Si no existe devuelve un error
          else:
              logger.info("[launcher.py] - No se ha encontrado la accion ["+ item.action + "] en el canal ["+item.channel+"] ni en el launcher")
              
    
    #Si no es una lista lo convierte a un string, para que no se muestre en pantalla ni de error por ser NoneType         
    if not type(itemlist)==list: itemlist=""
    
    #Aplicar varias modificaciones a los resultados (fanarts, menus contextuales predefinidos, etc...)
    for x, nitem in enumerate(itemlist):
      if not item.channel in ["","channelselector","favoritos","buscador","descargas"] or item.channel =="channelselector" and item.action =="listchannels":
        if itemlist[x].context:
          itemlist[x].context= itemlist[x].context + "|Añadir a Favoritos,add_to_favorites"
        else:
          itemlist[x].context="Añadir a Favoritos,add_to_favorites"

      '''
      if nitem.show:
          if itemlist[x].context:
            itemlist[x].context= itemlist[x].context + "|Añadir esta serie a la biblioteca,add_serie_to_library|Descargar todos los episodios de la serie,download_all_episodes"
          else:
            itemlist[x].context="Añadir esta serie a la biblioteca,add_serie_to_library|Descargar todos los episodios de la serie,download_all_episodes"
          if itemlist[x].action <> "add_serie_to_library":
            itemlist[x].refered_action=item.action
      
      if nitem.action=="play" or nitem.action =="findvideos":
          if itemlist[x].context:
            itemlist[x].context= itemlist[x].context + "|Buscar Trailer,search_trailer"
          else:
            itemlist[x].context="Buscar Trailer,search_trailer"
      '''
      if nitem.thumbnail =="" and nitem.action =="search":
        itemlist[x].thumbnail="http://pelisalacarta.mimediacenter.info/squares/search.png"
        
      if nitem.fanart=="":
        channel_fanart = os.path.join( config.get_runtime_path(), 'resources', 'images', 'fanart', item.channel+'.jpg')
        if os.path.exists(channel_fanart):
            itemlist[x].fanart = channel_fanart
        else:
            itemlist[x].fanart = os.path.join(config.get_runtime_path(),"fanart.jpg")

    if len(itemlist) >0:
      logger.info("[launcher.py] - EjecutarFuncion - Items devueltos")  
      logger.info("-----------------------------------------------------------------------")
      for item in itemlist:
        logger.info(item.tostring())
      logger.info("-----------------------------------------------------------------------")
      
    return itemlist
    

# Funcion para Mostrar los resultados:----------->OK
def MostrarResultado(itemlist, ParentItem):
    logger.info("[launcher.py] - MostrarResultado")
    Mostrar = True    
    for item in itemlist:
      #Funciones para "launcher", si un Item tiene función "launcher" no muestra los items, sino que ejecuta dicha funcion
      if item.channel=="launcher":
        Mostrar = False
        if item.action=="refresh":
          guitools.Refresh()
        if item.action=="alert":
          guitools.Dialog_OK(ParentItem.title,item.title)
        itemlist.remove(item)
      else:
        Mostrar = True
        guitools.AddItem(item)

    if Mostrar:         
      guitools.CloseDirectory(ParentItem)
      

#Funcion especifica para importar el canal:----------->OK
def ImportarCanal(channel):
  channelmodule=""
  if os.path.exists(os.path.join( config.get_runtime_path(),"pelisalacarta","channels",channel+".py")):
    exec "from pelisalacarta.channels import "+channel+" as channelmodule"
  elif os.path.exists(os.path.join( config.get_runtime_path(),"pelisalacarta",channel+".py")):
    exec "from pelisalacarta import "+channel+" as channelmodule"
  elif os.path.exists(os.path.join( config.get_runtime_path(),"core",channel+".py")):
    exec "from core import "+channel+" as channelmodule"
  elif os.path.exists(os.path.join( config.get_runtime_path(),channel+".py")):
    exec "import "+channel+" as channelmodule"
  return channelmodule

#Sección encargada de comprobar las actualizaciones del plugin:----------->OK
def ActualizarPlugin():
  from core import updater
  logger.info("[launcher.py] - ActualizarPlugin")
  updater.checkforupdates()

   
   
#Función findvideos generica:----------->OK
def findvideos(item,channelitemlist=None):
    logger.info("findvideos")
    itemlist = []
    if channelitemlist==None:
      from core import scrapertools
      from servers import servertools
      from servers import longurl
      import copy
      data = scrapertools.cache_page(item.url)
      data=longurl.get_long_urls(data)  
      listavideos = servertools.findvideos(data)  
      for video in listavideos:
          NuevoItem = copy.deepcopy(item)
          NuevoItem.title = item.title
          NuevoItem.fulltitle = "Ver en: ["  + video[2] + "]"
          NuevoItem.url = video[1]
          NuevoItem.server = video[2]
          NuevoItem.action = "play"
          NuevoItem.folder=False
          itemlist.append(NuevoItem)
    else:
        import copy
        for itemvideo in channelitemlist:
            NuevoItem = copy.deepcopy(itemvideo)
            NuevoItem.fulltitle = itemvideo.title
            NuevoItem.title = item.title
            NuevoItem.thumbnail = item.thumbnail
            itemlist.append(NuevoItem)
        
    return itemlist


#Función para el menú de reproduccion:----------->OK
def play(item):
  itemlist = MenuVideo(item)
  if len(itemlist) >0:
    Resultado = MostrarMenuVideo(item,itemlist)
    if not Resultado == None:
      exec itemlist[Resultado].action+"(item, itemlist[Resultado])"
    else:
      play_video(item,None)


#Función para añadir una serie a la Libreria:----------->OK
def add_serie_to_library(item):
  from core import library
  channelmodule = ImportarCanal(item.channel)
  if item.extra: action = item.extra
  if item.refered_action: action = item.refered_action
  
  if "###" in action:
    item.extra = action.split("###")[1]
    action = action.split("###")[0]
  item.action = action
  
  nombre_fichero_config_canal = os.path.join( config.get_data_path() , "series.xml" )
  if not os.path.exists(nombre_fichero_config_canal):
      f = open( nombre_fichero_config_canal , "w" )
  else:
      f = open( nombre_fichero_config_canal , "r" )
      contenido = f.read()
      f.close()
      f = open( nombre_fichero_config_canal , "w" )
      f.write(contenido)

  f.write(item.serialize()+"\n")
  f.close();

  exec "itemlist = channelmodule."+action+"(item)"
  for episodio in itemlist:
    if episodio.action!="add_serie_to_library" and episodio.action!="download_all_episodes":
        episodio.category="Series"
        episodio.refered_action = action
        library.Guardar(episodio)
  guitools.Dialog_OK(config.get_localized_string(30101) , item.title +"\n"+ config.get_localized_string(30135)) # 'Se ha añadido a la Biblioteca'
  library.ActualizarBiblioteca(item)   

                   

#Función para descargar todos los episodios de una serie:----------->OK
def download_all_episodes(item):
    from servers import servertools
    from core import downloadtools
    from core import scrapertools

    # Esto es poco elegante...
    # Esta marca es porque el item tiene algo más aparte en el atributo "extra"
    if item.extra: action = item.extra
    if item.refered_action: action = item.refered_action
    if "###" in action:
      item.extra = action.split("###")[1]
      action = action.split("###")[0]    
        
    #Importamos el canal    
    channel = ImportarCanal(item.channel)
    
    #Ejecutamos la funcion
    exec "itemlist = channel."+action+"(item)"
    
    #Quitamos estos dos elementos de la lista (si los hay)
    for episodio in itemlist:
      if episodio.action=="add_serie_to_library" or episodio.action=="download_all_episodes":
        itemlist.remove(episodio)
    

    #Abrimos el dialogo
    pDialog = guitools.Dialog_Progress('pelisalacarta', 'Descargando ' + item.show)
    
    for x, episodio in enumerate(itemlist):
    
      #Si se presiona cancelar, se cancela
      if pDialog.iscanceled():
        return
      #Extraemos la Temporada y el Episodio  
      episodio.title = scrapertools.get_season_and_episode(episodio.title)
      
      #Actualizamos el progreso
      pDialog.Actualizar(((x)*100)/len(itemlist), 'Descargando ' + item.show, 'Descargando episodio: ' + episodio.title)

      # Extrae los mirrors
      if hasattr(channel, 'findvideos'):
          mirrors_itemlist = channel.findvideos(episodio)
      else:
          mirrors_itemlist = findvideos(episodio,episodio.channel)
      
      
      descargado = False
      
      #Descarga el primer mirror que funcione
      for mirror_item in mirrors_itemlist:
      
        if hasattr(channel, 'play'):
            video_items = channel.play(mirror_item)
        else:
            video_items = [mirror_item]
            
        if len(video_items)>0:
            video_item = video_items[0]
            
            # Comprueba que esté disponible
            video_urls, puedes, motivo = servertools.resolve_video_urls_for_playing( video_item.server , video_item.url , video_password="" , muestra_dialogo=False)
            
            # Lo descarga
            if puedes:
            
              # El vídeo de más calidad es el último
              devuelve = downloadtools.downloadbest(video_urls,item.show+" "+episodio.title+" ["+video_item.server+"]",continuar=False)
              if devuelve==0:
                  logger.info("[launcher.py] download_all_episodes - Archivo Descargado")
                  descargado = True
                  break
              elif devuelve==-1:
                  pDialog.Cerrar()
                  logger.info("[launcher.py] download_all_episodes - Descarga abortada")
                  guitools.Dialog_OK("pelisalacarta" , "La descarga ha sido cancelada")
                  return
              else:
                  continue
    pDialog.Cerrar()
    

###########################################################################
#                          MENU DE REPRODUCCIÓN                           #
#         ESPACIO ENCARGADO DEL MENÚ DE REPRODUCCIÓN DEL VÍDEO            #
#                        Y SUS DISTINTAS OPCIONES                         #
###########################################################################

#Función encargada de construir el menu de reproduccion de los videos:----------->OK
def MenuVideo(item):
    logger.info("[launcher.py] MenuVideo")
    
    # Lista de Opciones Disponibles
    OpcionesDisponibles =[]
    OpcionesDisponibles.append(config.get_localized_string(30151)) #"Ver el vídeo"
    OpcionesDisponibles.append(config.get_localized_string(30164)) #"Borrar este fichero"
    OpcionesDisponibles.append(config.get_localized_string(30153)) #"Descargar"
    OpcionesDisponibles.append(config.get_localized_string(30154)) #"Quitar de favoritos"
    OpcionesDisponibles.append(config.get_localized_string(30155)) #"Añadir a favoritos"
    OpcionesDisponibles.append(config.get_localized_string(30161)) #"Añadir a Biblioteca"
    OpcionesDisponibles.append(config.get_localized_string(30157)) #"Añadir a lista de descargas"
    OpcionesDisponibles.append(config.get_localized_string(30159)) #"Borrar descarga definitivamente"
    OpcionesDisponibles.append(config.get_localized_string(30160)) #"Pasar de nuevo a lista de descargas"
    OpcionesDisponibles.append(config.get_localized_string(30156)) #"Quitar de lista de descargas"
    OpcionesDisponibles.append(config.get_localized_string(30158)) #"Enviar a JDownloader"
    OpcionesDisponibles.append(config.get_localized_string(30158).replace("jDownloader","pyLoad")) # "Enviar a pyLoad"
    OpcionesDisponibles.append(config.get_localized_string(30162)) #"Buscar Trailer"
    
    
    itemlist = []
    if item.server=="": item.server="directo"   
    default_action = config.get_setting("default_action")
    
    # Extrae las URL de los vídeos, y si no puedes verlo te dice el motivo
    from servers import servertools
    video_urls,puedes,motivo = servertools.resolve_video_urls_for_playing(item.server,item.url,item.password, True)
    
 
    
    # Si puedes ver el vídeo, presenta las opciones
    if puedes:
      for video_url in video_urls:
        itemlist.append(Item(title=OpcionesDisponibles[0] + " " + video_url[0], url=video_url, action="play_video"))
        
      if item.server=="local":
        itemlist.append(Item(title=OpcionesDisponibles[1], url=video_urls, action="delete"))

      if not item.server=="local":
        itemlist.append(Item(title=OpcionesDisponibles[2], url=video_urls, action="download")) #"Descargar"

      if item.channel=="favoritos":
        itemlist.append(Item(title=OpcionesDisponibles[3], url=video_urls, action="remove_from_favorites")) #"Quitar de favoritos"
      
      if not item.channel=="favoritos":
        itemlist.append(Item(title=OpcionesDisponibles[4], url=video_urls, action="add_to_favorites"))  #"Añadir a favoritos"
      
      if not item.channel=="library":
        itemlist.append(Item(title=OpcionesDisponibles[5], url=video_urls, action="add_to_library")) #"Añadir a Biblioteca"
      if item.channel=="library":
        itemlist.append(Item(title="Quitar de la Biblioteca", url=video_urls, action="remove_from_library")) #"Añadir a Biblioteca"

      if not item.channel=="descargas":
        itemlist.append(Item(title=OpcionesDisponibles[6], url=video_urls, action="add_to_downloads")) #"Añadir a lista de descargas"
            
      if item.channel =="descargas" and item.category=="errores":
        itemlist.append(Item(title=OpcionesDisponibles[7], url=video_urls, action="remove_from_error_downloads")) #"Borrar descarga definitivamente"
        itemlist.append(Item(title=OpcionesDisponibles[8], url=video_urls, action="add_again_to_downloads")) #"Pasar de nuevo a lista de descargas"          
      if item.channel =="descargas" and item.category=="pendientes": 
        itemlist.append(Item(title=OpcionesDisponibles[9], url=video_urls, action="remove_from_downloads")) #"Quitar de lista de descargas"

      if config.get_setting("jdownloader_enabled")=="true": 
        itemlist.append(Item(title=OpcionesDisponibles[10], url=video_urls, action="send_to_jdownloader")) #"Enviar a JDownloader"
          
      if config.get_setting("pyload_enabled")=="true": 
        itemlist.append(Item(title=OpcionesDisponibles[11], url=video_urls, action="send_to_pyLoad")) #"Enviar a pyLoad"

      if not item.channel in ["trailertools","ecarteleratrailers"]: 
        itemlist.append(Item(title=OpcionesDisponibles[12], url=video_urls, action="search_trailer")) # "Buscar Trailer" 
        
    else:
        if item.server!="":
          guitools.Dialog_OK( "No puedes ver ese vídeo porque..." , motivo.replace("<br/>","\n") + "\n" + item.url)

        else:
            guitools.Dialog_OK("No puedes ver ese vídeo porque...","El servidor donde está alojado no está\nsoportado en pelisalacarta todavía\n"+url)

            if item.channel=="favoritos":
              itemlist.append(Item(title=OpcionesDisponibles[3], url=video_urls, action="remove_from_favorites")) #"Quitar de favoritos"
            if item.channel=="library":
              itemlist.append(Item(title="Quitar de la Biblioteca", url=video_urls, action="remove_from_library")) #"Añadir a Biblioteca"

            if item.channel =="descargas" and item.category=="errores":
              itemlist.append(Item(title=OpcionesDisponibles[7], url=video_urls, action="remove_from_error_downloads")) #"Borrar descarga definitivamente"         
            if item.channel =="descargas" and not item.category=="errores": 
              itemlist.append(Item(title=OpcionesDisponibles[9], url=video_urls, action="remove_from_downloads")) #"Quitar de lista de descargas"

    return itemlist


#Función encargada de Mostrar el Menú de Reproduccion y devolver la opción seleccionada:----------->OK
def MostrarMenuVideo(item,itemlist):
    opciones = []
    Reproducible = False
    seleccion = -1
    for itemopcion in itemlist:
      opciones.append(itemopcion.title)
      if itemopcion.action=="play": Reproducible = True

    if len(opciones)>0:    
      default_action = config.get_setting("default_action")
      if default_action=="0" or not Reproducible: #Preguntar
        seleccion =guitools.Dialog_Select(config.get_localized_string(30163), opciones)
      elif default_action=="1": #Ver en Calidad Baja
          seleccion = 0
      elif default_action=="2": #Ver en Calidad Alta
          seleccion = len(video_urls)-1
      elif default_action=="3": #Mandar a jDownloader
        if config.get_setting("jdownloader_enabled")=="true":
          seleccion = opciones.index(OpcionesDisponibles[10])
      else:
          seleccion=0
    return seleccion


#Función para descargar un vídeo:----------->OK
def download(item, VideoItem = None): 
  from core import descargas
  item.title = guitools.Keyboard(item.title)
  if item.title:
    devuelve = descargas.download(item)
    if devuelve==0: guitools.Dialog_OK("pelisalacarta" , "Descargado con éxito")
    elif devuelve==-1: guitools.Dialog_OK("pelisalacarta" , "Descarga cancelada")
    else: guitools.Dialog_OK("pelisalacarta" , "Error en la descarga")


#Función para añadir un vídeo a Favoritos:----------->OK
def add_to_favorites(item, VideoItem = None):
  from core import favoritos
  item.title = guitools.Keyboard(item.title)
  if item.title:
    item.fulltitle=""
    favoritos.GuardarFavorito(item)
    guitools.Dialog_OK(config.get_localized_string(30102) , item.title + "\n" + config.get_localized_string(30108)) # 'se ha añadido a favoritos'


#Función para añadir un vídeo a la Librería:----------->OK
def add_to_library(item, VideoItem = None): 
  from core import library
  item.title = guitools.Keyboard(item.title)
  if item.title:
    library.Guardar(item)
    guitools.Dialog_OK(config.get_localized_string(30101) , item.title +"\n"+ config.get_localized_string(30135)) # 'Se ha añadido a la Biblioteca'
    library.ActualizarBiblioteca(item) 


#Función para borrar un vídeo de la Librería:----------->OK
def remove_from_library(item, VideoItem = None): 
    from core import library
    library.Borrar(item)
    library.ActualizarBiblioteca(item)    
    
    
#Función para añadir un vídeo a la Lista de Descargas:----------->OK
def add_to_downloads(item, VideoItem = None): 
  from core import descargas
  item.title = guitools.Keyboard(item.title)
  if item.title:
    item.fulltitle=""
    descargas.GuardarDescarga(item)
    guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + config.get_localized_string(30109)) # 'se ha añadido a la lista de descargas'


#Función para envíar un vídeo a jDownloader:----------->OK pendiente añadir user y password a la config
def send_to_jdownloader(item, VideoItem = None): 
    from core import scrapertools
    import urllib
    import base64
    User=config.get_setting("jdownloader_user")
    Password=config.get_setting("jdownloader_password")
    headers=[]
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"])
    headers.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
    headers.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])
    headers.append(["Accept-Encoding","gzip, deflate"])
    headers.append(["Authorization","Basic " + base64.b64encode(User + ":" + Password)])
    headers.append(["Content-Type","application/x-www-form-urlencoded"])
    url=config.get_setting("jdownloader")+"/link_adder.tmpl"
    Descargas = VideoItem.url[0][1]
    logger.info(Descargas)
    if item.thumbnail: Descargas = Descargas + "\n" + item.thumbnail
    if item.subtitle: Descargas = Descargas + "\n" + item.subtitle
    try:
      data = scrapertools.downloadpage(url,headers=headers,post="do=Add&addlinks="+ urllib.quote_plus(Descargas))
      guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + "Se ha enviado a jDownloader")
    except:
      guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + "No se ha podido enviar a jDownloader")
    
    

#Función para envíar un vídeo a pyLoad:----------->OK
def send_to_pyLoad(item, VideoItem = None):    
  logger.info("Opcion seleccionada: Enviar a pyLoad" )
  if item.show!="":
      package_name = item.show
  else:
      package_name = item.title
  from core import pyload_client
  pyload_client.download(url=VideoItem.url[0][1],package_name=package_name)
  if item.thumbnail: pyload_client.download(url=item.thumbnail,package_name=package_name)
  if item.subtitle: pyload_client.download(url=item.subtitle,package_name=package_name)
  guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + "Se ha enviado a pyLoad")



#Función para buscar un Trailer:----------->OK
def search_trailer(item, VideoItem = None): 
  logger.info("Opcion seleccionada: Buscar Trailer" )
  item.title = guitools.Keyboard(item.title)
  if item.title:
    item.channel="trailertools"
    item.action="buscartrailer"
    guitools.Update(item)


#Función para eliminar un vídeo de Favoritos:----------->OK
def remove_from_favorites(item, VideoItem = None): 
  from core import favoritos
  favoritos.BorrarFavorito(item)

  guitools.Dialog_OK(config.get_localized_string(30102) , item.title + "\n" + config.get_localized_string(30105)) # 'Se ha quitado de favoritos'
  guitools.Refresh()


#Función para eliminar un vídeo de la Lista de Descargas:----------->OK
def remove_from_downloads(item, VideoItem = None):
  from core import descargas
  # La categoría es el nombre del fichero en la lista de descargas
  descargas.BorrarDescarga(item)
  guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + config.get_localized_string(30106)) # 'Se ha quitado de lista de descargas'
  guitools.Refresh()


#Función para eliminar un vídeo de Descargas con error:----------->OK
def remove_from_error_downloads(item, VideoItem = None): 
  from core import descargas
  descargas.delete_error_bookmark(item)
  guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + config.get_localized_string(30106)) # 'Se ha quitado de la lista'
  guitools.Refresh()


#Función para añadir de nuevo un vídeo a Descargas desde Descargas con error:----------->OK
def add_again_to_downloads(item, VideoItem = None): 
  from core import descargas
  descargas.mover_descarga_error_a_pendiente(item)
  guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + config.get_localized_string(30107)) # 'Ha pasado de nuevo a la lista de descargas'
  guitools.Refresh()


#Función para eliminar un vídeo de descargado:----------->OK
def delete(item, VideoItem = None): 
  os.remove(item.url)
  tbn = os.path.splitext(item.url)[0]+".tbn"
  if os.path.exists(tbn):
    os.remove(tbn)
  nfo = os.path.splitext(item.url)[0]+".nfo"
  if os.path.exists(nfo):
    os.remove(nfo)
  guitools.Refresh() 


#Función encargada de reproducir un vídeo:----------->OK
def play_video(item, VideoItem = None):
  if item.server == "torrent":
    if VideoItem is not None:
      from core import torrent_player
      torrent_player.download(item, VideoItem, True)
  else:
    guitools.play(item, VideoItem)
