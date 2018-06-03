var allRows;


function notEqual(a, b){
  if( a instanceof Date && b instanceof Date ){
    return a.getTime() != b.getTime();
  } else {
    return a != b;
  }
}

function unique(a, b){
  if( a instanceof Array ){
    var s = d3.set(a);
    s.add(b);
    return s.values();
  } else {
    return d3.set([a, b]).values();
  }
}

function complaintReducer(complaintA, complaintB){
  // takes two complaint rows and combines them
  // where there are colliding values, creates an array and stores both
  var reducedComplaint = {};
  for (var key in complaintA){
    if( complaintA.hasOwnProperty(key) ){
      var complaintAVal = complaintA[key];
      var complaintBVal = complaintB[key];
      if( notEqual(complaintAVal, complaintBVal) ){
          reducedComplaint[key] = unique(complaintAVal, complaintBVal);
      } else {
        reducedComplaint[key] = complaintA[key];
      }
    }
  }
  return reducedComplaint;
}

function complaintsGroupedByID(rows){
  // group complaints by id
  // each complaint has a unique ID, but there may be multiple rows of data for a single complaint
  // this function reduces one complaint's rows to a single object that has arrays for fields with colliding values
  var complaintGrouper = d3.nest()
    .key(function (d){ return d.id; })
    .rollup(function(allegations){
      var complaint = allegations.reduce(complaintReducer);
      complaint['allegations'] = allegations;
      return complaint;
    });
  // return a list of just the values
  return complaintGrouper.map(rows, d3.map).values();
}

function raceKey( value ) {
  if( !value ){
    value = "";
  }
  return {
    "": "Unknown",
    "African Amer": "Black",
    "Am. Indian": "Other",
    "Amer-Indian": "Other",
    "Amind": "Other",
    "Asian": "Asian",
    "B": "Black",
    "Bi-racial": "Other",
    "Bi-Racial": "Other",
    "Black": "Black",
    "black": "Black",
    "East-Indian": "Asian",
    "Hispa": "Hispanic",
    "Hispanic": "Hispanic",
    "Korean": "Asian",
    "Mid. Eastern": "Other",
    "Mixed": "Other",
    "Other Asian": "Asian",
    "Other Hispan": "Hispanic",
    "Other": "Other",
    "Polynesian": "Asian",
    "Puerto Rican": "Hispanic",
    "Unknown": "Unknown",
    "W": "White",
    "White ": "White",
    "White": "White",
  }[value];
}

function race(k){
  return function(d){
    return raceKey(d[k]);
  };
}

function uniqueResidentProxy(d){
   return [ d.residentAge, "year old", d.residentRace, d.residentSex ].join(" ");
}

function uniqueComplaintAboutOfficerByResidentProxy(d){
   return [
     d.residentAge,
     "year old",
     d.residentRace,
     d.residentSex,
     "filed",
     d.id,
     "about",
     d.officerIdentifier
       ].join(" ");
}

function raceMatrix(config, data){

  var complaints = d3.nest()
    .key(uniqueComplaintAboutOfficerByResidentProxy)
    .rollup(function (group){
      var obj = {};
      [ 'residentAge', 'residentSex', 'officerAge',
        'officerSex', 'officerYearsOfService',
        ].map(function(k){
          obj[k] = group[0][k];
        });
      [ 'residentRace', 'officerRace',
        ].map(function(k){
          obj[k] = raceKey(group[0][k]);
        });
      obj.allegations = group;
      return obj;
    }).entries(data);

  var totalComplaintCount = complaints.length;
  var counts = d3.nest()
    .key(function(d){
      return d.values.residentRace;
    }).key(function(d){
      return d.values.officerRace;
    }).rollup(function(group){
      return {
        count: group.length,
        percent: ( group.length / totalComplaintCount ),
        complaints: group,
      };
    }).map(complaints, d3.map);

  var officerRaceTotals = d3.nest()
    .key(function(d){ return d.values.officerRace; })
    .rollup(function(group){
      return {
        count: group.length,
        percent: ( group.length / totalComplaintCount ),
      };
    }).map(complaints, d3.map);

  // unique keys for officer axis
  var allOfficerRaceKeys = officerRaceTotals.keys();

  // get resident race totals
  counts.keys().forEach(function(resRace){
      var total = 0;
      var subgroups = counts.get(resRace);
      subgroups.values().map(function(offRace){ total += offRace.count; });

      // add missing races, but only the unique keys of the corresponding axis
      allOfficerRaceKeys.forEach(function(officerRace){
        if( !subgroups.get(officerRace) ){
          subgroups.set(officerRace, {});
        }
      });
      subgroups.count = total;
      subgroups.percent = ( total / totalComplaintCount );
    });

  counts.officerRaceTotals = officerRaceTotals;
  return counts;
}

function uniqueOfficerComplaints(rows){
  var newSet = [];
  var grouper = d3.nest()
    .key(function (d){ return d.officerIdentifier; })
    .key(function (d){ return d.id; });
  var officerComplaintMap = grouper.map(rows, d3.map);
  officerComplaintMap.forEach(function(offId, complaints){
    newSet.push({
      officerIdentifier: offId,
      complaintCount: complaints.keys().length,
      values: complaints
    });
  });
  return newSet;
}

