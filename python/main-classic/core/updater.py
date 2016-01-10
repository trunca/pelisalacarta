# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Updater
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#----------------------------------------------------------------------
import os
import json
import time
import re
from core import scrapertools
from core import config
from core import logger
from core.item import Item
from platformcode import platformtools

__channel__ = "updater"

headers = [["User-Agent", "pelisalacarta"]] 
repo = "tvalacarta/pelisalacarta"
branch = "master"
GitApi = "https://api.github.com/repos/"+repo+"/contents/python/main-classic/%s?ref="+branch
DownloadUrl = "https://raw.githubusercontent.com/"+repo+"/master/python/main-classic/%s?ref=" + branch

def isGeneric():
    return True
    
def mainlist(item):
    itemlist = []
    itemlist.insert(0,Item(action="refresh",title="Buscar actualizaciones de nuevo",channel =__channel__ ))
    CacheUpdate = get_cache_updates()
    if len(CacheUpdate) > 0:
      progress = platformtools.ProgressDialogBG("Pelisalacarta","")   
      
      keys = sorted(CacheUpdate, key = lambda key: CacheUpdate[key]["name"])
      for sha in keys:
        progress.update((keys.index(sha)+1) *100 / len(CacheUpdate),"Procesando: " + CacheUpdate[sha]["name"] )
        #update  = get_cache_update(sha)
        update =  CacheUpdate[sha]
        if update["type"] =="channel":
          title = "[Canal]"
          #plot= update["data"]["channel"]["changes"].encode("utf8")
          plot=""
        if update["type"] =="server":
          title = "[Servidor]" 
          plot=""  
        if update["change"] =="added":
          title += " [Nuevo]"
        if update["change"] =="modified":
          title += " [Actualizado]"         
        title+= " " + update["name"].encode("utf8")
        extra = sha
        itemlist.append(Item(action="download",title=title, plot=plot ,channel =__channel__, extra=extra))
      progress.close()
      
    if len(itemlist)>1:
      itemlist.insert(1,Item(action="download_all",title="Actualizar todo",channel =__channel__ ))
    else:
      itemlist.append(Item(title="¡No hay actualizaciones!"))
          
    return itemlist

def refresh(item):
  CheckFiles(True)
  platformtools.ItemlistRefresh()   

def download_all(item):
  time.sleep(1)
  download_all_updates()
  platformtools.AlertDialog("pelisalacarta","Descarga completada")
  platformtools.ItemlistRefresh()
  
  
def download(item):
  sha = item.extra
  update  = get_cache_update(sha)
  if update["type"] == "channel":
    info = "Version: " + update["data"]["channel"]["version"] + "\n"
    info +="Cambios: " + update["data"]["channel"]["changes"]
  else:
    info = "Version: " + "No Disponible" + "\n"
    info +="Cambios: " + "No Disponible"

  if platformtools.YesNoDialog("Actualizar " + update["name"].encode("utf8"),info):
    download_update(update) 
    platformtools.AlertDialog("pelisalacarta","Descarga completada")
    platformtools.ItemlistRefresh()



def download_all_updates():
  progreso = platformtools.ProgressDialog("Actualizando","")
  CacheUpdate = read_cache()
  keys = sorted(CacheUpdate, key = lambda key: CacheUpdate[key]["name"])
  cantidad = len(CacheUpdate)
  for sha in keys:
    update  = get_cache_update(sha) 
    percent = (keys.index(sha)+1) *100 / cantidad
    if progreso.iscanceled(): 
      progreso.close()
      return
    if update["type"] == "channel":
      progreso.update(percent,"Descargando canal: " + update["name"])
      download_update(update)
    if update["type"] == "server":
      progreso.update(percent,"Descargando servidor: " + update["name"])
      download_update(update)
      
  progreso.close()

      
def download_update(update):
  if update["type"] == "server":
    file = update["name"] + ".py"
    try:
      data = download_file(DownloadUrl % ("servers/"+file))
    except:
       platformtools.AlertDialog("pelisalacarta","Se ha producido un error al descargar los datos\nIntentalo de nuevo mas tarde")
    else:
      open(os.path.join(config.get_runtime_path(),"servers",file),"wb").write(data)
      remove_cache_update(update["sha"])
      


  if update["type"] == "channel":
    file = update["name"] + ".py"
    try:
      data = download_file(DownloadUrl % ("channels/"+file))
    except:
       platformtools.AlertDialog("pelisalacarta","Se ha producido un error al descargar los datos\nIntentalo de nuevo mas tarde")
    else:
      open(os.path.join(config.get_runtime_path(),"channels",file),"wb").write(data)
      
      file = update["name"] + ".xml"
      try:
        data = download_file(DownloadUrl % ("channels/"+file))
      except:
         platformtools.AlertDialog("pelisalacarta","Se ha producido un error al descargar los datos\nIntentalo de nuevo mas tarde")
      else:
        open(os.path.join(config.get_runtime_path(),"channels",file),"wb").write(data)    
        remove_cache_update(update["sha"])
      


