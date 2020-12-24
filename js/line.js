import MapObject from "./mapObj.js"

export default class Line extends MapObject{

    constructor(context){
        super(context)
        this.coord = {
            x1 : 0,
            y1 : 0,
            x2 : 0,
            y2 : 0
        };
        this.name = "";
    }

    setP1Coord(x,y){
        this.coord.x1 = x;
        this.coord.y1 = y;
    }

    setP2Coord(x,y){
        this.coord.x2 = x;
        this.coord.y2 = y;
    }

    setCoord(coord){
        this.coord = coord;
    }

    draw(){
        this.context.beginPath();
        this.context.moveTo(this.coord.x1, this.coord.y1);
        this.context.lineTo(this.coord.x2, this.coord.y2);
        this.context.stroke();
    }

}