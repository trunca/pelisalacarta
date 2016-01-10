function GetResponses(data) {
    response = JSON.parse(data)
    data = response["data"];
    switch (response["action"]) {
        case "connect":
            document.getElementById("Version").innerHTML = data["version"]
            document.getElementById("Date").innerHTML = data["date"]
            ID = response["id"]
            break;
        case "EndItems":
            for (h = 0; h < data["itemlist"].length; h++) {
              JsonItem = data["itemlist"][h]
              //[COLOR xxx][/COLOR]
              var re = /(\[COLOR ([^\]]+)\])(?:.*?)(\[\/COLOR\])/g; 
              var str = JsonItem["title"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["title"] = JsonItem["title"].replace(resultado[1],"<span style='color:"+resultado[2]+"'>")
                  JsonItem["title"] = JsonItem["title"].replace(resultado[3],"</span>")
              }
              
              //[B][/B]
              var re = /(\[B\])(?:.*?)(\[\/B\])/g; 
              var str = JsonItem["title"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["title"] = JsonItem["title"].replace(resultado[1],"<b>")
                  JsonItem["title"] = JsonItem["title"].replace(resultado[2],"</b>")
              }
              
              //[i][/i]
              var re = /(\[I\])(?:.*?)(\[\/I\])/g; 
              var str = JsonItem["title"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["title"] = JsonItem["title"].replace(resultado[1],"<i>")
                  JsonItem["title"] = JsonItem["title"].replace(resultado[2],"</i>")
              }
              //[COLOR xxx][/COLOR]
              var re = /(\[COLOR ([^\]]+)\])(?:.*?)(\[\/COLOR\])/g; 
              var str = JsonItem["plot"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[1],"<span style='color:"+resultado[2]+"'>")
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[3],"</span>")
              }
              
              //[B][/B]
              var re = /(\[B\])(?:.*?)(\[\/B\])/g; 
              var str = JsonItem["plot"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[1],"<b>")
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[2],"</b>")
              }
              
              //[i][/i]
              var re = /(\[I\])(?:.*?)(\[\/I\])/g; 
              var str = JsonItem["plot"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[1],"<i>")
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[2],"</i>")
              }
              
              if (JsonItem["action"]=="go_back"){
                Action = 'Back()'
              }else{
                Action = 'DescargarContenido(\''+ JsonItem["url"] +'\')'
              }
              if (JsonItem["thumbnail"].indexOf("http") != 0){JsonItem["thumbnail"] = data["host"] +"/local-"+encodeURIComponent(btoa(JsonItem["thumbnail"]))}
              if (data["mode"]==0){
                HtmlItem ='<li class="ListItemBanner"><a onblur="" onfocus="ItemFocus=this" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+data["host"]+'" src="'+JsonItem["thumbnail"]+'"></div><h3 class="ListItem">' + JsonItem["title"] + '</h3><p class="ListItem"></p></a>{$BotonMenu}</li>'
              }else if (data["mode"]==1){
                HtmlItem ='<li class="ListItemChannels"><a onblur="DesCargarInfo(this)" onfocus="ItemFocus=this" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><h3 class="ListItem">' + JsonItem["title"] + '</h3><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+data["host"]+'" src="'+JsonItem["thumbnail"]+'"></div></a>{$BotonMenu}</li>'
             
              }else if (data["mode"]==2){
                if (JsonItem["action"]=="go_back" || JsonItem["action"]=="search" || JsonItem["thumbnail"].indexOf("thumb_folder") != -1 || JsonItem["thumbnail"].indexOf("thumb_nofolder") != -1 || JsonItem["thumbnail"].indexOf("thumb_error") != -1){
                  HtmlItem ='<li class="ListItem"><a onfocus="DesCargarInfo(this);ItemFocus=this" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+data["host"]+'" src="'+JsonItem["thumbnail"]+'"><img class="Default" src="http://pelisalacarta.mimediacenter.info/squares/folder.png"></div><h3 class="ListItem">' + JsonItem["title"] + '</h3><p class="ListItem">' + JsonItem["plot"] + '</p></a>{$BotonMenu}</li>'
                }else{
                  HtmlItem ='<li class="ListItem"><a onblur="DesCargarInfo(this)" onfocus="CargarInfo(this);ItemFocus=this" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+data["host"]+'" src="'+JsonItem["thumbnail"]+'"><img class="Default" src="http://pelisalacarta.mimediacenter.info/squares/folder.png"></div><h3 class="ListItem">' + JsonItem["title"] + '</h3><p class="ListItem">' + JsonItem["plot"] + '</p></a>{$BotonMenu}</li>'
                }
              }
              Lista = "";
              for (x = 0; x < JsonItem["context"].length; x++) {
                Lista +=
                '<li class="Lista"><a href="javascript:void(0)" onclick="CerrarDialogos();DescargarContenido(\'' + JsonItem["context"][x]["url"] +
                '\')" class="Lista"><h3>' + JsonItem["context"][x]["title"] + '</h3></a></li>';
              }
              BotonMenu = '<a class="ListItemButton" href="javascript:void(0)" onclick=\'ItemFocus=this;AbrirMenu("Menu","'+btoa(Lista)+'")\'></a>';
              ClassMenu = "ListItemMenu"
              if (JsonItem["context"].length === 0) {
                  BotonMenu = "";
                  ClassMenu = "";
              }
              HtmlItem = HtmlItem.replace("{$BotonMenu}", BotonMenu);
              HtmlItem = HtmlItem.replace("{$ClassMenu}", ClassMenu);
              ItemList += HtmlItem;

            }

            if (Navegacion.length > 0) {
                if (Navegacion[Navegacion.length - 1].Url == UltimoRequest) {
                    Navegacion[Navegacion.length - 1].Time          = new Date().getTime() - UltimoRequestTime;
                    document.getElementById("Contenedor").innerHTML = '<ul class="ListItem" id="itemlist">' + ItemList + '</ul>';
                    if (Navegacion[Navegacion.length - 1].Time > TiempoCache){
                      Navegacion[Navegacion.length - 1].Data            = document.getElementById("Contenedor").innerHTML;
                    }
                    if (document.getElementById("Contenedor").children[0].children.length > Navegacion[Navegacion.length - 1].Focus){
                      document.getElementById("Contenedor").children[0].children[Navegacion[Navegacion.length - 1].Focus].children[0].focus();
                    }else{
                      document.getElementById("Contenedor").children[0].children[document.getElementById("Contenedor").children[0].children.length -1].children[0].focus();
                    }
                    document.getElementById("Contenedor").scrollTop = Navegacion[Navegacion.length - 1].Scroll;
                    
                } else {
                    Navegacion[Navegacion.length - 1].Scroll        = document.getElementById("Contenedor").scrollTop;
                    Navegacion[Navegacion.length - 1].Focus         = Array.prototype.indexOf.call(document.getElementById("itemlist").children, ItemFocus.parentNode);
                    Navegacion.push({});
                    Navegacion[Navegacion.length - 1].Titulo        = ItemFocus.children[1].textContent;
                    Navegacion[Navegacion.length - 1].Url           = UltimoRequest;
                    Navegacion[Navegacion.length - 1].Time          = new Date().getTime() - UltimoRequestTime;
                    document.getElementById("Contenedor").innerHTML = '<ul class="ListItem" id="itemlist">' + ItemList + '</ul>';
                    if (Navegacion[Navegacion.length - 1].Time > TiempoCache){
                      Navegacion[Navegacion.length - 1].Data            = document.getElementById("Contenedor").innerHTML;
                    }
                    document.getElementById("Contenedor").children[0].children[0].children[0].focus();
                    document.getElementById("Contenedor").scrollTop = 0;
                }
            } else {
                Navegacion.push({});
                Navegacion[Navegacion.length - 1].Titulo          = "Inicio";
                Navegacion[Navegacion.length - 1].Url             = UltimoRequest;
                Navegacion[Navegacion.length - 1].Time            = new Date().getTime() - UltimoRequestTime;
                Navegacion[Navegacion.length - 1].Scroll          = "";
                Navegacion[Navegacion.length - 1].Focus           = "";
                document.getElementById("Contenedor").innerHTML   = '<ul class="ListItem" id="itemlist">' + ItemList + '</ul>'
                if (Navegacion[Navegacion.length - 1].Time > TiempoCache){
                  Navegacion[Navegacion.length - 1].Data            = document.getElementById("Contenedor").innerHTML;
                }
                document.getElementById("Contenedor").children[0].children[0].children[0].focus();

            }
            
            
            ActualizarNavegacion()           
            EnviarDatos({"id":response["id"], "result":true });
            CerrarLoading()
            break;
        case "Refresh":
            Consulta = Navegacion[Navegacion.length - 1].Url;
            Navegacion[Navegacion.length - 1].Scroll = document.getElementById("Contenedor").scrollTop;
            Navegacion[Navegacion.length - 1].Focus  = Array.prototype.indexOf.call(document.getElementById("itemlist").children, ItemFocus.parentNode);
            DescargarContenido(Consulta);
            EnviarDatos({"id":response["id"], "result":true });
            break;
        case "Alert":
            CerrarLoading()
            AbrirAlert(response["id"],data)
            break;
        case "AlertYesNo":
            CerrarLoading()
            AbrirAlertYesNo(response["id"],data)
            break;
        case "ProgressBG":
            AbrirProgressBG(response["id"],data)
            EnviarDatos({"id":response["id"], "result":true });
            break;
        case "ProgressBGUpdate":
            UpdateProgressBG(response["id"],data)
            break;
        case "ProgressBGClose":
            CerrarProgressBG();
            EnviarDatos({"id":response["id"], "result":true });
            break;
        case "Progress":
            CerrarLoading()
            AbrirProgress(response["id"],data)
            EnviarDatos({"id":response["id"], "result":true });
            break;
        case "ProgressUpdate":
            UpdateProgress(response["id"],data)
            break;
        case "ProgressClose":
            CerrarProgress();
            EnviarDatos({"id":response["id"], "result":true });
            CerrarLoading()
            break;
        case "ProgressIsCanceled":
            EnviarDatos({"id":response["id"], "result":document.getElementById("ProgressBar-Cancelled").checked !="" });
            break;
        case "isPlaying":
            EnviarDatos({"id":response["id"], "result": HED.avmedia.isActive()});
            break;
        case "Keyboard":
            CerrarLoading()
            AbrirKeyboard(response["id"],data);
            break;
        case "List":
            CerrarLoading()
            Lista = "";
            for (x = 0; x < data["list"].length; x++) {
                Lista +=
                    '<li class="Lista"><a href="javascript:void(0)" onclick="CerrarDialogos();EnviarDatos({\'id\':\''+response["id"]+'\', \'result\':'+x+' })" class="Lista"><h3>' + data["list"][x] + '</h3></a></li>';
            }
            AbrirLista(response["id"],data,Lista)
            break;
        case "Play":
            EnviarDatos({"id":response["id"], "result":true });
            CerrarLoading()
             Load = false;
             buffer = true;
             data["video_url"] = data["video_url"].replace(/&amp;/g, '&');
             //data["Url"] = data["video_url"].split("?")[0]
             
             //archivos locales
             if(!new RegExp("^(.+://)").test(data["video_url"])){
              buffer = false;
              if (PythonPath !="" && data["video_url"].indexOf(".mkv")==-1){
                data["video_url"] =  PythonPath + data["video_url"]
              }else{
                data["video_url"] =  PythonPath + data["video_url"]
                //data["video_url"] = JsonResponse["Host"]+"/local-"+encodeURIComponent(btoa(Utf8.encode(data["video_url"])))+".mp4"
              }
             }
             /*
             if (data["url"].indexOf("mega.co.nz") != -1) {
              data["video_url"] = data["url"]
              Load = true;
             }
             */
             /*
             var oOptions = {
              x: 1280/2, y: 720/2, width: 0, height: 0, 
              type: 'browser',
              windowOptions: [
                'destroyOnMenuKey', // Important!
                'noTabs',
                'noTabBar',
                'noToolBar',
                'noBookmarksMenu',
                'noSettingsMenu',
                'readonlyUrl',
                'noExitConfirm',
              ],
              downloadOptions: ['downloadAndPlay'],
              userAgent: "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
              url: data["video_url"],
              fCallbacks: {
                fOnPlay: function(internalId, sUrl) {
                  var browser = HED.window.getByInternalId(internalId, true);
                  var parent = browser.oArgs.parent;
                  browser.destroy();
                  parent.hide();
                  browser_player(internalId, sUrl,
                    // fOnFinish
                    function() {
                      parent.show();
                      parent.focus();
                    }
                  );

                  parent.blur();
                },
              },
              oArgs: {
                parent: HED.window.get(),
              }
            };
            browser = HED.window.create(oOptions);
            browser.focus();
            */
                         
            if (buffer==true){
             Options = {
                url:  data["video_url"],
                title: data["title"],
                load: Load,
                cbmx : function(reason, args){
                  if (reason=="play-ok"){
                    HED.window.get().blur();
                    HED.window.get().hide();
                  }

                  if (reason=="play-error"){
                    HED.window.get().focus();
                    HED.window.get().show();
                    alert("Se ha producido un error al reproducir el vídeo\n" + data["video_url"])
                  }
                  if (reason=="server-nostreams"){
                    HED.window.get().focus();
                    HED.window.get().show();
                    alert("Se ha producido un error al reproducir el vídeo\n" + data["video_url"])
                  }
                  if (reason=="play-finish"){
                    HED.window.get().focus();
                    HED.window.get().show();
                  }
                  if (reason=="play-stop"){
                    HED.window.get().focus();
                    HED.window.get().show();
                  }
                
                },


              }
              HED.helpers.play(Options);
              HED.window.get().blur();
              HED.window.get().hide();
             }else{
             
             if (data["video_url"].indexOf("http://") == 0) {
              Type = "http";
              Options = { 'path' : data["video_url"].slice(7) };
             }else if (data["video_url"].indexOf("/") == 0) {
             Type = "file";
              Options = { 'file' : data["video_url"]};            
             }else{
              Type = "custom";
              Options = { 'url' : data["video_url"]};
             }
             HED.avmedia.play( 
                  
                  {
                     'type': Type,
                     'options': Options,
                     'resume':  true,
                     'details': {
                        'name': data["title"], 
                        'contextmenu': {
                            'duration': 0,
                            'options': [],
                            'render': {},
                            'keyHandler': {},
                            'controls': ["pfr", "stop", "play", "pff", "audio", "subs"],
                            'hideProgressBar': false
                        }
                     }      
                  },
                  function(oResult){HED.window.get().blur();HED.window.get().hide();},
                  function(oError){alert("Se ha producido un error al reproducir el vídeo\n" + data["video_url"])},
                  {
                     'onStart': function(pObject){HED.window.get().blur();HED.window.get().hide();},
                     'onFinish': function(pObject){HED.window.get().focus();HED.window.get().show();}
                  }); 
             }
            break;
        case "Update":
            DescargarContenido(data["url"]);
            CerrarLoading()
            break;
        case "HideLoading":
            CerrarLoading()
            break;
        case "OpenConfig":
            CerrarLoading()
            Opciones = {};
            for (x = 0; x < data["items"].length; x++) {
                if (typeof(Opciones[data["items"][x]["category"]]) == 'undefined') {
                    Opciones[data["items"][x]["category"]] = "";
                }
                switch (data["items"][x]["type"]) {
                    case "sep":
                        Opciones[data["items"][x]["category"]] +=
                            '<li class="ListItem"><div class="Separador"></div></li>';
                        break;
                    case "lsep":
                        Opciones[data["items"][x]["category"]] +=
                            '<li class="ListItem"><div class="LabelSeparador">' + data["items"][x]["label"] + '</div></li>';
                        break;
                    case "text":
                        if (data["items"][x]["option"] == "hidden") {
                            Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Text"><input class="Text" onchange="ChangeSetting(this)" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="password" id="' + data["items"][x]["id"] + '" value="' + data["items"][x]["value"] + '"></div></span</div></li>';
                        } else {
                            Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Text"><input class="Text" onchange="ChangeSetting(this)" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="text" id="' + data["items"][x]["id"] + '" value="' + data["items"][x]["value"] + '"></div></span</div></li>';
                        }
                        break;
                    case "bool":
                        if (data["items"][x]["value"] == "true") {
                            Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Check"><input class="Check" onchange="ChangeSetting(this)" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="checkbox" checked=checked id="' + data["items"][x]["id"] + '" value="' + data["items"][x]["value"] + '"></div></span</div></li>';
                        } else {
                            Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Check"><input class="Check" onchange="ChangeSetting(this)" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="checkbox" id="' + data["items"][x]["id"] + '" value="' + data["items"][x]["value"] + '"></div></span</div></li>';
                        }
                        break;
                    case "labelenum":
                        if (data["items"][x]["values"] === "" || typeof(data["items"][x]["values"]) === "undefined") {
                            Opcion = data["items"][x]["lvalues"].split("|");
                        } else {
                            Opcion = data["items"][x]["values"].split("|");
                        }
                        SOpciones = "";
                        for (y = 0; y < Opcion.length; y++) {
                            if (data["items"][x]["value"] == Opcion[y]) {
                                if (data["items"][x]["lvalues"] === "" || typeof(data["items"][x]["lvalues"]) === "undefined") {
                                    SOpciones += "<option selected=selected>" + data["items"][x]["values"].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option selected=selected>" + data["items"][x]["lvalues"].split("|")[y] +
                                        "</option>";
                                }
                            } else {
                                if (data["items"][x]["lvalues"] === "" || typeof(data["items"][x]["lvalues"]) === "undefined") {
                                    SOpciones += "<option>" + data["items"][x]["values"].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option>" + data["items"][x]["lvalues"].split("|")[y] + "</option>";
                                }
                            }
                        }
                        Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Select"><select class="Select" onchange="ChangeSetting(this)" name="labelenum" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" id="' + data["items"][x]["id"] + '">' + SOpciones + '</select></div></span</div></li>';
                        break;
                    case "enum":
                        
                        if (data["items"][x]["values"] === "" || typeof(data["items"][x]["values"]) === "undefined") {
                            Opcion = data["items"][x]["lvalues"].split("|");
                            for (y = 0; y < Opcion.length; y++) {
                                Opcion[y] = y;
                            }
                        } else {
                            Opcion = data["items"][x]["values"].split("|");
                        }
                        SOpciones = "";
                        for (y = 0; y < Opcion.length; y++) {
                            if (data["items"][x]["value"] == Opcion[y]) {
                                if (data["items"][x]["lvalues"] === "" || typeof(data["items"][x]["lvalues"]) === "undefined") {
                                    SOpciones += "<option selected=selected>" + data["items"][x]["values"].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option selected=selected>" + data["items"][x]["lvalues"].split("|")[y] +
                                        "</option>";
                                }
                            } else {
                                if (data["items"][x]["lvalues"] === "" || typeof(data["items"][x]["lvalues"]) === "undefined") {
                                    SOpciones += "<option>" + data["items"][x]["values"].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option>" + data["items"][x]["lvalues"].split("|")[y] + "</option>";
                                }
                            }
                        }
                        Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Select"><select class="Select" onchange="ChangeSetting(this)" name="enum" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" id="' + data["items"][x]["id"] + '">' + SOpciones + '</select></div></span</div></li>';
                        break;
                    default:
                        break;
                }

            }
            Secciones = "";
            Lista = "";
            for (var key in Opciones) {
                if (Opciones.hasOwnProperty(key)) {
                    Secciones += '<a href="javascript:void(0)" class="Boton" onclick="MostrarSeccion(\'' + key + '\')">' + key + '</a>\n';
                    Lista +=
                        '<ul class="ListItem" style="display:none" id="Config-' + key + '">' + Opciones[key] + '</ul>';
                }
            }
            AbrirConfig(response["id"],data, Secciones, Lista)

            break;

        default:
            break;
    }
}


