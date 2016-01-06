# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración - xbmc
#------------------------------------------------------------
# tvalacarta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import sys
import os

import xbmcplugin
import xbmc

PLATFORM_NAME = "xbmc-plugin"

PLUGIN_NAME = "pelisalacarta"



def get_platform():
    return PLATFORM_NAME

def is_xbmc():
    return True

def get_library_support():
    return True

def get_system_platform():
    """ fonction: pour recuperer la platform que xbmc tourne """
    import xbmc
    platform = "unknown"
    if xbmc.getCondVisibility( "system.platform.linux" ):
        platform = "linux"
    elif xbmc.getCondVisibility( "system.platform.xbox" ):
        platform = "xbox"
    elif xbmc.getCondVisibility( "system.platform.windows" ):
        platform = "windows"
    elif xbmc.getCondVisibility( "system.platform.osx" ):
        platform = "osx"
    return platform
    
def open_settings():
    xbmcplugin.openSettings( sys.argv[ 0 ] )

def get_setting(name):
    return xbmcplugin.getSetting(name)

def set_setting(name,value):
    try:
        xbmcplugin.setSetting(name,value)
    except:
        pass

def get_localized_string(code):
    dev = xbmc.getLocalizedString( code )

    try:
        dev = dev.encode ("utf-8") #This only aplies to unicode strings. The rest stay as they are.
    except:
        pass
    
    return dev
    
def get_library_path():
    #return os.path.join( get_data_path(), 'library' )
    default = os.path.join( get_data_path(), 'library' )

    value = get_setting("librarypath")
    if value=="":
        value=default
    return value

def get_temp_file(filename):
    return xbmc.translatePath( os.path.join( "special://temp/", filename ))

def get_runtime_path():
    return os.getcwd()

def get_data_path():
    devuelve = xbmc.translatePath( os.path.join("special://home/","userdata","plugin_data","video",PLUGIN_NAME) )
    
    # XBMC en modo portable
    if devuelve.startswith("special:"):
        devuelve = xbmc.translatePath( os.path.join("special://xbmc/","userdata","plugin_data","video",PLUGIN_NAME) )

    # Plex 8
    if devuelve.startswith("special:"):
        devuelve = os.getcwd()

    return devuelve

def get_cookie_data():
    import os
    ficherocookies = os.path.join( get_data_path(), 'cookies.dat' )

    cookiedatafile = open(ficherocookies,'r')
    cookiedata = cookiedatafile.read()
    cookiedatafile.close();

    return cookiedata

# Test if all the required directories are created
def verify_directories_created():
    import logger
    import os
    logger.info("pelisalacarta.core.config.verify_directories_created")

    # Force download path if empty
    download_path = get_setting("downloadpath")
    if download_path=="":
        download_path = os.path.join( get_data_path() , "downloads")
        set_setting("downloadpath" , download_path)

    # Force download list path if empty
    download_list_path = get_setting("downloadlistpath")
    if download_list_path=="":
        download_list_path = os.path.join( get_data_path() , "downloads" , "list")
        set_setting("downloadlistpath" , download_list_path)

    # Force bookmark path if empty
    bookmark_path = get_setting("bookmarkpath")
    if bookmark_path=="":
        bookmark_path = os.path.join( get_data_path() , "bookmarks")
        set_setting("bookmarkpath" , bookmark_path)

    # Create data_path if not exists
    if not os.path.exists(get_data_path()):
        logger.debug("Creating data_path "+get_data_path())
        try:
            os.mkdir(get_data_path())
        except:
            pass

    # Create download_path if not exists
    if not download_path.lower().startswith("smb") and not os.path.exists(download_path):
        logger.debug("Creating download_path "+download_path)
        try:
            os.mkdir(download_path)
        except:
            pass

    # Create download_list_path if not exists
    if not download_list_path.lower().startswith("smb") and not os.path.exists(download_list_path):
        logger.debug("Creating download_list_path "+download_list_path)
        try:
            os.mkdir(download_list_path)
        except:
            pass

    # Create bookmark_path if not exists
    if not bookmark_path.lower().startswith("smb") and not os.path.exists(bookmark_path):
        logger.debug("Creating bookmark_path "+bookmark_path)
        try:
            os.mkdir(bookmark_path)
        except:
            pass

    # Create library_path if not exists
    if not get_library_path().lower().startswith("smb") and not os.path.exists(get_library_path()):
        logger.debug("Creating library_path "+get_library_path())
        try:
            os.mkdir(get_library_path())
        except:
            pass

    # Checks that a directory "xbmc" is not present on platformcode
    old_xbmc_directory = os.path.join( get_runtime_path() , "platformcode" , "xbmc" )
    if os.path.exists( old_xbmc_directory ):
        logger.debug("Removing old platformcode.xbmc directory")
        try:
            import shutil
            shutil.rmtree(old_xbmc_directory)
        except:
            pass
