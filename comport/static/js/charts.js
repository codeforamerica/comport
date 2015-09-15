// Chart steps:
// 1. data query
// 2. axes
// 3. sizes
var currentYear = 2015;
var defaultNullValue = "NULL";
var xAxisTickFormat = d3.format("d");


function mergeMaps(a, b){
  b.forEach(function(k, v){
    a.set(k, v);
  });
}

function nullify(value){
  if (value === defaultNullValue){
    return null;
  } else {
    return value
  }
}

var dateTimeFormat = d3.time.format("%Y-%m-%d %H:%M:%S");
var dateTimeKey = "occuredDate";

function parseDate(dateTimeString){
  return dateTimeString ? dateTimeFormat.parse(dateTimeString) : null;
}

function parseData(rows){
  // parses dates and nulls from the raw csv
  rows.forEach(function(r){
    var dateString = nullify(r[dateTimeKey]);
    if( dateString === null ){
      dateString = r[backupDateTimeKey];
    }
    r.date = parseDate(dateString);
  });
  return rows;
}

d3.csv(
  "/department/1/uof.csv ",
  function(error, rows){
    uofByYear(
      parseData(rows)
      );
});

function structureData(parsed_rows){
  // restructures csv data into data than can be used to draw a chart
  // create a grouping machine that groups by year
  var unmapped_data = d3.nest()
    .key(function(d){ return d.date.getFullYear(); })
    .rollup(function(leaves){
      return { "count": leaves.length,
        "incidents": leaves,
        "year": leaves[0].date.getFullYear()
      };
    });

  // use the parsed data and the grouping machine to create a
  // simple key value store (aka "map") with years as keys
  var data = unmapped_data.map(parsed_rows, d3.map);

  // add missing years to the map, so we know they are empty
  var year0 = d3.min(data.keys());
  var allYears = d3.range(year0, currentYear);
  allYears.forEach(function(yr){
    if( !data.has(yr) ){
      data.set(
        yr, {
          year: yr,
          count: 0,
          incidents: [],
        }
      );
    }
  });

  // return data structured for a chart
  return data.values();
}

function uofByYear(rows){
  // creates one chart, using parsed data

  // restructure the data
  var data = structureData(rows);
  console.log("data", data);

  // get basic dimensions (in ems)
  var height,
      width,
      margin,
      year_width,
      dot_radius,
      font_size;
  margin = { top: 2, right: 2, bottom: 3, left: 2 };
  font_size = 14; // px
  year_width = 7;
  height = 14;
  width = (data.length * year_width);
  dot_radius = 0.5;

  // determine x axis scale
  var x = d3.scale.linear()
    .domain([
        d3.min(data, function(d){return d.year;}),
        d3.max(data, function(d){return d.year;})
        ])
    .range([
        0,
        font_size * width
        ]);

  // determine y axis scale
  var y = d3.scale.linear()
    .domain([
        0,
        d3.max(data, function(d){return d.count;})
        ])
    .range([
        font_size * height,
        0
        ]);

  // draw svg
  var svg = d3.select(".chart.per.year.uof")
    .append("svg")
    .attr("class", "line-chart")
    .attr("height", (height + margin.top + margin.bottom) + "em")
    .attr("width", (width + margin.left + margin.right) + "em");

  // draw chart container
  var g = svg.append("g")
    .attr("class", "chart-box")
    .attr("transform", "translate("
        + (font_size * margin.left) + ","
        + (font_size * margin.top) + ")");

  // draw x axis
  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(xAxisTickFormat);
  g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + (
            font_size * (
              height + (
                margin.bottom * 0.25
                ))
            ) + ")")
    .call(xAxis);

  // draw tick lines
  var tickLine = g.selectAll(".tick-line")
    .data(data).enter().append("line")
    .attr("class", "tick-line")
    .attr("transform", function(d){
      return "translate("
      + x(d.year) + ","
      + y(d.count) + ")";
    })
    .attr("y2", function(d){
      return  (font_size * height) 
              - y(d.count)
              + (font_size * 0.5);
    });
  

  var lineFunction = d3.svg.line()
    .x(function(d){ return x(d.year); })
    .y(function(d){ return y(d.count); });

  // draw line
  var line = g.append("path")
    .datum(data)
    .attr("class", "trend-line")
    .attr("d", lineFunction);

  var dotBoxes = g.selectAll(".datum")
    .data(data).enter().append("g")
    .attr("class", "datum")
    .attr("transform", function(d){
      return "translate(" + x(d.year) + ","
        + y(d.count) + ")";
    });

  // draw dots
  var dots = dotBoxes.append("circle")
    .attr("class", "dot")
    .attr("r", font_size * dot_radius);

  // draw text
  var dotText = dotBoxes.append("text")
    .attr("class", "datum-text")
    .attr("y", -15)
    .attr("text-anchor", "middle")
    .text(function(d){return d.count;});

  // draw y axis
  //var yAxis = d3.svg.axis()
    //.scale(y)
    //.orient("left");
  //g.append("g")
    //.attr("class", "y axis")
    //.call(yAxis);

}
