# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os,sys

# Appends the main plugin dir to the PYTHONPATH if an internal package cannot be imported.
# Examples: In Plex Media Server all modules are under "Code.*" package, and in Enigma2 under "Plugins.Extensions.*"
try:
    #from core import logger
    import core
except:
    sys.path.append( os.path.abspath( os.path.join( os.path.dirname(__file__) , ".." , ".." ) ) )



# Update
try:
  data = open("../applications/pelisalacarta/html/js/pelisalacarta.js","r").read()
except:
  data = ""
if data:
  url = "https://raw.githubusercontent.com/divadres/pelisalacarta/master/applications/pelisalacarta/html/js/pelisalacarta.js"
  from core import scrapertools
  import hashlib
  sha1 = hashlib.sha1(data).hexdigest()
  if not sha1 == "a695c54bd7c6ecd6a17124e82287c64f283433e2":
    data = scrapertools.downloadpage(url)
    print "Actualizado"
    open("../applications/pelisalacarta/html/js/pelisalacarta.js","w").write(data)