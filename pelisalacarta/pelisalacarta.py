#! /usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import sys

sys.dont_write_bytecode = True
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from platformcode.mediaserver.WebSocketServer import WebSocket, SimpleWebSocketServer
from SocketServer import ThreadingMixIn
import time
##################################################
#                     CLASS                      #
##################################################

#Handler HTTPServer sin imprimir errores en consola
class MyHTTPServer(HTTPServer):   
    def handle_error(self, request, client_address):
      import traceback
      if not "Errno 10054" in traceback.format_exc() and not "Errno 10053" in traceback.format_exc():
        logger.error(traceback.format_exc())
      else:
        logger.info( "Conexion Cerrada")
    
class ThreadedHTTPServer(ThreadingMixIn, MyHTTPServer):
    pass


#Handler para el serivodr WebSocket
class HandleWebSocket(WebSocket):
   def handleMessage(self):
      if self.data is None: self.data = ''
      
      if str(self.data).startswith("?"):
        sys.argv[str(self)]["Request"]=str(self.data).replace("?","")
        Thread(target=RunLauncher,args=[self]).start()  
                 
      elif str(self.data).startswith("!"):
        sys.argv[str(self)]["Data"]=str(self.data).replace("!","")
      

   def handleConnected(self):
      sys.argv[str(self)]={"Socket": self, "Request":"", "Data":"","Host":"http://" + myip + ":" + str(PORT)}
      MostrarInfo()

   def handleClose(self):
    if str(self) in sys.argv:
      del sys.argv[str(self)]
      MostrarInfo()
        
