dojo.require("esri.map");
var map; 

function init() {
    map = new esri.Map("viewDiv");
    
    map.addLayer(
            new esri.layers.ArcGISTiledMapServiceLayer("http://server.arcgisonline.com/ArcGIS/rest/services/ESRI_Imagery_World_2D/MapServer")
        );
}

function addLineToMap() {
    let lon1= -122.44400024414062;
    let lat1= 37.75382995605469;
    let lon2= -112.44400024414062;
    let lat2= 27.75382995605469;
       var point1 = new esri.geometry.Point(lon1, lat1, map.spatialReference);
       var point2 = new esri.geometry.Point(lon2, lat2, map.spatialReference);
       var line = new esri.geometry.Polyline(map.spatialReference);
       line.addPath([point1, point2]);
       var lineSymbol = new esri.symbol.SimpleLineSymbol(esri.symbol.SimpleLineSymbol.STYLE_SOLID, new dojo.Color([255,0,0,0.5]),3);
       var pointSymbol = new esri.symbol.SimpleMarkerSymbol().setColor(new dojo.Color([255,0,0, 0.5]));
       map.graphics.add(new esri.Graphic(point1, pointSymbol));
       map.graphics.add(new esri.Graphic(point2, pointSymbol));
       map.graphics.add(new esri.Graphic(line, lineSymbol))
 
}

function addLineToMap2() {
    var simpleLineSymbol = {
        type: "simple-line",
        color: [226, 119, 40], // orange
        width: 2
      };

    var lineSymbol = new esri.symbol.SimpleLineSymbol(esri.symbol.SimpleLineSymbol.STYLE_SOLID, new dojo.Color([255,0,0,0.5]),3);

   

    var polyline = {
        type: "polyline",
        paths: [
            [-118.821527826096, 34.0139576938577],
            [-122.814893761649, 34.0080602407843],
            [-152.808878330345, 34.0016642996246]
        ]
    };
    
    var polylineGraphic = new  esri.Graphic({
        geometry: polyline,
        symbol: lineSymbol
    });

      map.graphics.add(polylineGraphic);
 
}
   
   
dojo.addOnLoad(init);