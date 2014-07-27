import csv
import urllib
import simplejson
import webbrowser
from datetime import datetime
startTime=datetime.now()

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_coordinates(query):
    query = query.encode('utf-8')
    params = {
        'address': query
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        print latitude, longitude
    return latitude, longitude



#Will be used to launch a web browser and view the output
filepath = 'file:///c:/python27/waterindia.html'
htmlCoords=""
with open('water.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        try:
            lat,lon=get_coordinates(row[4])
            htmlCoords+='new google.maps.LatLng('+str(lat)+","+str(lon)+"),"
        except:
            pass

#To remove the last comma which gets added by iteration of the previous statement.        
jsInput = htmlCoords[:-1]

#Create the HTML file
outputFile = open('waterindia.html','w')
message="""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Heatmap</title>
    <style>
      html, body, #map-canvas {
        height: 100%;
        margin: 0px;
        padding: 0px
      }
      #panel {
        position: absolute;
        top: 5px;
        left: 50%;
        margin-left: -180px;
        z-index: 5;
        background-color: #fff;
        padding: 5px;
        border: 1px solid #999;
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=visualization"></script>
    <script>

    var map, pointarray, heatmap;

    var taxiData = ["""+jsInput+"""
  
    ];

    function initialize() {
      var mapOptions = {
        zoom: 2,
        center: new google.maps.LatLng(0,0),
        mapTypeId: google.maps.MapTypeId.ROADMAP
        styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#000000"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#000000"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":17},{"weight":1.2}]}]
    };

     map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

      var pointArray = new google.maps.MVCArray(taxiData);

      heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray
      });

  heatmap.setMap(map);
    }

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}



google.maps.event.addDomListener(window, 'load', initialize);

    </script>
  </head>

  <body>
    <div id="panel">
      <button onclick="toggleHeatmap()">Toggle Heatmap</button>
      <button onclick="changeGradient()">Change gradient</button>
      <button onclick="changeRadius()">Change radius</button>
    </div>
    <div id="map-canvas"></div>
  </body>
</html>"""
outputFile.write(message)
outputFile.close()

#Launch a browser to view the results
webbrowser.open(filepath)