function GuardarConfig(Guardar) {
    var Ajustes = {};
    if (Guardar === true) {
        JsonAjustes = {};
        Objetos = document.getElementById("Config-popup").getElementsByTagName("input")
        
        for(x=0;x<Objetos.length;x++){
          switch (Objetos[x].type) {
                case "text":
                    JsonAjustes[Objetos[x].id] = Objetos[x].value;
                    break;
                case "password":
                    JsonAjustes[Objetos[x].id] = Objetos[x].value;
                    break;
                case "checkbox":
                    JsonAjustes[Objetos[x].id] = Objetos[x].checked.toString();
                    break;
                case "select-one":
                    JsonAjustes[Objetos[x].id] = Objetos[x].selectedIndex.toString();
                    break;
            }
        }
        Objetos = document.getElementById("Config-popup").getElementsByTagName("select")
        for(x=0;x<Objetos.length;x++){
          switch (Objetos[x].type) {
                case "select-one":
                    if (Objetos[x].name == "enum"){
                      JsonAjustes[Objetos[x].id] = Objetos[x].selectedIndex.toString();
                    } else if (Objetos[x].name == "labelenum"){
                      JsonAjustes[Objetos[x].id] = Objetos[x].value;
                    }
                    break;
            }
        }
        EnviarDatos({"id":document.getElementById("Config-popup").RequestID, "result":JsonAjustes });
    } else {
        EnviarDatos({"id":document.getElementById("Config-popup").RequestID, "result":false });
    }
    
    AbrirLoading()
}