class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args): 
      #sys.stderr.write("%s - - [%s] %s\n" %(self.client_address[0], self.log_date_time_string(), format%args))
      pass

    def do_GET(self):     
        try:
            host = self.headers.get("Host")
        except:
            host = ""
        if ":" in host: host = host.split(":")[0]

        #Control de accesos
        Usuario = "user"
        Password = "password"
        ControlAcceso = False
        import base64
        #Comprueba la clave
        if ControlAcceso and self.headers.getheader('Authorization') <> "Basic " + base64.b64encode(Usuario + ":"+ Password):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"Introduce el nombre de usuario y clave para acceder a pelisalacarta\"')
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('¡Los datos introducidos no son correctos!')
            return
        
        
        if self.path =="/"+PLATFORM_NAME:
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , "page.html" ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            respuesta = f.read()
            respuesta = respuesta.replace("{$host}","ws://"+host + ":"+config.get_setting("websocket.port")+"/")
            self.wfile.write(respuesta)
            f.close()
      
        elif self.path.startswith("/image-"):
          import urllib2, urllib
          import base64
          url= self.path.replace("/image-","")
          url = base64.b64decode(urllib.unquote_plus(url)) 
          try:
            Headers = self.headers.dict
            if 'host' in Headers.keys(): del Headers["host"]
            if 'referer' in Headers.keys(): del Headers["referer"]
            
            req = urllib2.Request(url, headers=Headers)
            response = urllib2.urlopen(req)
            self.send_response(200)
            self.send_headers=response.info()
            self.end_headers()
            self.wfile.write(response.read())
            self.wfile.close()
            response.close() 
          except:
            self.send_response(400)
            self.wfile.close()
            
        elif self.path.startswith("/local-"):
          import base64
          import urllib
          Path= self.path.replace("/local-","").replace(".mp4","")  
          Path = base64.b64decode(urllib.unquote_plus(Path))
          Size = int(os.path.getsize(Path.decode("utf8") ))
          f=open(Path.decode("utf8") , "rb" )
          if not self.headers.get("range") ==None:
            if "=" in str(self.headers.get("range")) and "-" in str(self.headers.get("range")):
              Inicio= int(self.headers.get("range").split("=")[1].split("-")[0])
              if self.headers.get("range").split("=")[1].split("-")[1]<>"": 
                Fin= int(self.headers.get("range").split("=")[1].split("-")[1])
              else:
                Fin = Size-1
            
          else:
            Inicio=0
            Fin = Size-1
          
          if not Fin > Inicio: Fin = Size-1
            
          if self.headers.get("range") ==None:
            logger.info("-------------------------------------------------------")
            logger.info("Solicitando archivo local: "+ Path)
            logger.info("-------------------------------------------------------")
            
            self.send_response(200)
            self.send_header("Content-Disposition", "attachment; filename=video.mp4")  
            self.send_header('Accept-Ranges', 'bytes')   
            self.send_header('Content-Length', str(Size))   
            self.send_header("Connection", "close") 
            self.end_headers()
            while True:
              time.sleep(0.2)
              buffer =f.read(1024*250)
              if not buffer:
                break
              self.wfile.write(buffer)
            self.wfile.close()
            f.close()
          else:
            logger.info("-------------------------------------------------------")
            logger.info("Solicitando archivo local: "+ Path)
            logger.info("Rango: "+ str(Inicio) + "-" + str(Fin) + "/" + str(Size))
            logger.info("-------------------------------------------------------")
            f.seek(Inicio)
            
            self.send_response(206)
            self.send_header("Content-Disposition", "attachment; filename=video.mp4")  
            self.send_header('Accept-Ranges', 'bytes')   
            self.send_header('Content-Length', str(Fin-Inicio))   
            self.send_header('Content-Range', str(Inicio) + "-" + str(Fin) + "/" + str(Size))
            self.send_header("Connection", "close") 
            
            self.end_headers()
            while True:
              time.sleep(0.2)
              buffer =f.read(1024*250)
              if not buffer:
                break
              self.wfile.write(buffer)
            self.wfile.close()
            f.close()         
            
        elif self.path.startswith("/remote-"):
          import urllib2, urllib
          url= self.path.replace("/remote-","").replace(".mp4","")
          import base64
          url = base64.b64decode(urllib.unquote_plus(url))
          Headers = self.headers.dict
          h=urllib2.HTTPHandler(debuglevel=0)
          request = urllib2.Request(url)
          request.add_header("Accept-Encoding","")
          for header in Headers:
            if not header in ["host","referer","user-agent"]:
              request.add_header(header,Headers[header])
            
          opener = urllib2.build_opener(h)
          urllib2.install_opener(opener)  
          connexion = opener.open(request)
          self.send_response(connexion.getcode())
          ResponseHeaders = connexion.info()
          logger.info("------------------------------------")
          logger.info(url)
          logger.info(connexion.getcode())
          logger.info("Headers:")
          for header in ResponseHeaders:
            if header in ["content-disposition"]:
              logger.info("Eliminado Header ->" + header + "=" + ResponseHeaders[header])
            
            else:
              self.send_header(header, ResponseHeaders[header])
              logger.info("Reenviado Header ->" + header + "=" + ResponseHeaders[header])
          logger.info("Añadido Header   ->" + "content-disposition" + "=" + "attachment; filename=video.mp4")
          self.send_header("content-disposition", "attachment; filename=video.mp4")    
          self.end_headers()
          blocksize = 1024
          bloqueleido = connexion.read(blocksize)
          while len(bloqueleido)>0:
            self.wfile.write(bloqueleido)
            bloqueleido = connexion.read(blocksize)
          logger.info("Terminado")
          logger.info("------------------------------------")
          self.wfile.close()
          connexion.close()
             
        elif self.path.startswith("/netutv-"):
          import urllib2, urllib
          url= self.path.replace("/netutv-","").replace(".mp4","")
          import base64
          url = base64.b64decode(urllib.unquote_plus(url))
          Headers = self.headers.dict
          h=urllib2.HTTPHandler(debuglevel=0)
          request = urllib2.Request(url)
          request.add_header("Accept-Encoding","")
          for header in Headers:
            if not header in ["host","user-agent"]:
              request.add_header(header,Headers[header])
            
          opener = urllib2.build_opener(h)
          urllib2.install_opener(opener)  
          connexion = opener.open(request)
          self.send_response(connexion.getcode())
          ResponseHeaders = connexion.info()
          logger.info("------------------------------------")
          logger.info(url)
          logger.info(connexion.getcode())
          logger.info("Headers:")
          for header in ResponseHeaders:
              self.send_header(header, ResponseHeaders[header])
              logger.info("Reenviado Header ->" + header + "=" + ResponseHeaders[header])

          self.end_headers()

          if url.endswith(".m3u8"):
            m3u8 = connexion.read()
            base = url.replace(url.split("/")[len(url.split("/"))-1],"")
            file = url.replace(base,"").replace(".m3u8","")
            import re
            patron="("+file+"[^\.]+\.ts)"
            matches = re.compile(patron,re.DOTALL).findall(m3u8)
            for video in matches:
              m3u8 = m3u8.replace(video,"netutv-"+urllib.quote_plus(base64.b64encode(base+video))+".mp4")
            self.wfile.write(m3u8)
            self.wfile.close()
            connexion.close()
            logger.info("Terminado")
            logger.info("------------------------------------")
          
          else:
            blocksize = 1024
            bloqueleido = connexion.read(blocksize)
            while len(bloqueleido)>0:
              self.wfile.write(bloqueleido)
              bloqueleido = connexion.read(blocksize)
            logger.info("Terminado")
            logger.info("------------------------------------")
            self.wfile.close()
            connexion.close()
             
        elif self.path.endswith(".jpg"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.endswith(".png"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            
        elif self.path.endswith(".gif"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'image/gif')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            
        elif self.path.endswith(".css"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.endswith(".js"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'text/js')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.endswith(".html"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        else:
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        return
    
    def address_string(self):
        # Disable reverse name lookups
        return self.client_address[:2][0] 
        
        
##################################################
#                 FUNCIONES                      #
##################################################

def LibraryService():
  import library_service

def MostrarInfo():

    os.system('cls' if os.name == 'nt' else 'clear')
    print ("--------------------------------------------------------------------")
    print ("Pelisalacarta Iniciado")
    print ("La URL para " + PLATFORM_NAME + " es http://" + myip + ":" + str(PORT) + "/" + PLATFORM_NAME)
    print ("WebSocket Server iniciado en ws://"+ myip + ":" + config.get_setting("websocket.port")+"/")
    print ("--------------------------------------------------------------------")
    print ("Runtime Path      : " + config.get_runtime_path())
    print ("Data Path         : " + config.get_data_path())
    print ("Download Path     : " + config.get_setting("downloadpath") )
    print ("DownloadList Path : " + config.get_setting("downloadlistpath"))
    print ("Bookmark Path     : " + config.get_setting("bookmarkpath"))  
    print ("Library Path      : " + config.get_setting("library_path"))  
    print ("Cache Path        : " + config.get_setting("cache.dir"))  
    print ("Cookies Path      : " + config.get_setting("cookies.dir"))  
    print ("--------------------------------------------------------------------")
    conexiones = []
    Threads = []
    for a in sys.argv:
      if "WebSocket" in a:
        try:
          conexiones.append(str(sys.argv[a]["Socket"].client.getpeername()).split("'")[1])
        except:
          del sys.argv[a]
      if "Thread" in a:
        Threads.append(a)
    if len(conexiones) >0:
      print ("Clientes conectados:")
      for conexion in conexiones:
        print (conexion)
    else:
      print ("No hay conexiones")
      
    if len(Threads) >0:
      print ("")
      print ("Hilos Trabajando:")
      for Thr in Threads:
        print (Thr)
    else:
      print ("")
      print ("No hay Hilos")

def RunLauncher(Socket):

  sys.argv[threading.current_thread().name]={"Socket":str(Socket), "Thread": threading.current_thread()}
  MostrarInfo()
  #Para desarrollo, recarga los modulos en cada peticion, para no tener que reiniciar si modificamos un modulo.
  #Reduce el rendiemiento cuando esta activo.
  #Por defecto desactivado, para activar poner 1.
  if 1:
    import inspect
    #Recorre los modulos cargados en memoria
    for module in sys.modules.keys():
      if inspect.ismodule(sys.modules[module]):
        #Recarga todos los modulos excepto los loggers.
        if config.get_runtime_path() in str(sys.modules[module]) and not "__main__" in str(sys.modules[module]) and not "logger" in str(sys.modules[module]) and not "library_service" in str(sys.modules[module]):
          reload(sys.modules[module])
          
  try:
    launcher.run()
    del sys.argv[threading.current_thread().name]
    MostrarInfo()
  except Exception as e:
    import traceback
    from platformcode.mediaserver import cliente
    logger.error(traceback.format_exc())
    from core import scrapertools
    patron = 'File "'+os.path.join(config.get_runtime_path(),"pelisalacarta","channels","").replace("\\","\\\\")+'([^.]+)\.py"'
    canal = scrapertools.find_single_match(traceback.format_exc(),patron)
    if canal:
      cliente.Dialogo().MostrarOK(
        "Se ha producido un error en el canal " + canal,
        "Esto puede ser devido a varias razones: \n - El servidor no está disponible, o no esta respondiendo.\n - Cambios en el diseño de la web.\n - Etc...\nComprueba el log para ver mas detalles del error.")
    else:
      cliente.Dialogo().MostrarOK(
        "Se ha producido un error en pelisalacarta",
        "Comprueba el log para ver mas detalles del error." )
    del sys.argv[threading.current_thread().name]
    MostrarInfo()
       
##################################################
#                   CODIGO                       #
##################################################        
        
import os
from core import platform_name
from core import logger
logger.info("pelisalacarta server init...")
from core import config
config.verify_directories_created()
from threading import Thread
import threading
from platformcode import launcher
PLATFORM_NAME = platform_name.PLATFORM_NAME
sys.argv ={}
librerias = os.path.join( config.get_runtime_path(), 'lib' ) 
sys.path.append (librerias)
# IP
try:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.mimediacenter.info', 80))
    myip = s.getsockname()[0]
except:
    myip = "0.0.0.0"

try:
    PORT=int(config.get_setting("server.port"))
    WebsocketPort=int(config.get_setting("websocket.port"))
    server = ThreadedHTTPServer(('', PORT), Handler)
    
    WebSocketServer = SimpleWebSocketServer("",WebsocketPort,HandleWebSocket)
    Thread(target=WebSocketServer.serveforever).start()
    
    # Da por levantado el servicio
    logger.info("--------------------------------------------------------------------")
    logger.info("Pelisalacarta Iniciado")
    logger.info("La URL para " + PLATFORM_NAME + " es http://" + myip + ":" + str(PORT) + "/" + PLATFORM_NAME)
    logger.info("WebSocket Server iniciado en ws://"+ myip + ":" + str(WebsocketPort))
    logger.info("--------------------------------------------------------------------")
    logger.info("Runtime Path      = " + config.get_runtime_path())
    logger.info("Data Path         = " + config.get_data_path())
    logger.info("Download Path     = " + config.get_setting("downloadpath") )
    logger.info("DownloadList Path = " + config.get_setting("downloadlistpath"))
    logger.info("Bookmark Path     = " + config.get_setting("bookmarkpath"))
    logger.info("Library Path      = " + config.get_setting("library_path"))
    logger.info("Cache Path        : " + config.get_setting("cache.dir"))  
    logger.info("Cookies Path      : " + config.get_setting("cookies.dir"))  
    logger.info("--------------------------------------------------------------------")
    MostrarInfo()
    
    #Thread(target=LibraryService).start()
    server.serve_forever()



except KeyboardInterrupt:
    print 'Deteniendo el servidor'
    server.socket.close()
    server.shutdown()
    WebSocketServer.close()

 

    