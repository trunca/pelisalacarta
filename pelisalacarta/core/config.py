# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración multiplataforma
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
PLATFORM_NAME = platform_name.PLATFORM_NAME
exec "from platformcode."+PLATFORM_NAME+" import logger"
exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"

def force_platform(platform_name):
    global PLATFORM_NAM
    PLATFORM_NAME = platform_name
    exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"

def get_platform():
    return PLATFORM_NAME

def get_library_support():
    return (PLATFORM_NAME=="xbmc" or PLATFORM_NAME=="xbmcdharma" or PLATFORM_NAME=="xbmceden" or PLATFORM_NAME=="boxee")

def get_system_platform():
    exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"
    return platformconfig.get_system_platform()

def open_settings():
    exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"
    return platformconfig.open_settings()

def get_setting(name,channel=""):
    if channel =="":   
      exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"  
      dev=platformconfig.get_setting(name)
    if channel !="":          
      from xml.dom import minidom
      rutacanal = os.path.join(get_data_path(), channel+".xml")
      settings=""
      encontrado = False
      #Lee el archivo XML (si existe)
      if os.path.exists(rutacanal):
        while len(settings)<> os.path.getsize(rutacanal) or len(settings)==0:
          settings = open(rutacanal, 'rb').read()
        xmldoc= minidom.parseString(settings)
        dev=""
        #Busca el elemento y dvuelve el valor
        for setting in xmldoc.getElementsByTagName("setting"):
          if setting.getAttribute("id") == name:
            dev = setting.getAttribute("value").encode("utf8")
            encontrado = True
    
      if encontrado == False:
        dev=""
        logger.error("clave: "+ name  + " no encontrada en canal: " + channel)
    
    return dev

def set_setting(name,value, channel=""):

    if channel!="":
      from xml.dom import minidom
      rutacanal = os.path.join(get_data_path(), channel+".xml")
      settings=""
      guardado = False
      #Crea un Nuevo XML vacio
      new_settings = minidom.getDOMImplementation().createDocument(None, "settings", None)
      new_settings_root = new_settings.documentElement
      #Lee el XML antiguo (Si Existe)
      if os.path.exists(rutacanal):
        while len(settings)<> os.path.getsize(rutacanal) or len(settings)==0:
          settings = open(rutacanal, 'rb').read()
          xmldoc= minidom.parseString(settings)
      
        #Pasa todos los elementos al XML Nuevo (Modificando el valor del elemento que se quiere cambiar)
        for setting in xmldoc.getElementsByTagName("setting"):
          nodo = new_settings.createElement("setting")
          if setting.getAttribute("id") == name:
            nodo.setAttribute("value",value)
            guardado = True
          else:
            nodo.setAttribute("value",setting.getAttribute("value"))
          nodo.setAttribute("id",setting.getAttribute("id"))    
          new_settings_root.appendChild(nodo)
        
      #Si el elemento no estaba en el XML antiguo crea uno nuevo con el valor pasado
      if guardado ==False:
        nodo = new_settings.createElement("setting")
        nodo.setAttribute("value",value)
        nodo.setAttribute("id",name)    
        new_settings_root.appendChild(nodo)
      #Guarda los datos
      fichero = open(os.path.join( get_data_path() , channel+".xml" ), "w")
      fichero.write(new_settings.toprettyxml(encoding='utf-8'))
      fichero.close()
    
    else:
      exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"
      platformconfig.set_setting(name,value)

def save_settings():
    exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"
    platformconfig.save_settings()

def get_localized_string(code):
    exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"
    return platformconfig.get_localized_string(code)

def get_library_path():
    exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"
    return platformconfig.get_library_path()

def get_temp_file(filename):
    exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"
    return platformconfig.get_temp_file(filename)

def get_runtime_path():
    exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"
    return platformconfig.get_runtime_path()

def get_data_path():
    exec "import platformcode."+PLATFORM_NAME+".config as platformconfig"
    return platformconfig.get_data_path()

def get_thumbnail_path():
    WEB_PATH = ""
    thumbnail_type = get_setting("thumbnail_type")
    if thumbnail_type=="":
        thumbnail_type="2"
    if thumbnail_type=="0":
        WEB_PATH = "http://pelisalacarta.mimediacenter.info/posters/"
    elif thumbnail_type=="1":
        WEB_PATH = "http://pelisalacarta.mimediacenter.info/banners/"
    elif thumbnail_type=="2":
        WEB_PATH = "http://pelisalacarta.mimediacenter.info/squares/"
    return WEB_PATH
    
    
# Test if all the required directories are created
def verify_directories_created():
    logger.info("Comprobando directorios")
    # Create data_path if not exists
    if not os.path.exists(get_data_path()):
        logger.debug("Creating data_path: "+get_data_path())
        try:
            os.mkdir(get_data_path())
        except:
            pass
    
    config_paths = [["library_path",     "Biblioteca"],
                    ["downloadpath",     "Descargas"],
                    ["downloadlistpath", os.path.join("Descargas","Lista")],
                    ["bookmarkpath",     "Favoritos"],
                    ["cache.dir",        "Cache"],
                    ["cookies.dir",      "Cookies"]]
                             
    for setting, default in config_paths:
      path = get_setting(setting)
      if path=="":
          path = os.path.join( get_data_path() , default)
          set_setting(setting , path)
          
      if not get_setting(setting).lower().startswith("smb") and not os.path.exists(get_setting(setting)):
        logger.debug("Creating " + setting +": " +get_setting(setting))
        try:
            os.mkdir(get_setting(setting))
        except:
            pass


          





