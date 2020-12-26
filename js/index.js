import Line from "./line.js"
import MapObject from "./mapObj.js"


const INFO_DIV = document.getElementById("infoDiv");
const INFO_DIV2 = document.getElementById("infoDiv2");

var svgCanvas = document.getElementById("mySVG");
var viewPort =  svgCanvas.querySelector('.svg-pan-zoom_viewport');
svgPanZoom(svgCanvas, {
    viewportSelector: viewPort
});


let click = 0;
let objArr = new Array();

const MODES = {
    NONE:0,
    LINE:1,
    POLYGON:2,
    POINT:3
}

let modeActive = false;
let mode = MODES.NONE;

const lineOption = document.getElementById("drowLineButton");


showInfo();

///________________________________________________________

lineOption.addEventListener("click", function (evt){
    if(modeActive){
        modeActive = false;
        this.style.backgroundColor = "";
        this.style.color = "";
        mode = MODES.NONE;
    }else{
        modeActive = true;
        this.style.backgroundColor = "red";
        this.style.color = "white";
        mode = MODES.LINE;
    }
})

function addLine(mousePos){
    if(click == 0){
        objArr.push(new Line());
        objArr[objArr.length - 1].setP1Coord(mousePos.x, mousePos.y);
        click = 1;
    }else{
        objArr[objArr.length - 1].setP2Coord(mousePos.x, mousePos.y);
        let inner = objArr[objArr.length - 1].draw();
        viewPort.innerHTML += inner;
        click = 0;
        
    }  
}

svgCanvas.addEventListener("mousemove", function (evt){
    let mousePos = getMousePos(svgCanvas, evt); 
    INFO_DIV2.innerHTML =  `${mousePos.x}, ${mousePos.y}`;
});




svgCanvas.addEventListener("click", function (evt) {   
    let mousePos = getMousePos(svgCanvas, evt); 
    let points = transformPoints(mousePos, getTransformMatrix(viewPort))
    
    
    if(modeActive){
        switch (mode) {
            case MODES.LINE:
                console.log("Line");
                addLine(points);
                break;
        
            default:
                console.log("Other")
                break;
        }

        
    }

    showInfo();
}, false);

function getMousePos(cnv, evt){
    var rect = cnv.getBoundingClientRect();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
    };
}



function showInfo(){
    let str = "Num of obj = " + objArr.length;

    INFO_DIV.innerHTML = str;
}

function getTransformMatrix(element){
    let attr = element.getAttribute("transform");
    let numbers = attr.substring(attr.lastIndexOf('(')+1).slice(0, -1).split(',')
    return {
        a: parseFloat(numbers[0]),
        b: parseFloat(numbers[1]),
        c: parseFloat(numbers[2]),
        d: parseFloat(numbers[3]),
        e: parseFloat(numbers[4]),
        f: parseFloat(numbers[5]),
    }
}

function transformPoints(point, matrix){    
    let y = (point.y - (matrix.b*point.x)/matrix.a + (matrix.b*matrix.e)/matrix.a - matrix.f)/(matrix.d-(matrix.b*matrix.c)/matrix.a);
    let x = (point.x - matrix.c*y - matrix.e)/matrix.a;
    return {x:x, y:y};
}