def download_file(url):
  for x in range(10):
    try:
      data = scrapertools.downloadpage(url)
      assert data
      return data
    except:
      logger.info("No se ha podido descargar: " + url + " (intento " + str(x) + " de 10)" )
    else:
      break
  else:
      logger.info("Ha sido imposible descargar: " + url)
      logger.info("Abortando")
      raise Exception("File not downloaded")
      
      
      
'''
Funciones para manejar el cache de las actualizaciones.

Funcion:  Guarda todas las actualizaciones disponibles despues de una busqueda en un fichero json
          para poder acceder a ellas tantas veces como necesitemos sin tener que volver a descargar datos
          despues de instalar la actualización se borra del cache
           
Uso:      add_cache_update(Json, change, type)      <- Añade una nueva actualizacion al cache
          remove_cache_update(sha)                  <- Elimina una actualizacion del cache
          get_cache_update(sha)                     <- Obtiene una actualización del cache

'''
def read_cache():
  if os.path.exists(os.path.join(config.get_data_path(),"updates.json")):
    try:
      CacheUpdate=json.loads(open(os.path.join(config.get_data_path(),"updates.json"),"r").read())
    except:
      CacheUpdate = {}
  else:
    CacheUpdate = {}
  return CacheUpdate

def add_cache_update(Json, change, type):
  CacheUpdate = read_cache()
  if not Json["sha"] in CacheUpdate:
    CacheUpdate[Json["sha"]] = {}
    CacheUpdate[Json["sha"]]["name"] = Json["name"]
    CacheUpdate[Json["sha"]]["sha"] = Json["sha"]
    CacheUpdate[Json["sha"]]["change"] = change
    CacheUpdate[Json["sha"]]["type"] = type
    open(os.path.join(config.get_data_path(),"updates.json"),"w").write(json.dumps(CacheUpdate, indent=4, sort_keys=True))
    
    
def remove_cache_update(sha):
  CacheUpdate = read_cache()
  if sha in CacheUpdate:
   del CacheUpdate[sha]
   open(os.path.join(config.get_data_path(),"updates.json"),"w").write(json.dumps(CacheUpdate, indent=4, sort_keys=True))

  
def get_cache_update(sha):
  CacheUpdate = read_cache()
  if not "data" in CacheUpdate[sha] and CacheUpdate[sha]["type"]=="channel":
    dataurl = DownloadUrl % ("channels/"+CacheUpdate[sha]["name"] + ".xml")
    data = scrapertools.downloadpage(dataurl)
    CacheUpdate[sha]["data"] = xml2json(data)
    open(os.path.join(config.get_data_path(),"updates.json"),"w").write(json.dumps(CacheUpdate, indent=4, sort_keys=True))
  return CacheUpdate[sha]
  
def get_cache_updates():
  CacheUpdate = read_cache()
  channel_list = get_channels_list()
  server_list = get_servers_list()
  shas = CacheUpdate.keys()
  for sha in shas:
    if CacheUpdate[sha]["type"]=="channel":
      if CacheUpdate[sha]["change"]=="added" and CacheUpdate[sha]["name"] in channel_list:
        CacheUpdate[sha]["change"]="modified"
      if CacheUpdate[sha]["change"]=="modified" and not CacheUpdate[sha]["name"] in channel_list:
        CacheUpdate[sha]["change"]="added"
      if CacheUpdate[sha]["change"]=="modified" and channel_list[CacheUpdate[sha]["name"]]["sha"] == sha:
        del CacheUpdate[sha]
      continue
    if CacheUpdate[sha]["type"]=="server":
      if CacheUpdate[sha]["change"]=="added" and CacheUpdate[sha]["name"] in server_list:
        CacheUpdate[sha]["change"]="modified"
      if CacheUpdate[sha]["change"]=="modified" and not CacheUpdate[sha]["name"] in server_list:
        CacheUpdate[sha]["change"]="added"
      if CacheUpdate[sha]["change"]=="modified" and server_list[CacheUpdate[sha]["name"]]["sha"] == sha:
        del CacheUpdate[sha]

  open(os.path.join(config.get_data_path(),"updates.json"),"w").write(json.dumps(CacheUpdate, indent=4, sort_keys=True))
  return CacheUpdate
 
 
