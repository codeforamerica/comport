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
percentFmt = d3.format(".1f");

function percentFormat(d){
  if(d.percent === undefined ){
    return "";
  }
  var num = percentFmt(d.percent * 100);
  return num + '<span class="percent">%</span>';
}

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

function symmetricalFlags(config, data){

  if(data.length == 0){
    return;
  }

  var raceKeys = [
    "White", "Black", "Hispanic", "Asian", "Other"];
  var raceColors = [
    "#a865a8", "#00a6d2", "#fdb81e", "#4aa564", "#cd2026"];

  var raceMap = d3.map();
  raceKeys.forEach(function(r, i){
    raceMap.set(r, {
      color: raceColors[i],
      race: r,
    });
  });

  ['city', 'department'].forEach(function(entity){
    var total = 0;
    var subset = data.filter(function(d){
          return d.entity == entity.toLowerCase();
        });
    subset.forEach(function(d){
      total += d.count;
    });
    subset.forEach(function(d){
      d.percent = d.count / total;
      var datum = raceMap.get(d.race)
      datum[entity] = d;
    });
  });

  var data = raceKeys.map(function(r){
    var d = raceMap.get(r);
    // if there is only city or department, but not both
    // http://stackoverflow.com/a/4540481/418586
    if( !d.city ^ !d.department  ){
      var filler = {
        count: 0,
        percent: 0
      }
      if( !d.city ){
        d.city = filler;
      } else {
        d.department = filler;
      }
    }
    return raceMap.get(r);
  }).filter(function(d){
    return d;
  });

  var table = d3.select(config.parent).append("table")
    .attr("class", "sym-flag-table");

  var rows = table.selectAll("tr")
    .data(data).enter()
    .append("tr")
    .attr("class", "sym-flag-row");

  rows.append("th").attr("class", 'sym-flag-row-label')
    .text(function(d){ return d.race; });

  ['city', 'department'].forEach(function(entity, right){
    var flagCells = rows.append("td")
      .attr("class", 'flag-cell ' + (right ? 'flag-right' : 'flag-left'));
    function makeFlags(cells){
      cells.append("span")
        .attr("class", "sym-flag-bar")
        .style("width", function(d){ return (d[entity].percent * 75) + "%"; })
        .style("background-color", function(d){ return d.color; });
    }
    function makeLabels(cells){
      cells.append("span")
        .attr("class", "sym-flag-label")
        .html(function(d){
          return percentFormat(d[entity]);
        });
    }
    if( right ){
      makeFlags(flagCells);
      makeLabels(flagCells);
    } else {
      makeLabels(flagCells);
      makeFlags(flagCells);
    }
  });

  var headers = table.insert("tr", ":first-child")
    .attr("class", "sym-flag-col-header")
    .selectAll("th")
    .data(["", "residents", "officers"]).enter()
    .append("th")
    .attr("class", "sym-flag-col-header")
    .text(String);

}
