# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Zip Tools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import base64, re, urllib, string, sys, zipfile, os, os.path
import config
import logger

class ziptools:

    def extract(self, file, dir, progress =False):
        import guitools
        logger.info("file=%s" % file)
        logger.info("dir=%s" % dir)
        
        if not dir.endswith(':') and not os.path.exists(dir):
            os.mkdir(dir)

        zf = zipfile.ZipFile(file)
        self._createstructure(file, dir)
        num_files = len(zf.namelist())
        dprogress = guitools.Dialog_Progress("Extrayendo Archivos...","Iniciando")
        for x, name in enumerate(zf.namelist()):
            logger.info("name=%s" % name)
            dprogress.Actualizar(x*100 / len(zf.namelist()),"Extrayendo archivo " + str(x) + " de " + str(len(zf.namelist())) + "\n" + name)
            if not name.endswith('/'):
                logger.info("no es un directorio")
                try:
                    (path,filename) = os.path.split(os.path.join(dir, name))
                    logger.info("path=%s" % path)
                    logger.info("name=%s" % name)
                    os.makedirs( path )
                except:
                    pass
                outfilename = os.path.join(dir, name)
                logger.info("outfilename=%s" % outfilename)
                try:
                    outfile = open(outfilename, 'wb')
                    outfile.write(zf.read(name))
                except:
                    logger.info("Error en fichero "+name)
        dprogress.Cerrar()

    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)

    def create_necessary_paths(filename):
        try:
            (path,name) = os.path.split(filename)
            os.makedirs( path)
        except:
            pass

    def _makedirs(self, directories, basedir):
        for dir in directories:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)

    def _listdirs(self, file):
        zf = zipfile.ZipFile(file)
        dirs = []
        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)

        dirs.sort()
        return dirs
        
    def _listdirsandfiles(self, file):
        zf = zipfile.ZipFile(file)
        dirs = []
        files = []
        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)
            else:
                files.append(name)

        dirs.sort(key=lambda item: len(item.split("/")))
        files.sort(key=lambda item: len(item.split("/")))
        
        return dirs, files