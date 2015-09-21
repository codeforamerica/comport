var percentFormat = d3.format("d");

function basicPercent(config, data){
 var div = d3.select(config.parent);
 var rows = div.selectAll(".percentStatement")
   .data(data).enter().append("div")
   .attr("class", "percentStatement");

 var percents = rows.selectAll(".percent")
   .data(function(d){
     return [
       { "label": config.x,
         "amt": (d[config.x] / d.total) * 100 },
       { "label": config.y,
         "amt": (d[config.y] / d.total) * 100 }
     ];
   }).enter()
   .append("span")
   .attr("class", "percent");

 percents.append("span")
   .attr("class", "percent-amt")
   .text(function(d){
     console.log("percent", d);
     return d3.round(d.amt, 0);
   }).append("sup")
  .attr("class", "percent-symbol")
  .text("%");

  percents.append("span")
    .attr("class", "percent-label")
    .text(function(d){ return d.label; });

}

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
  
  // set y axis scale
  var yScale = d3.scale.linear()
    .domain([ 0, 
        d3.max(data, function(d){ return d[config.y]; })
        ])
    .range([0, font_size * width]);

  var y = function(d){ return yScale(d[config.y]) };

  // draw table
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