'''
Funciones para comprobar las actualizaciones de forma automatica al entrar en pelisalacarta.

Funcion:  Comprueba si hay actualizaciones, y actua en funcion de la configuracion:
          1. Si estan activadas las actualizaciones del plugin:
            Comprueba si hay una nueva version y te pregunta si instalarla.
            
          2. Si estan activadas las actualizaciones de canales:
            Comprueba si hay actualizaciones de canales o servidores.
            
              2.1 Si esta en modo "Auto":
                Las Instala.
                
              2.2 Si esta en modo "Preguntar":
                Te pregunta si instalarlas.
                
              2.2 Si esta en modo "Elegir":
                Te avisa que hay actualizaciones, y que vayas al canal "Actualizaciones para ver mas detalles"
                
Uso:      checkforupdates()  <- Comprueba las actualizaciones en segundo plano

'''
def checkforupdates():
  from threading import Thread
  Thread(target=Threaded_checkforupdates).start()

def Threaded_checkforupdates():
  logger.info("checkforupdates")
  import time
  #Actualizaciones del plugin
  if config.get_setting("updateplugin") == "true":
    logger.info("Comprobando actualizaciones de pelisalcarta")
    
    LOCAL_VERSION_FILE = open(os.path.join(config.get_runtime_path(), "version.xml" )).read()
    #REMOTE_VERSION_FILE = scrapertools.downloadpage(DownloadUrl % "bin/version.xml")
    REMOTE_VERSION_FILE = scrapertools.downloadpage("http://descargas.tvalacarta.info/pelisalacarta-version.xml")
    
    try:
      versiondescargada = scrapertools.get_match(REMOTE_VERSION_FILE,"<tag>([^<]+)</tag").strip()
    except:
      versiondescargada = "0.0.0"
      
    versionlocal = scrapertools.get_match(LOCAL_VERSION_FILE,"<tag>([^<]+)</tag")  
        
    logger.info("Versión local: " + versionlocal)
    logger.info("Versión remota: " + versiondescargada)
    
    from distutils.version import StrictVersion
    if StrictVersion(versiondescargada) > StrictVersion(versionlocal):
      if platformtools.YesNoDialog("pelisalacarta","¡Hay una nueva versión lista para descargar!\nVersión actual: "+versionlocal+" - Nueva versión: "+versiondescargada+"\nQuieres instalarla ahora?"):
        update(versiondescargada)
        return
      else:
       logger.info("Opción seleccionada: No Descargar")
  #Actualizacion de canales      
  if config.get_setting("updatechannels") == "true":
    CheckFiles()

def CheckFiles(channelmode=False):
  logger.info("CheckFiles")
  progress = platformtools.ProgressDialogBG("Pelisalacarta","Comprobando actualizaciones...")
  progress.update(50, "Descargando lista de canales...")
  
  RemoteJSONData = json.loads(scrapertools.downloadpage(GitApi %("channels"), headers=headers))
  LocalJSONData = get_channels_list()
  

  for file in RemoteJSONData:
    if file["name"].endswith(".xml"):
      file["name"] = file["name"][:-4]
      if not file["name"] in LocalJSONData:
        add_cache_update(file, "added", "channel")
      elif file["sha"] <> LocalJSONData[file["name"]]["sha"]:
        add_cache_update(file, "modified", "channel")
        
  progress.update(100, "Descargando lista de servidores...")
  RemoteJSONData = json.loads(scrapertools.downloadpage(GitApi %("servers"), headers=headers))
  LocalJSONData = get_servers_list()
  
  for file in RemoteJSONData:
    if file["name"].endswith(".py") and not file["name"] in ["__init__.py"]:
      file["name"] = file["name"][:-3]
      if not file["name"] in LocalJSONData:
        add_cache_update(file, "added", "server")
      elif file["sha"] <> LocalJSONData[file["name"]]["sha"]:
        add_cache_update(file, "modified", "server")

  if channelmode: 
    progress.close()
    return
  
  #Si todo esta al dia:
  CacheUpdate = get_cache_updates()
  if len(CacheUpdate) == 0:
    progress.update(100, "Todos los canales y servidores estan actualizados")
    time.sleep(1)
    progress.close()
        
  #Si hay actualizaciones
  else:
    progress.update(100, "Hay actualizaciones disponibles")
    time.sleep(1)
    progress.close()
      
    if config.get_setting("updatemode") =="0": #Automatico
      download_all_updates()
         
    elif config.get_setting("updatemode") =="1": #Preguntar
      if platformtools.YesNoDialog("pelisalacarta","¡Hay "+str(len(CacheUpdate)) + " actualizaciones disponibles\nQuieres instalarlas ahora?"):
        download_all_updates()

    elif config.get_setting("updatemode") =="2": #Manual
      platformtools.AlertDialog("pelisalacarta","¡Hay "+str(len(CacheUpdate)) + " actualizaciones disponibles\nEntra en el muenu 'Actualizaciones' para elegir que hacer")



