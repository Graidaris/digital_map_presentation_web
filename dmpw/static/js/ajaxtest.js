
function ajaxGeometryLoad(){
    console.log("AJAX")
    $.ajax({
        url: '/getGeometry',
        method: 'get',
        cache: false,
        success: processResult
    });
}

function processResult(results){
    lines = results['geo_linestrings'];
    poligons = results['geo_poligons'];
    processLines(lines);
    processPolygons(poligons);

    setCenterMap(
            results['geo_statistic']['MIN_LON'],
            results['geo_statistic']['MIN_LAT']
        );
}

function processLines(lines){
    Object.entries(lines).forEach(([key, value]) => {
      value['longlat'].forEach(element => addLineToMap(key, element));
     });    
}

function processPolygons(lines){
    Object.entries(lines).forEach(([key, value]) => {
      value['longlat'].forEach(element => addPolygonToMap(key, element));
     });    
}