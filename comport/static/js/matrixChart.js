function insertBlankCell(cols){
  return function(sel){
    sel.insert('td', ':first-child')
      .attr("colspan", cols)
      .attr("class", "blank-cell");
  }
}

function orderedGet(keys, map){
  var results = [];
  keys.forEach(function(k){
    if( map.has(k) ){
      results.push(
        map.get(k)
        );
    }
  });
  return results;
}

percentFmt = d3.format(".1f");

function percentFormat(d){
  var num = percentFmt(d.percent * 100);
  return num + '<span class="percent">%</span>';
}


function sortedEntries(keys, map){
  var sorted = [];
  var entries = map.entries();
  keys.forEach(function(k){
    var filtered = entries.filter(function(e){
      return e.key === k;
    });
    if( filtered.length > 0 ){
      sorted.push(filtered[0]);
    }
  });
  return sorted;
}

function matrixChart(config, data){

  // set basic dimensions
  // we need a width, a height for each
  var height,
      width,
      font_size;

  font_size = 14; // px

  var races = [
    'Asian',
    'Black',
    'Hispanic',
    'White',
    'Other',
    'Unknown',
  ];

  // draw table
  var table = d3.select(config.parent)
    .append("table")
    .attr("class", "matrix-table table");

  console.log("data for matrix", data);
  var officerEntries = sortedEntries(races, data.officerRaceTotals);
  var officerRaceKeys = officerEntries.map(function(e){ return e.key; });
  var officerRaceTotals = officerEntries.map(function(e){ return e.value; });

  var rows = table.selectAll("tr").data(sortedEntries(races, data))
    .enter().append("tr")
    .attr("class", "matrix-row");

  var cells = rows.selectAll("td")
    .data(function(e){
      return orderedGet(races, e.value);
    }).enter().append("td")
    .attr("class", "matrix-cell")
    .attr("title", function(d){ return d.count; })
    .html(percentFormat);

  var residentTotals = rows.insert("th", ":first-child")
    .attr("class", "matrix-total")
    .attr("title", function(e){ return e.value.count; })
    .html(function (e){ 
      return percentFormat(e.value);
    });

  var residentLabels = rows.insert("th", ":first-child")
    .attr("class", "matrix-label")
    .text(function (e){ 
      return e.key;
    });

  var officerTotals = table.insert("tr", ":first-child");
  officerTotals.selectAll("th")
    .data(officerRaceTotals).enter().append("th")
    .attr("class", "matrix-total")
    .attr("title", function(d){ return d.count; })
    .html(percentFormat);

  var officerLabels = table.insert("tr", ":first-child");
  officerLabels.selectAll("th")
    .data(officerRaceKeys).enter().append("th")
    .attr("class", "matrix-label")
    .text(String);

  var yAxisLabel = table.insert("tr", ":first-child");

  yAxisLabel.append("th")
    .attr("class", "y-axis-title")
    .attr("colspan", officerRaceKeys.length)
    .text(config['yAxisTitle']);

  [officerLabels, yAxisLabel].map(insertBlankCell(2));
  officerTotals.insert("th", ":first-child")
    .attr("class", "x-axis-title")
    .attr("colspan", 2)
    .text(config['xAxisTitle']);


}
