
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


var color;
var oldKey = '';

function processLines(lines){
    Object.entries(lines).forEach(([key, value]) => {
        if (key != oldKey){
            color = getRandomColor();
            oldKey = key;
        }

        value['longlat'].forEach(element => addLineToMap(key, element, color));
    });    
}

function processPolygons(lines){
    Object.entries(lines).forEach(([key, value]) => {
        if (key != oldKey){
            color = getRandomColor();
            oldKey = key;
        }
        value['longlat'].forEach(element => addPolygonToMap(key, element, color));
    });    
}

function getRandomColor(){
    let r = getRandomInt(255);
    let g = getRandomInt(255);
    let b = getRandomInt(255);
    return [r,g,b]
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}