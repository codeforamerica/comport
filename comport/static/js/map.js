
function mapChart(config, data){
  L.mapbox.accessToken  = "pk.eyJ1IjoiY29kZWZvcmFtZXJpY2EiLCJhIjoiSTZlTTZTcyJ9.3aSlHLNzvsTwK-CYfZsG_Q"

  console.log("data for map", data);
  var mapWrapper = d3.select(config.parent);
  var div = mapWrapper[0][0];
  mapWrapper.style('width', '50em')
    .style('height', '30em');

  var map = L.mapbox.map(div, 'mapbox.light')
    .setView([39.759729, -86.154723], 10)

  var maxY = d3.max(data.values(), function(d){ return d[config.y]; });

  // make color scale
  var colorScale = d3.scale.linear()
    .domain([1, 
        maxY
        ])
    .range([
      d3.rgb("#ffffb2"),
      d3.rgb("#bd0026")
      ]);

  // make the styling function
  function style(f) {

    var y = f.properties[config.y];

    if(y){
      var color = colorScale(y);
    } else {
      var color = "#cccccc"
    }
    return {
      fillColor: color,
      weight: 1,
      opacity: 0.7,
      color: 'white',
      fillOpacity: 0.7
    };
  }

  d3.json("/static/indy_tracts.geojson", function(error, json) {

    json.features.forEach(function(feature){
      var tract_id = feature.properties['NAME'];
      var incident_data = data.get(tract_id);
      if( incident_data ){
        feature.properties[config.y] = incident_data[config.y];
        feature.properties['incidents'] = incident_data['incidents'];
      }
    });

    console.log("geojson!", json);

    var tracts = L.mapbox.featureLayer(json, {style: style})
        .addTo(map);

    var tracts = d3.selectAll('.leaflet-overlay-pane path');

    console.log("tracts", tracts);


  });

}
