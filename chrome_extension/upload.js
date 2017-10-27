
function getUserInfo(userInfo) {
	user_email = userInfo.email;
	console.log(user_email);
    if(user_email){
        document.getElementById("hello").innerHTML="Hello, "+user_email;
    }
}

chrome.identity.getProfileUserInfo(getUserInfo);

var marker = null;
var map = null;
var curlat=39.85990;
var curlng=116.40472;

function initMap() {
        var uluru = {lat: 39.85990, lng: 116.40472};
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: uluru
        });
        marker = new google.maps.Marker({
          position: uluru,
          draggable: true,
          map: map
        });
  document.getElementById("lat").value=39.85990;
  document.getElementById("lng").value=116.40472;
  markerCoords(marker);
}

function markerCoords(markerobject){
    google.maps.event.addListener(markerobject, 'dragend', function(evt){
        curlat=evt.latLng.lat().toFixed(5);
        curlng=evt.latLng.lng().toFixed(5);
        document.getElementById("lat").value=curlat;
        document.getElementById("lng").value=curlng;
        map.panTo(new google.maps.LatLng(curlat,curlng));
    });
}


var url= "<a href=\'http://pigeonhole-apt.appspot.com/view_single?stream_id=PigeonFamily \' >Click Here</a> to view the full stream"

$( "#upload-form" ).submit(function( event ) {
    event.preventDefault();
    this.submit();
    document.getElementById("urlinput").value="";
    document.getElementById("response").innerHTML="You have successfully upload your image. "+ url;
});


$(document).ready(function(){
   $('body').on('click', 'a', function(){
     chrome.tabs.create({url: $(this).attr('href')});
     return false;
   });
});


