window.onload = function() {
    //IP ="192.168.2.102";
    //Port ="8081";
    //HED.window.enable_debug()
    //HED.window.show_debug_window()
    HED.configuration.get_key("ip",function(key){IP=key[0]["value"]},function(key){IP="localhost"})
    HED.configuration.get_key("port",function(key){Port=key[0]["value"];},function(key){Port="8889"})
    GetDevices();
    Dispose();
    WebSocketConnect();
    DescargarContenido("");
};
window.onresize = function() {
    Dispose();
};

function GetDevices() {
   HED.fs.get_devices(undefined, undefined,
      ['name','root','type','subtype','volume'],
      'type',
      'asc',
      [{'by': 'type', 'value':'local'}],
      
      function(oDevices) {         
         next_device(0);
         function next_device(i) {
            if (i >= oDevices.length) {
            }
            var device_id = (oDevices[i].root.split('/by-id/')[1]).split('/')[0];
            HED.fs.get_files(
               {
                  'device': oDevices[i].name,               
                  'path': "/bg_apps/pelisalacarta/",
                  'order': 'name',
                  'dir': 'asc',
                  'mediaTypes': ['dir']                  
               },
               function(oFiles){
                  for (var j in oFiles.list) {
                     PythonPath = oDevices[i].root + "/bg_apps"
                     return
                  }                  
                  next_device(i+1);
               },
               function(oError) {
                  next_device(i+1);
               }
            );
            
         }
      },
      function(oError) {}
   );   
}