'''
Funciones para generar los indices de canales y servers:

Pendiente:  Pasar al channeltools o donde corresponda

Funcion:    Genera los indices para los canales y servers.
            Los indices contienen el nombre, el sha1 y el contenido del JSON del canal.
            Compara la fecha de creacion del indice con la fecha de la ultima modificacion de algun archivo de la carpeta para saber cuando hay que regenerarlos
            Estos indices sirven tanto para las actualizaciones como para el channelselector.
            
Uso:        ChannelList = get_channels_list()
            for Channel in ChannelList:
              ChannelList[Channel]["sha"]   <- Contiene el SHA1
              ChannelList[Channel]["json"]  <- Contiene el JSON del canal (demomento solo para canales, para server se podria implementar para llevar un control de versiones)
          
'''

def get_channels_list():
  logger.info("get_channels_list")
  ChannelsPath = os.path.join(config.get_runtime_path(),"channels")
  ChannelsIndex = os.path.join(config.get_data_path(),"channels.json")
  filedates = [os.path.getmtime(os.path.join(ChannelsPath,a)) for a in os.listdir(ChannelsPath) if a.endswith(".xml")]
  if os.path.exists(ChannelsIndex):
    try:
      JSONIndex = json.loads(open(ChannelsIndex,"r").read())      
      if JSONIndex["date"] == max(filedates):
        if JSONIndex["count"] == len([a for a in os.listdir(ChannelsPath) if a.endswith(".xml")]):
          logger.info("[get_channels_list] No es necesario regenerar el indice")
          return JSONIndex["list"]
    except:
      pass
  logger.info("[get_channels_list] Generando indice nuevo")
  import hashlib
  JSONIndex={"list":{}, "date":0}
  for File in os.listdir(ChannelsPath):
    File = os.path.join(ChannelsPath,File)
    if File.endswith(".xml"):
        XMLData = open(File, 'rb').read()
        JSONChannel = xml2json(XMLData)
        JSONChannel["sha"] = hashlib.sha1("blob " + str(len(XMLData)) + "\0" + XMLData).hexdigest()
        JSONIndex["list"][os.path.basename(File)[:-4]] = JSONChannel
  
  try:
    JSONIndex["date"] = max(filedates)
  except:
    JSONIndex["date"] = 0
  JSONIndex["count"] = len(filedates)
  open(ChannelsIndex,"w").write(json.dumps(JSONIndex, indent=4, sort_keys=True))
  return JSONIndex["list"]

def xml2json(data):
  JSONChannel = {}
  JSONChannel["id"]= re.compile('<id>(.*?)</id>',re.DOTALL).findall(data)[0].encode("utf8")
  JSONChannel["name"]= unicode(re.compile('<name>(.*?)</name>',re.DOTALL).findall(data)[0],"utf8", "ignore").encode("utf8")
  JSONChannel["version"]= re.compile('<version>(.*?)</version>',re.DOTALL).findall(data)[0].encode("utf8")
  JSONChannel["changes"]= unicode(re.compile('<changes>(.*?)</changes>',re.DOTALL).findall(data)[0],"utf8", "ignore").encode("utf8")
  JSONChannel["date"]= re.compile('<date>(.*?)</date>',re.DOTALL).findall(data)[0].encode("utf8")
  return JSONChannel
  
