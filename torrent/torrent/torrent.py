# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib2
sys.path.append("lib")
import bencode
import libtorrent as lt 
Time = 0

#Mostrar el progreso
def Progreso(session,torrent,url):
  os.system('cls' if os.name == 'nt' else 'clear')
  s= torrent.status()
  if session.dht_state() is not None:
      DHT=str(session.status().dht_nodes)
  else:
      DHT="inactivo"
      
  DHT_peers = 0
  TRK_peers = 0
  PEX_peers = 0
  LSD_peers = 0
  
  for peer in torrent.get_peer_info():   
    if peer.source & 1:
      TRK_peers +=1
    if peer.source & 2:
      DHT_peers +=1
    if peer.source & 4:
      PEX_peers +=1
    if peer.source & 8:
      LSD_peers +=1    
      
  TORRENT_tracker = 0
  ADDED_tracker = 0
  MAGNET_tracker = 0
  TEX_tracker = 0
  trackers= 0 

  for tracker in torrent.trackers():
    trackers+=1
    if tracker["source"] & 1:
      TORRENT_tracker +=1
    if tracker["source"] & 2:
      ADDED_tracker +=1
    if tracker["source"] & 4:
      MAGNET_tracker +=1
    if tracker["source"] & 8:
      TEX_tracker +=1    
  
  Estados = ['En Cola', 'Comprobando', 'Descargando Metadatos', 'Descargando', 'Finalizado', 'Seeding', 'Allocating', 'Checking fastresume']
  Mensaje  = "Tiempo: %s\n\n"
  Mensaje += 'Estado: %.1f%% - %s \n'
  Mensaje += 'Descarga:%.1f kb/s Subida:%.1f kB/s \n'
  Mensaje += 'Peers:%d Seeds:%d Nodos DHT:%s Trackers: %i\n\n' 
  Mensaje += 'DHT-Peers:%d TRK-Peers:%d PEX-Peers:%d LSD-Peers:%d\n'
  Mensaje += 'Torrent-Trackers:%d Added-Trackers:%d Magnet-Trackers:%d TEX-Trackers:%d\n'

  Mensaje  = Mensaje % (time.strftime("%H:%M:%S", time.gmtime(time.time() - Time)),s.progress * 100, Estados[s.state], s.download_rate / 1000, s.upload_rate / 1000,s.num_peers, s.num_seeds,DHT,trackers,DHT_peers,TRK_peers,PEX_peers,LSD_peers,TORRENT_tracker,ADDED_tracker,MAGNET_tracker,TEX_tracker)
  Progreso = int(s.progress * 100)
  print ( Mensaje)
  
  if torrent.has_metadata():
    info = torrent.get_torrent_info()
    files = []
    for x, f in enumerate(info.files()):
     files.append(f.path)
     if f.path.endswith(".txt"):
      torrent.file_priority(x,1)
     else:
      torrent.file_priority(x,0)
    files.sort(key=lambda item: len(item.split("\\")))
    print files[0]
  print ("Presiona Ctrl+C para detener")



