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
}

placeChange = function(element, value, callback) {
  if (!value[0]) {
    return;
  }
  lookupPlace(value[0], function(element, val, cb, res, lat, lon) {
    if (res) {
      element.previousSibling.style.borderBottom = '0px';

      var size = new OpenLayers.Size(21,25);
      var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
      var icon = new OpenLayers.Icon(element.previousSibling.src, size, offset);
      markers.addMarker(new OpenLayers.Marker(res, icon));
      val[1] = lat;
      val[2] = lon;
    } else {
      element.previousSibling.style.borderBottom = '2px solid red';
      val[1] = 0;
      val[2] = 0;
    }
    cb();
  }.bind(this, element, value, callback));
}

function lookupPlace(addr, callback) {
  addr += " seattle, wa";

  var onResp = function requestSuccess(cb, response) {
    try {
      var resp = JSON.parse(response.responseText);
      var latlong = new OpenLayers.LonLat(resp[0]['lon'], resp[0]['lat']);
      cb(latlong.transform(
          new OpenLayers.Projection("EPSG:4326"),
          map.getProjectionObject()), resp[0]['lat'], resp[0]['lon']);
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
