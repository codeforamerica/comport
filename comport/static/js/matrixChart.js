function matrixChart(config, data){

  // set basic dimensions
  // we need a width, a height for each
  var height,
      width,
      font_size;

  font_size = 14; // px
  
  // draw table
  var table = d3.select(config.parent)
    .append("table")
    .attr("class", "matrix-table");

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
