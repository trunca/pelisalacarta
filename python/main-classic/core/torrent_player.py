# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# cliente torrent para pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys
import time
from platformcode import platformtools
from core import scrapertools
from core import config
from core import logger
from core.item import Item
import bencode
import socket
__module__ = "Torrent"




def download(item, Reproducir =  False):
    logger.info("[torrent_player.py] - play")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
    local_ip_address = s.getsockname()[0]
    
    try:
      PorcentajeInicio = int(config.get_setting("porcentaje_torrent"))
    except:
      PorcentajeInicio = 5
      
    video_file_path = ""
    video_file = ""
    video_file_size = 0
    Cancelado = False

    #importa la libreria si no la encuentra sale de la funcion
    lt = libtorrent()
    if lt is None:
      return -2
      
    #Para enlaces de EliteTorrent y quiza otros
    import HTMLParser
    item.url =  HTMLParser.HTMLParser().unescape(item.url)
    
    
    #Creamos el directorio
    save_path_videos = os.path.join( config.get_setting("downloadpath") , "Torrent")
    if not os.path.exists(save_path_videos): os.mkdir(save_path_videos)
    
    #Creamos la sesion
    session = lt.session()
    settings = session.settings()
    settings.stop_tracker_timeout = 5
    session.set_settings(settings)
    session.stop_dht()
    
    session.add_dht_router("router.bittorrent.com",6881)
    session.add_dht_router("router.utorrent.com",6881)
    session.add_dht_router("router.bitcomet.com",554)
    session.start_dht(None)
    session.listen_on(0,0,local_ip_address)

    #Añadimos el torrent
    if not item.url.startswith("magnet:" ):
      if os.path.isfile(item.url):
        data = open(url,'rb').read()
        info = lt.torrent_info(bencode.bdecode(data))
      else:
        data = scrapertools.downloadpage(item.url)
        info = lt.torrent_info(bencode.bdecode(data))
      
      torrent = session.add_torrent({'ti':info     , 'save_path':save_path_videos, 'storage_mode':lt.storage_mode_t.storage_mode_sparse})
    else:
      torrent = session.add_torrent({'url':item.url, 'save_path':save_path_videos, 'storage_mode':lt.storage_mode_t.storage_mode_sparse})

    #Descarga secuencial
    torrent.set_sequential_download(True)

    Time = time.time()
    pDialog = platformtools.ProgressDialog(__module__,"Iniciando descarga...")
    
    #Esperamos a los metadatos
    while not torrent.has_metadata():
      time.sleep(1)
      if pDialog.iscanceled():
          pDialog.close()
          Cancelado =True
          break
      Progreso(session,torrent,pDialog,Time,0)
      
    #Obtenemos la info del Torrent
    if torrent.has_metadata():
      info = torrent.get_torrent_info()
      VideoFiles=[]
      SrtFiles=[]
      Files = []
      for f in info.files():
        Size = 0
        for file in Files:
          Size += file["Size"]

        Start = int(Size / info.piece_length())
        End = int((Size + f.size) / info.piece_length()) 
        Files.append({"Start":Start, "End" : End, "Size": f.size, "Path" : f.path})
        
        
      VideoExtensions =  ["avi", "mp4", "mkv", "flv", "mpeg", "ts"]  
      
      for file in Files:
        if file["Path"].split(".")[len( file["Path"].split("."))-1].lower() in VideoExtensions:
          VideoFiles.append(file)

        elif file["Path"].split(".")[len(file["Path"].split("."))-1].lower() =="srt":
         SrtFiles.append(file)

          
      item.video_url = os.path.join(save_path_videos, VideoFiles[0]["Path"])
      item.server="Directo"
      
      
      #Loop para controlar la descarga
      ReproduccionIniciada = False
      IniciarAutomatico = Reproducir
      
      while (not torrent.is_seed()):
          time.sleep(1)
          VideoFile = VideoFiles[0]
              
          #Los Srt Primero      
          if len(SrtFiles):
            SrtFile = SrtFiles[0]
            for x in range(SrtFile["Start"],SrtFile["End"]- SrtFile["Start"] +1):
              torrent.piece_priority(x,7)
          Progreso(session,torrent,pDialog,Time)
          
          #Si se cierra el reproductor, vuelve a mostrar el progreso
          if not platformtools.IsPlaying() and ReproduccionIniciada:
            ReproduccionIniciada = False
            IniciarAutomatico = False
            pDialog = platformtools.ProgressDialog(__module__,"")
            Progreso(session,torrent,pDialog,Time)

          #Para cancelar la descarga
          if not platformtools.IsPlaying() and pDialog.iscanceled():
            pDialog.close()
            Respuesta = platformtools.YesNoDialog(__module__,"Presione 'Si' para cancelar la descarga y 'No' para cerrar el dialogo e iniciar la reproduccion.")
            
            if Respuesta == True:
              Cancelado =True
              break;           
            else:
              ReproduccionIniciada =True
              platformtools.PlayVideo(item)
              
              
           
          #Para reproducir el vídeo    
          if torrent.status().state ==3 and  (torrent.status().progress * 100) >= PorcentajeInicio and not platformtools.IsPlaying() and IniciarAutomatico and not ReproduccionIniciada:
            logger.info("[torrent_player.py] - Iniciando reproduccion")
            pDialog.close()
            ReproduccionIniciada = True
            platformtools.PlayVideo(item)



    #Si llega aqui es porque se ha cancelado o porque la descarga ha terminado.
    #si se esta reprodciendo se espera.
    while platformtools.IsPlaying():
      time.sleep(1)

    
    #Si era una reproduccion, pregunta si desea eliminar los datos descargados
    if Reproducir:
      pDialog.close()
      Respuesta = platformtools.YesNoDialog(__module__,"Eliminar los datos descargados?")
      pDialog = platformtools.ProgressDialog(__module__,"")
      pDialog.update(25, "Deteniendo Torrent")
      if Respuesta ==True:
        session.remove_torrent(torrent,1)
      else:
        session.remove_torrent(torrent,0)
      pDialog.update(50, "Eliminando sesion")
      del session
      pDialog.update(75, "Deteniendo libtorrent")
      del lt
      pDialog.close()
      if Respuesta ==True:
        platformtools.AlertDialog(__module__, 'Torrent eliminado y datos borrados.')
    
    #Si era una descarga, detiene el torrent.
    else:
      pDialog = platformtools.ProgressDialog(__module__,"")
      pDialog.update(25, "Deteniendo Torrent")
      session.remove_torrent(torrent,0)
      pDialog.update(50, "Eliminando sesion")
      del session
      pDialog.update(75, "Deteniendo libtorrent")
      del lt
      
      #Si la descarga se ha completado, la mueve a la carpeta descargas
      if not Cancelado:
        '''
        RutaArchivo = os.path.join(config.get_setting("downloadpath"),item.title + "." + video_file.split(".")[len(video_file.split("."))-1] )
        if os.path.exists(RutaArchivo):
          os.remove(RutaArchivo)
        if os.path.exists(os.path.join(save_path_videos,video_file_path)):
          os.rename(os.path.join(save_path_videos,video_file_path), RutaArchivo )
          import shutil
          shutil.rmtree(os.path.join(save_path_videos,video_file_path.replace(save_path_videos,"").replace(video_file,"")))
        '''  
        pDialog.close()
        return 0
        
      else:
        pDialog.close()
        return -1
     
      


