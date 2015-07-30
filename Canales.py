import os
import re
import hashlib
import sys
import urlparse

branch = "trunk"
urlbase="https://raw.githubusercontent.com/divadres/pelisalacarta/" + branch

def Canal(channel):
  JSONData={}
  JSONData["name"] = os.path.basename(channel)
  JSONData["size"] = os.path.getsize(channel)
  JSONData["path"] = "/".join(channel.replace(os.path.dirname(__file__) + os.sep,"").split(os.sep))
  JSONData["url"] = "https://api.github.com/repos/divadres/pelisalacarta/contents/" +JSONData["path"] +"?ref=" + branch
  JSONData["type"] = "file"
  with open(channel, 'rb') as f: JSONData["sha"] =  hashlib.sha1("blob " + str(JSONData["size"]) + "\0" + f.read()).hexdigest()
  JSONData["download_url"] = "https://raw.githubusercontent.com/divadres/pelisalacarta/"+ branch + "/" + JSONData["path"] 
  JSONData["git_url"] = "https://api.github.com/repos/divadres/pelisalacarta/git/blobs/" + JSONData["sha"]
  JSONData["html_url"] = "https://github.com/divadres/pelisalacarta/blob/"+ branch + "/"+ JSONData["path"]
  JSONData["_links"]={}
  JSONData["_links"]["git"] = JSONData["git_url"]
  JSONData["_links"]["html"] = JSONData["html_url"]
  JSONData["_links"]["self"] = JSONData["url"] 
  return JSONData



JSONData=[]
for channel in os.listdir(os.path.join(os.path.dirname(__file__),"pelisalacarta","pelisalacarta","channels","")):
  if channel.endswith(".py"):
    JSONData.append( Canal(os.path.join(os.path.dirname(__file__),"pelisalacarta","pelisalacarta","channels",channel)))

JSONData.sort(key=lambda item: item["name"])
    
import json
f = open("C:\json.txt","w")
f.write(json.dumps(JSONData, indent=4, sort_keys=True))
f.close()    
 