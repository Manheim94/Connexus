var font;
var vehicles = [];

function preload() {
  font = loadFont('assets/AvenirNextLTPro-Demi.otf');
}

function setup() {
  var canvas = createCanvas(1110, 300);
  canvas.parent('sketch-holder');
  background('rgba(220,255,210, 0.0)');

  var points = font.textToPoints('Connexus', 100, 200, 192);

  for (var i = 0; i < points.length; i++) {
    var pt = points[i];
    var vehicle = new Vehicle(pt.x, pt.y);
    vehicles.push(vehicle);
  }
}

function draw() {
  background('rgba(240, 237, 242, 1.0)');
  for (var i = 0; i < vehicles.length; i++) {
    var v = vehicles[i];
    v.behaviors();
    v.update();
    v.show();
  }
}
