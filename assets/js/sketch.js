var font;
var vehicles = [];

function preload() {
  font = loadFont('assets/AvenirNextLTPro-Demi.otf');
}

function setup() {
  createCanvas(1200, 300);
  background('white');

  var points = font.textToPoints('Connexus', 100, 200, 192);

  for (var i = 0; i < points.length; i++) {
    var pt = points[i];
    var vehicle = new Vehicle(pt.x, pt.y);
    vehicles.push(vehicle);
  }
}

function draw() {
  background('white');
  for (var i = 0; i < vehicles.length; i++) {
    var v = vehicles[i];
    v.behaviors();
    v.update();
    v.show();
  }
}
