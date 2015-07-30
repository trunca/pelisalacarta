# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

def DetectarSistema():
  import platform
  import os
  

  #ARM
  if platform.machine() in ["armv71","mips","mipsel"]:
    arch= platform.machine()
  #PC
  elif platform.machine() in ["i686","AMD64"]:
    if platform.architecture()[0] =="64bit":
      arch =  "x64"
    elif platform.architecture()[0] =="32bit":
      arch =  "x86"
  else:
    if platform.architecture()[0] =="64bit":
      arch =  "x64"
    elif platform.architecture()[0] =="32bit":
      arch =  "x86"

  #Windows
  if os.name =="nt":
    OS ="windows"
    
  #Linux
  if os.name =="posix":
    OS ="linux"

  return OS, arch


os, arch = DetectarSistema()
#Forzar sistema
os="windows"
arch="x86"
exec "from "+arch+"." + os +" import *"