def get_servers_list():
  logger.info("get_servers_list")
  ServersPath = os.path.join(config.get_runtime_path(),"servers")
  ServersIndex = os.path.join(config.get_data_path(),"servers.json")
  filedates = [os.path.getmtime(os.path.join(ServersPath,a)) for a in os.listdir(ServersPath) if a.endswith(".py")]
  if os.path.exists(ServersIndex):
    try:
      JSONIndex = json.loads(open(ServersIndex,"r").read())
      if JSONIndex["date"] == max(filedates):
        if JSONIndex["count"] == len([a for a in os.listdir(ServersPath) if a.endswith(".py")]):
          logger.info("[get_servers_list] No es necesario regenerar el indice")
          return JSONIndex["list"]
    except:
      pass
  logger.info("[get_servers_list] Generando indice nuevo")
  import hashlib
  JSONIndex={"list":{}, "date":0}
  for File in os.listdir(ServersPath):
    File = os.path.join(ServersPath,File)
    if File.endswith(".py") and not File in ["__init__.py"]:
        FileData = open(File, 'rb').read()
        JSONFileData = {}
        #JSONFileData["json"] = json.loads(FileData)
        JSONFileData["sha"] = hashlib.sha1("blob " + str(len(FileData)) + "\0" + FileData).hexdigest()
        JSONIndex["list"][os.path.basename(File)[:-3]] = JSONFileData
  try:
    JSONIndex["date"] = max(filedates)
  except:
    JSONIndex["date"] = 0
  JSONIndex["count"] = len(filedates)
  open(ServersIndex,"w").write(json.dumps(JSONIndex, indent=4, sort_keys=True))
  return JSONIndex["list"]





'''
Funciones para actualizar el plugin por completo

Pendiente: Comprobar su correcto funcionamiento en las distintas platadormas / sistemas operativos
           funcion GetDownloadPath() para obtener la ruta del zip para la plataforma concreta y update() para instalar el zip: 
           ¿Mejor pasarlo al config? ya que cada plataforma tiene su config y seria mas sencillo que siempre obtenga la correcta y la instale correctamente
           
'''
  
def GetDownloadPath(version, platform=""):
  zipfile = config.PLUGIN_NAME + "-%s-%s.zip"
  if not platform:
    if config.PLATFORM_NAME=="kodi-isengard":
        platform = "kodi-isengard"
    elif config.PLATFORM_NAME=="kodi-helix":
        platform = "kodi-helix"
    elif config.PLATFORM_NAME=="xbmceden":
        platform = "xbmc-eden"
    elif config.PLATFORM_NAME=="xbmcfrodo":
        platform = "xbmc-frodo"
    elif config.PLATFORM_NAME=="xbmcgotham":
        platform = "xbmc-gotham"
    elif config.PLATFORM_NAME=="xbmc":
        platform = "xbmc-plugin"
    elif config.PLATFORM_NAME=="wiimc":
        platform = "wiimc"
    elif config.PLATFORM_NAME=="rss":
        platform = "rss"
    else:
        platform = config.PLATFORM_NAME
  return zipfile % (platform, version)
  
  

def update(version):
    logger.info("Actualizando plugin...")   
    
    LOCAL_FILE = os.path.join( config.get_data_path(),"pelisalacarta.zip" )
    
    REMOTE_FILE = DownloadUrl % (GetDownloadPath(version))
    REMOTE_FILE = "http://descargas.tvalacarta.info/" + GetDownloadPath(version)
    DESTINATION_FOLDER = os.path.join(config.get_runtime_path(),"..")

    logger.info("Archivo Remoto: " + REMOTE_FILE)
    logger.info("Archivo Local: " + LOCAL_FILE)
    
    from core import downloadtools
    if os.path.isfile(LOCAL_FILE):
      os.remove(LOCAL_FILE)
      
    ret = downloadtools.downloadfile(REMOTE_FILE, LOCAL_FILE)
    
    if ret is None:
      logger.info("Descomprimiendo fichero...")
      import ziptools
      unzipper = ziptools.ziptools()
      logger.info("Destino: " + DESTINATION_FOLDER)


      import shutil
      for file in os.listdir(os.path.join(config.get_runtime_path())):
        if not file in [".",".."]:
          if os.path.isdir(os.path.join(config.get_runtime_path(), file)):
            shutil.rmtree(os.path.join(config.get_runtime_path(), file))
          if os.path.isfile(os.path.join(config.get_runtime_path(), file)):
            os.remove(os.path.join(config.get_runtime_path(), file))
     
      unzipper.extract(LOCAL_FILE,DESTINATION_FOLDER)
      os.remove(LOCAL_FILE)
      platformtools.AlertDialog("Actualizacion", "Pelisalacarta se ha actualizado correctamente")
    elif ret == -1:
      platformtools.AlertDialog("Actualizacion", "Descarga Cancelada")
    else:
      platformtools.AlertDialog("Actualizacion", "Se ha producido un error al descargar el archivo")
