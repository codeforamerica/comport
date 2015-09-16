function flagHistogram(config, data){

  // set basic dimensions
   // we need a width, a height for each
  var height,
      width,
      margin,
      barHeight,
      font_size;

  font_size = 14; // px
  barHeight = 5; 
  height = (data.length * barHeight);
  width = 20
  
  // set x axis scale
  var yScale = d3.scale.linear()
    .domain([ 0, 
        d3.max(data, function(d){ return d[config.y]; })
        ])
    .range([0, font_size * width]);

  var y = function(d){ return yScale(d[config.y]) };

  // set y axis scale
  // x and y functions
  // draw svg
  var table = d3.select(config.parent)
    .append("table")
    .attr("class", "flagHistogram-table");

  var rows = table.selectAll("tr")
    .data(data).enter()
    .append("tr");

  var rowLabels = rows.append("td")
    .attr("class", "hist-label")
    .text(function(d){ return d[config.x] || "Unspecified"; });

  var flags = rows.append("td")
    .attr("class", "hist-flag");

  var flagBars = flags.append("span")
    .attr("class", "hist-flag-bar")
    .style("width", function (d){ return y(d) + "px"; });

  var flagLabels = flags.append("span")
    .attr("class", "hist-flag-label")
    .text(function(d){ 
      return d[config.y];
    });

}

function mountainHistogram(config, data){

}
