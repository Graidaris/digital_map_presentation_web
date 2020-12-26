import MapObject from "./mapObj.js"

export default class Line extends MapObject{

    constructor(){
        super()
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
        console.log(`P1 = ${x}, ${y}`)
    }

    setP2Coord(x,y){
        this.coord.x2 = x;
        this.coord.y2 = y;
        console.log(`P2 = ${x}, ${y}`)
    }

    setCoord(coord){
        this.coord = coord;
    }

    draw(){
        return `
        <line 
        id="Line_${this.id}"
        x1="${this.coord.x1}" y1="${this.coord.y1}" 
        x2="${this.coord.x2}" y2="${this.coord.y2}" 
        stroke-width="3" stroke="rgb(0,0,0)"        
        />`
    }

}