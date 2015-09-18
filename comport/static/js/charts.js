// Chart steps:
// 1. data query
// 2. axes
// 3. sizes
var currentYear = 2015;
var width = 500;
var height = 20;
var defaultNullValue = "";


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

function rollByCategories(rows, keyfunc, rollup, categories){
  var data = d3.map();
  categories.forEach(function(k){
    data.set(k, rollup([]));
  });
  var existing = d3.nest()
    .key(keyFunc)
    .rollup(rollup)
    .map(data, d3.map);
  mergeMaps(data, existing);
  return data;
}

var dateTimeFormat = d3.time.format("%Y-%m-%d %H:%M:%S");
var dateTimeKey = "occuredDate";

function parseDate(dateTimeString){
  return dateTimeString ? dateTimeFormat.parse(dateTimeString) : null;
}

d3.csv(
  "/department/1/uof.csv ",
  function(error, rows){

    rows.forEach(function(r){
      var dateString = nullify(r[dateTimeKey]);

      r.date = parseDate(dateString);
    });

    uofByYear(rows);
});

function uofByYear(rows){
  var data = d3.nest()
    .key(function(d){ return d.date.getFullYear(); })
    .rollup(function(leaves){
      return { "count": leaves.length,
        "incidents": leaves,
        "year": leaves[0].date.getFullYear()
      };
    })
    .map(rows, d3.map);
  var year0 = d3.min(data.keys());
  var numYears = currentYear - year0;
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
  var count1 = d3.max(data.values(), function(d){ return d.count;});
  var container = d3.select(".chart.per.year.uof")
    .append("div")
    .attr("class", "hist wrapper");

  console.log("data", data);
  var bars = container.selectAll(".bar")
    .data(data.values()).enter()
    .append("div")
    .attr("class", function(d){ return "bar " + d.year; });

  bars.style("height", function(d){
    return d.count + "rem";
  }).style("margin-top", function(d){
      return height - d.count + "rem";
  }).text(function(d){
    return d.count;
  });

}