def Progreso(session,torrent,pDialog,Time):
  s= torrent.status()
  if session.dht_state() is not None:
      DHT=str(session.status().dht_nodes)
  else:
      DHT="inactivo"  

  trackers= 0 

  for tracker in torrent.trackers():
    trackers+=1

  Estados = ['En Cola', 'Comprobando', 'Descargando Metadatos', 'Descargando', 'Finalizado', 'Seeding', 'Allocating', 'Checking fastresume']
  Mensaje  = 'Tiempo: %s Estado: %.1f%% - %s\n'
  Mensaje += 'Descarga:%.1f kb/s Subida:%.1f kB/s \n'
  Mensaje += 'Peers:%d Seeds:%d Nodos DHT:%s Trackers: %i' 

  Mensaje  = Mensaje % (time.strftime("%H:%M:%S", time.gmtime(time.time() - Time)),s.progress * 100, Estados[s.state], s.download_rate / 1000, s.upload_rate / 1000,s.num_peers, s.num_seeds,DHT,trackers)
  Progreso = int(s.progress * 100)
  pDialog.update(Progreso, Mensaje)
  
def libtorrent():
  try:
  
    import libtorrent as lt
    if not lt.version in ["0.14.10.0","0.16.10.0", "0.15.10.0", "0.16.18.0"]:
        platformtools.AlertDialog("Torrent","La versión de libtorrent instalada es: " + lt.version + "\nNo se garantiza su funcionamento con esta versión")

  except (ImportError): 
    platformtools.AlertDialog("Error","No se ha podido localizar la libreria libtorrent, asegurate de que la tienes instalada correctamente.")
    return None
  return lt
