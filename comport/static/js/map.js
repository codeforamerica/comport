function mapChart(config, data){
  console.log("data for map", data);
  var mapWrapper = d3.select(config.parent);
  var div = mapWrapper[0][0];
  mapWrapper.style('width', '50em')
    .style('height', '30em');

  L.mapbox.accessToken = 'pk.eyJ1IjoiY29kZWZvcmFtZXJpY2EiLCJhIjoiSTZlTTZTcyJ9.3aSlHLNzvsTwK-CYfZsG_Q';
  var map = L.mapbox.map(div, 'mapbox.streets');
}
