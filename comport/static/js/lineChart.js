function lineChart(config, data){
  // creates one chart, using parsed data

  // get basic dimensions (in ems)
  var height,
      width,
      margin,
      xWidth,
      dot_radius,
      font_size;
  margin = { top: 2, right: 3, bottom: 3, left: 2 };
  font_size = 14; // px
  xWidth = 4;
  height = 8;
  width = (data.length * xWidth);
  dot_radius = 0.5;
  var xAxisTickFormat = config.xTickFormat || d3.format('d');


  // determine x axis scale
  var xScale = d3.scale.linear()
    .domain([
        d3.min(data, function(d){return d[config.x];}),
        d3.max(data, function(d){return d[config.x];})
        ])
    .range([
        0,
        font_size * width
        ]);

  // determine y axis scale
  var yScale = d3.scale.linear()
    .domain([
        0,
        d3.max(data, function(d){return d[config.y];})
        ])
    .range([
        font_size * height,
        0
        ]);

  // create the x and y functions
  var x = function(d){ return xScale(d[config.x]); }
  var y = function(d){ return yScale(d[config.y]); }

  // draw svg
  var svg = d3.select(config.parent)
    .append("svg")
    .attr("class", "line-chart")
    .attr("height", (height + margin.top + margin.bottom) + "em")
    .attr("width", (width + margin.left + margin.right) + "em");

  // draw chart container
  var g = svg.append("g")
    .attr("class", "chart-box")
    .attr("transform", translate(
        font_size * margin.left,
        font_size * margin.top
      ));

  // draw x axis
  var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom")
    .tickFormat(xAxisTickFormat);

  g.append("g")
    .attr("class", "x axis")
    .attr("transform", translate(0,
            font_size * ( height + ( margin.bottom * 0.25))
            ))
    .call(xAxis);

  // draw tick lines
  var tickLine = g.selectAll(".tick-line")
    .data(data).enter().append("line")
    .attr("class", "tick-line")
    .attr("transform", function(d){ return translate( x(d), y(d) ); })
    .attr("y2", function(d){
      return  (font_size * height) 
              - y(d)
              + (font_size * 0.5);
    });
  
  // draw line
  var lineFunction = d3.svg.line()
    .x(function(d){ return x(d); })
    .y(function(d){ return y(d); });
  var line = g.append("path")
    .datum(data)
    .attr("class", "trend-line")
    .attr("d", lineFunction);

  var dotBoxes = g.selectAll(".datum")
    .data(data).enter().append("g")
    .attr("class", "datum")
    .attr("transform", function(d){
      return translate( x(d), y(d) );
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

}


