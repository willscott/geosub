var map;
var markers;
function init(){
  map = new OpenLayers.Map('map', {
    controls: [
      new OpenLayers.Control.ScaleLine(),
      new OpenLayers.Control.Navigation(),
      new OpenLayers.Control.Zoom(),
      new OpenLayers.Control.KeyboardDefaults()
    ]
  });

  var layer = new OpenLayers.Layer.OSM("Simple OSM Map");
  map.addLayer(layer);
  
  map.setCenter(new OpenLayers.LonLat(-122.4, 47.7).transform(
      new OpenLayers.Projection("EPSG:4326"),
      map.getProjectionObject()
  ), 9);

  markers = new OpenLayers.Layer.Markers( "Markers" );
  map.addLayer(markers);

  initPlaceChooser();
}

function initPlaceChooser() {
  var container = document.getElementById('interests');
  var places = container.getElementsByTagName('input');
  for(var i = 0; i < places.length; i++) {
    places[i].addEventListener('change', placeChange, true);
  }
}

function placeChange(e) {
  var place = e.target;
  if (!place.value) {
    return;
  }
  lookupPlace(place.value, function(place, val) {
    if (val) {
      place.previousSibling.style.borderBottom = '0px';

      var size = new OpenLayers.Size(21,25);
      var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
      var icon = new OpenLayers.Icon(place.previousSibling.src, size, offset);
      markers.addMarker(new OpenLayers.Marker(val, icon));
    } else {
      place.previousSibling.style.borderBottom = '2px solid red';
    }
  }.bind(this, place));
}

function lookupPlace(addr, callback) {
  addr += " seattle, wa";

  var onResp = function requestSuccess(cb, response) {
    try {
      var resp = JSON.parse(response.responseText);
      var latlong = new OpenLayers.LonLat(resp[0]['lon'], resp[0]['lat']);
      cb(latlong.transform(
          new OpenLayers.Projection("EPSG:4326"),
          map.getProjectionObject()));
    } catch(e) {
      cb(false);
    }
  }
  OpenLayers.Request.GET({
    url: "http://nominatim.openstreetmap.org/search?q=" + encodeURIComponent(addr) + "&countrycodes=us&limit=1&format=json",
    scope: this,
    failure: callback.bind(this, false),
    success: onResp.bind(this, callback),
    headers: {"Content-Type": "application/x-www-form-urlencoded"}
  });
}

function addEventMarker(lat, lon, data) {
  console.log("lat: " + lat + " lon: " + lon + " data: " + data);
  var latlong = new OpenLayers.LonLat(lon, lat);
  latlong.transform(
          new OpenLayers.Projection("EPSG:4326"),
          map.getProjectionObject());

  var size = new OpenLayers.Size(21,25);
  var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
  var icon = new OpenLayers.Icon('static/img/marker.png', size, offset);
  markers.addMarker(new OpenLayers.Marker(latlong, icon));
}

window.addEventListener('load', init, true);
