export default class MapObject{

    static nr = 0;

    constructor(){
        MapObject.nr += 1;
        this.id = MapObject.nr;
    }

    draw(){
        console.log("Draw");
    }
}