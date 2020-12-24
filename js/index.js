import Line from "./line.js"
import MapObject from "./mapObj.js"

const INFO_DIV = document.getElementById("infoDiv");

var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

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
        objArr.push(new Line(ctx));
        objArr[objArr.length - 1].setP1Coord(mousePos.x, mousePos.y);
        click = 1;
    }else{
        objArr[objArr.length - 1].setP2Coord(mousePos.x, mousePos.y);
        objArr[objArr.length - 1].draw();
        click = 0;
    }  
}


canvas.addEventListener("click", function (evt) {   
    let mousePos = getMousePos(canvas, evt); 
    if(modeActive){
        switch (mode) {
            case MODES.LINE:
                console.log("Line");
                addLine(mousePos);
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