if __name__ == "__main__":

  #Enlaces magnet:
  
  '''Enlace Magnet'''
  url = "magnet:?xt=urn:btih:ji5sehfjxcmuim45djsayd5wboobfn6a&dn=Cenicienta (HDTV-Screener)_(aquitorrent)&tr=http://tracker.torrentbay.to:6969/announce"
  #url = "magnet:?xt=urn:btih:873544be4a75827dd3bdbd0b8aab9a5ab4e42a8c&dn=Dragon+Ball+Z+Remastered+Season+1-9+%2B+Movies+Pack&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969"

  '''Enlace Torrent'''
  #url = "http://www.elitetorrent.net/get-torrent/27128"

  '''Torrent en HDD'''
  #url = "pelicula.torrent"
  
  
  if len(sys.argv) >1:
    url = sys.argv[1]
    
  #Creamos la sesion
  session = lt.session()
  settings = session.settings()
  settings.stop_tracker_timeout = 5
  session.set_settings(settings)
  session.stop_dht()
  session.listen_on(0,0)
  session.add_dht_router("router.bittorrent.com",6881)
  session.add_dht_router("router.utorrent.com",6881)
  session.add_dht_router("router.bitcomet.com",554)
  session.start_dht()

  #Añadimos el torrent
  if not url.startswith("magnet:" ):
    if os.path.isfile(url):
      f = open(url,'rb')
      data = f.read()
      info = lt.torrent_info(bencode.bdecode(data))
      f.close()
    else:
      data = urllib2.urlopen(url).read()
      info = lt.torrent_info(bencode.bdecode(data))
    
    torrent = session.add_torrent({'ti':info     , 'save_path':'.', 'storage_mode':lt.storage_mode_t.storage_mode_allocate})
  else:
    
    torrent = session.add_torrent({'url':url, 'save_path':'.', 'storage_mode':lt.storage_mode_t.storage_mode_allocate})
  '''  
  torrent.add_tracker({"url" : "http://exodus.desync.com:6969/announce"})
  torrent.add_tracker({"url" : "udp://tracker.publicbt.com:80/announce"})
  torrent.add_tracker({"url" : "udp://tracker.openbittorrent.com:80/announce"})
  torrent.add_tracker({"url" : "http://tracker.torrentbay.to:6969/announce"})
  torrent.add_tracker({"url" : "http://fr33dom.h33t.com:3310/announce"})
  torrent.add_tracker({"url" : "http://tracker.pow7.com/announce"})
  torrent.add_tracker({"url" : "udp://tracker.publicbt.com:80/announce"})
  torrent.add_tracker({"url" : "udp://tracker.ccc.de:80/announce"})
  torrent.add_tracker({"url" : "http://tracker.bittorrent.am:80/announce"})
  torrent.add_tracker({"url" : "http://denis.stalker.h3q.com:6969/announce"})
  torrent.add_tracker({"url" : "udp://tracker.prq.to:80/announce"})
  torrent.add_tracker({"url" : "udp://tracker.istole.it:80/announce"})
  torrent.add_tracker({"url" : "udp://open.demonii.com:1337"})
  torrent.add_tracker({"url" : "http://9.rarbg.com:2710/announce"})
  torrent.add_tracker({"url" : "http://announce.torrentsmd.com:6969/announce"})
  torrent.add_tracker({"url" : "http://bt.careland.com.cn:6969/announce"})
  torrent.add_tracker({"url" : "http://explodie.org:6969/announce"})
  torrent.add_tracker({"url" : "http://mgtracker.org:2710/announce"})
  torrent.add_tracker({"url" : "http://tracker.best-torrents.net:6969/announce"})
  torrent.add_tracker({"url" : "http://tracker.tfile.me/announce"})
  torrent.add_tracker({"url" : "http://tracker.torrenty.org:6969/announce"})
  torrent.add_tracker({"url" : "http://tracker1.wasabii.com.tw:6969/announce"})
  torrent.add_tracker({"url" : "udp://9.rarbg.com:2710/announce"})
  torrent.add_tracker({"url" : "udp://9.rarbg.me:2710/announce"})
  torrent.add_tracker({"url" : "udp://coppersurfer.tk:6969/announce"})
  torrent.add_tracker({"url" : "udp://tracker.btzoo.eu:80/announce"})
  '''
  Time = time.time()
  #Descarga secuencial
  torrent.set_sequential_download(True)
  torrent.force_reannounce()
  torrent.force_dht_announce()

  try: 
    #Esperamos a los metadatos
    while not torrent.has_metadata():
      time.sleep(0.5)
      Progreso(session,torrent,url)
    #Obtenemos la info del Torrent
    if torrent.has_metadata():
      info = torrent.get_torrent_info()
           
      #Buscamos el archivo del vídeo, en principio es el de mayor tamaño.
      
      video_file_size=0
      for f in info.files():
        if f.size > video_file_size:
          video_file_size = f.size
          video_file_path = f.path.decode("utf8")
          video_file = os.path.basename(video_file_path)
      
      
      #Loop para controlar la descarga
      while (not torrent.is_seed()):
          time.sleep(0.5)
          Progreso(session,torrent,url)
      

    session.remove_torrent(torrent,1)
      
    del session
    del lt
      
  except KeyboardInterrupt:
    print "Eliminando datos descargados..."
    session.remove_torrent(torrent,1)
    print "Eliminando sesion..."
    del session


  