function officerComplaintsCount(config, data){
  data = uniqueOfficerComplaints(data);
  var hasMaxComplaints = config.hasOwnProperty('maxComplaints');
  var counts = d3.nest()
    .key( function (d){
      if (hasMaxComplaints){
        return Math.min(d.complaintCount, config.maxComplaints);
      } else {
        return d.complaintCount;
      }
    }).rollup( function (values){
      return values.length;
    }).entries(data);
  return counts.map(function(e){
    var obj = {};
    var n = e.key;
    if (n == config.maxComplaints){
      obj['label'] = "Officers with " + n + " or more complaints";
    } else {
      obj['label'] = "Officers with " + ( n > 1 ? n+" complaints" : n+" complaint" );
    }
    obj['count'] = n;
    obj[config.y] = e.values;
    return obj;
  });
}

var experienceBuckets = d3.scale.quantize()
  .domain([2.5, 5.5, 10.5])
  .range([
      '0-2 years',
      '3-5 years',
      '6-10 years',
      '10+ years',
      ]);

var currentYear = 2015;
var defaultNullValue = "NULL";

function translate(x, y){
  return "translate(" + x + "," + y + ")";
}

function mergeMaps(a, b){
  b.forEach(function(k, v){
    a.set(k, v);
  });
}

function nullify(value){
  if (value === defaultNullValue){
    return null;
  } else {
    return value;
  }
}

function addMissingYears(dataMap){
  // add missing years to the map, so we know they are empty
  var year0 = d3.min(dataMap.keys());
  var allYears = d3.range(year0, currentYear);
  allYears.forEach(function(yr){
    if( !dataMap.has(yr) ){
      dataMap.set(
        yr, {
          year: yr,
          count: 0,
          incidents: [],
      });
    }
  });
}

function addOtherCategory(data, label){
  // add an 'other' category to the prestructured data
  // to consolidate groups of small counts
  var threshold = 0.006;
  var small_list = [];
  // get total sum of all counts
  var total = data.map(function (g){
    return g.count;
  }).reduce(function (a,b) {
    return a + b;
  });
  var otherTotal = 0;

  data.forEach(function(d, i) {
    if(d.count / total < threshold){
      small_list.push(i);
      otherTotal = otherTotal + d.count;
    }
  });

  // don't continue if there isn't anything in the 'Other' category
  if (otherTotal <= 0) {
    return;
  }

  data.push({
    type: label,
    count: otherTotal,
    groups: small_list.map(function(i){
      return data[i];
    })
  });

  var removed_count = 0;
  small_list.forEach(function(i){
    i -= removed_count;
    data.splice(i, 1);
    removed_count += 1;
  });
}

var dateTimeFormat = d3.time.format("%Y-%m-%d %H:%M:%S");
var niceMonthYearFormat = d3.time.format('<span class="month">%b</span>&nbsp;<span class="year">%Y</span>');
function parseDate(dateTimeString){
  return dateTimeString ? dateTimeFormat.parse(dateTimeString) : null;
}

function parseData(rows, dateKey){
  // parses dates and nulls from the raw csv
  rows.forEach(function(r){
    var dateString = nullify(r[dateKey]);
    r.date = parseDate(dateString);
  });
  rows = rows.filter(function(d){
    return d.date;
  });
  return rows;
}

function lastNMonths(rows, config, num){
  // offset today by the passed number of d3-defined months in the past
  offset = -1 * (num || 12);
  var latestDate = d3.max(rows, function(d){ return d.date; });
  var startDate = d3.time.month.offset(latestDate, offset);
  // start from the 1st of the month
  startDate = d3.time.day.offset(startDate, -1 * (startDate.getDate() - 1));
  config.dateSpan = [startDate, latestDate];
  return rows.filter(function(r){
    return startDate < r.date;
  });
}

function last12Months(rows, config){
  return lastNMonths(rows, config, 12);
}

function last24Months(rows, config){
  return lastNMonths(rows, config, 24);
}

function last48Months(rows, config){
  return lastNMonths(rows, config, 48);
}

function uniqueForKeys(){
  // takes a list of key strings to filter a set of raw incidents
  // concatenates the values of the given keys to provide a unique key
  // for example:
  //    uniqueForKeys('id', 'shift', 'beat')
  // returns an array of objects representing each unique
  // combination of the values of those columns
   //   returns [
   //     {id:1, shift: 'a', beat: 'b'},
   //     {id:1, shift: 'c', beat: 'b'},
   //     {id:2, shift: 'a', beat: 'b'},
   // ]
  function concatValues(values){
    var separator = '-';
    var result = '';
    values.forEach(function(val){
      result += (separator + val);
    });
    return result;
  }
  var keys = Array.prototype.slice.call(arguments);
  var grouper = d3.nest()
    .key(function (d){
      var values = keys.map(function(k){ return d[k]; });
      return concatValues(values);
    }).rollup(function(leaves){
      // each 'leaf' has the same values for the keys
      var datum = {};
      keys.forEach(function(k){
        datum[k] = leaves[0][k];
      });
      return datum;
    });
    return function(unfilteredRows){
      return grouper.map(unfilteredRows, d3.map)
        .values();
    };
}

