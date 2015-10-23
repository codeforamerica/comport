/*
This contains two charting functions: 

1) `basicPercent`, use to draw a list of percents as a chart. 
2) `flagHistogram`, creates an html table that contains labels in the left column and 
   bars with quantities in the right column.

All chart drawing functions take two arguments:

1) a `config` object
2) structured `data`

All chart configs are coming from `chartConfigs.js`, so you can find examples there.

`charts.js` processes each config object, structures data accordingly, finds the correct drawing function,
and then passes config and structured data into the drawing function. 

*/
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
  var width,
      font_size;

  font_size = 14; // px
  width = 12;
  
  // set y axis scale
  var yScale = d3.scale.linear()
    .domain([ 0, 
        d3.max(data, function(d){ return d[config.y]; })
        ])
    .range([0, font_size * width]);

  var y = function(d){ return yScale(d[config.y]) };

  // draw containing table node
  var table = d3.select(config.parent)
    .append("table")
    .attr("class", "flagHistogram-table");

  var rows = table.selectAll("tr")
    .data(data).enter()
    .append("tr")
    .attr("title", function(d){
      if( d[config.x] == "Other" ){
        return "Other includes:\n- " + d.groups.map(function(d){
          return d.type + " (" + d.count + ")";
        }).join("\n- ");
      }
    })
    .style("cursor", function(d){
      if(d[config.x] == "Other"){
        return "pointer";
      } else {
        return "auto";
      }
    });

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

