
var addLineToMap;
var addPolygonToMap;
var setCenterMap;

var objects = {};


function showObjects(){
    console.log(objects);
}

function hideLayer(ch_box_id, layer_name){ 
    let check_box = document.getElementById(ch_box_id);
    if (check_box.checked){
        objects[layer_name].forEach(element => element.visible = true);
    }else{
        objects[layer_name].forEach(element => element.visible = false);
    }
}


require([
    "esri/Map",
    "esri/views/MapView",
    "esri/Graphic",
    "esri/layers/GraphicsLayer"
    ], function(Map, MapView, Graphic, GraphicsLayer) {

    var map = new Map({
        basemap: "satellite"
    });

    var view = new MapView({
        container: "viewDiv",
        map: map,
        zoom: 3
    });

    var graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);


    addLineToMap = function (name_layer, paths, color){

        var simpleLineSymbol = {
            type: "simple-line",
            color: color, // orange
            width: 2
        };

        var polyline = {
            type: "polyline",
            paths: paths
        };

        var polylineGraphic = new Graphic({
            geometry: polyline,
            symbol: simpleLineSymbol
        });

       
        addObjectToDict(name_layer, polylineGraphic);
        graphicsLayer.add(polylineGraphic);

    }

    addPolygonToMap = function (name_layer, paths, color){
        var polygon = {
            type: "polygon",
            rings: paths
          };
          color.push(0.8)
        var simpleFillSymbol = {
            type: "simple-fill",
            color: color,
            outline: {
                color: [255, 255, 255],
                width: 1
            }
        };
   
        var polygonGraphic = new Graphic({
            geometry: polygon,
            symbol: simpleFillSymbol
        });
        
        addObjectToDict(name_layer, polygonGraphic);
        graphicsLayer.add(polygonGraphic);
    }


    setCenterMap = function(lon, lat){
        view.center = [lon, lat];
        view.zoom = 15
    }

    

    function addObjectToDict(name_layer, obj){
        if (name_layer in objects){
            objects[name_layer].push(obj);
        }else{
            objects[name_layer] = [obj]
        }
    }

});