function uniqueForKeysInLast12Months(){
  // takes a list of key strings to filter a set of raw incidents
  // concatenates the values of the given keys to provide a unique key
  // but first prefilters down to the last 12 months
  // for example:
  //    uniqueForKeys('id', 'shift', 'beat')
  var args = Array.prototype.slice.call(arguments);
  var uniqueFilter = uniqueForKeys.apply(uniqueForKeys, args);
  return function(rows, config){
    var prefiltered = last12Months(rows, config);
    return uniqueFilter(prefiltered);
  };
}

function uniqueForKeysInLast24Months(){
  // takes a list of key strings to filter a set of raw incidents
  // concatenates the values of the given keys to provide a unique key
  // but first prefilters down to the last 24 months
  // for example:
  //    uniqueForKeys('id', 'shift', 'beat')
  var args = Array.prototype.slice.call(arguments);
  var uniqueFilter = uniqueForKeys.apply(uniqueForKeys, args);
  return function(rows, config){
    var prefiltered = last24Months(rows, config);
    return uniqueFilter(prefiltered);
  };
}

function uniqueForKeysInLast48Months(){
  // takes a list of key strings to filter a set of raw incidents
  // concatenates the values of the given keys to provide a unique key
  // but first prefilters down to the last 24 months
  // for example:
  //    uniqueForKeys('id', 'shift', 'beat')
  var args = Array.prototype.slice.call(arguments);
  var uniqueFilter = uniqueForKeys.apply(uniqueForKeys, args);
  return function(rows, config){
    var prefiltered = last48Months(rows, config);
    return uniqueFilter(prefiltered);
  };
}


function structureData(parsed_rows, config){
  // restructures csv data into data than can be used to draw a chart

  // create a grouping machine that groups by key function
  var data_grouper = d3.nest()
    .key(config.keyFunc)
    .rollup(function(leaves){
      var datum = {};
      datum[config.y] = config.yFunc(leaves);
      datum[config.x] = config.xFunc(leaves);
      datum['incidents'] = leaves;
      return datum;
    });

  // use the parsed data and the grouping machine to create a
  // simple key value store (aka "map") with years as keys
  var data = data_grouper.map(parsed_rows, d3.map);

  if( config.dataMapAdjust ){
    config.dataMapAdjust(data);
  }

  if( config.dontFlatten ){
    return data;
  }

  if( config.removeBlankX ){
    data.remove("");
  }

  // return data structured for a chart
  var structured_data = data.values();
  if( config.sortWith ){
    var mapped = structured_data.map(function(d, i){
      return { index: i, value: config.sortWith(d) };
    });
    mapped.sort(function(a,b){
      return +(a.value > b.value) || +(a.value === b.value) - 1;
    });
    structured_data = mapped.map(function(n){
      return structured_data[n.index];
    });
  }
  if( config.addOther ){
    otherLabel = 'Other';
    if ( config.otherLabel ) {
      otherLabel = config.otherLabel;
    }
    addOtherCategory(structured_data, otherLabel);
  }
  return structured_data;
}

function drawChart(rows, config){

  // filter rows if necessary
  if( config.filter ){
    rows = config.filter(rows, config);
  }

  // structure data for the particular chart
  var data;
  if( config.dataFunc ){
    data = config.dataFunc(config, rows);
  } else {
    data = structureData(rows, config);
  }
  if( !config.dateSpan ){
    config.dateSpan = allRows.dateSpan;
  }

  if( !config.hideDate ){
    // add the date interval for this chart's data
    $(config.brick).find('.brick-titleblock > h4').append(
      ' <span class="brick-datespan">' +
        '<span class="brick-datespan-start">' +
          niceMonthYearFormat(config.dateSpan[0]) +
        '</span>&nbsp;' +
        '<span class="brick-datespan-separator">' +
          '—' +
        '</span>&nbsp;' +
        '<span class="brick-datespan-end">' +
          niceMonthYearFormat(config.dateSpan[1]) +
        '</span>' +
      '</span>');
  }
  // get the correct function for drawing this chart
  drawingFunction = drawFuncs[config.chartType];

  // if we have no chart block in the database, just make the brick
  if(config.noTemplate){
    var brick = d3.select('[role=main]')
      .append('div').attr("class", "brick");
    brick.append("h4").attr("class", "brick-title")
      .text(config.title);
    config.parent = brick.append("div").attr("class", config.parent)[0][0];
  }

  // run the function to draw the chart
  drawingFunction(config, data);
}

drawFuncs = {
  'lineChart': lineChart,
  'percent': basicPercent,
  'flagHistogram': flagHistogram,
  'mountainHistogram': mountainHistogram,
  'symmetricalFlags': symmetricalFlags,
  'matrix': matrixChart,
};
