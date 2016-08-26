var configs = {

  // filter with
    // filters: [
    // ]
  // per branch (if nested) or total:
    // variables: {
    //  key: varFunc,
    //  key: varFunc
    // }
  // nest with
    // nest by [keyFunc1, keyFunc2]
    // postNest: mapFunc
    // don't flatten: false/true
  // if flattened or unnested
    // sortBy: [
    //  -key,
    //  key,
    //  sortFunc,
    // ]

  'uof-by-year': {
    chartType: 'lineChart',
    keyFunc: function(d){ return d.date.getFullYear(); },
    dataMapAdjust: addMissingYears,
    x: 'year',
    xFunc: function(b){ return b[0].date.getFullYear(); },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'uof-type-of-call': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return d.serviceType; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].serviceType; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'uof-reason': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return d.useOfForceReason; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].useOfForceReason; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'uof-citizen-weapon': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return d.residentWeaponUsed; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].residentWeaponUsed; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'uof-map': {
    chartType: 'map',
    filter: function(b, config){
      return last12Months(b, config).filter(function(d){
       if( d.censusTract ){ return true; } else { return false; }
      });
    },
    dontFlatten: true,
    keyFunc: function(d){ return d.censusTract; },
    x: 'censusTract',
    xFunc: function(b){ return b[0].censusTract; },
    y: 'count',
    yFunc: function(b){ return b.length; }
    },

  'uof-by-shift': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return d.shift; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].shift; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'uof-by-inc-district': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return d.district; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].district; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  'uof-by-assignment': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return d.assignment; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].assignment; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  'uof-force-type': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return d.officerForceType; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].officerForceType; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  'uof-officer-injuries': {
    chartType: 'percent',
    filter: last12Months,
    keyFunc: function(d){ return d.officerInjured; },
    x: "injured",
    xFunc: function (b) { return b.length; },
    y: "hospitalized",
    yFunc: function (b){
      var hospitalizations = b.filter(function(d){
        return d.officerHospitalized == "true";
      });
      return hospitalizations.length;
    },
    dataMapAdjust: function (dataMap){
      dataMap.remove("");
      dataMap.remove("false");
      dataMap.get("true").total = last12Months(allRows).length;
    },
    },

  'uof-resident-injuries': {
    chartType: 'percent',
    filter: last12Months,
    keyFunc: function(d){ return d.residentInjured; },
    x: "injured",
    xFunc: function (b) { return b.length; },
    y: "hospitalized",
    yFunc: function (b){
      var hospitalizations = b.filter(function(d){
        return d.residentHospitalized == "true";
      });
      return hospitalizations.length;
    },
    dataMapAdjust: function (dataMap){
      dataMap.remove("");
      dataMap.remove("false");
      dataMap.get("true").total = last12Months(allRows).length;
    },
    },

  'uof-dispositions': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return d.finding; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].finding; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'uof-dispositions-outcomes': {
    },

  'officer-demographics': {
    hideDate: true,
    chartType: 'symmetricalFlags',
    dataFunc: function(){ return DEMOGRAPHICS; }
    },

  'uof-race': {
    filter: last12Months,
    chartType: 'matrix',
    dataFunc: raceMatrix,
    xAxisTitle: "Resident",
    yAxisTitle: "Officer",
    },

  'uof-per-officer': {
    chartType: 'flagHistogram',
    },

  'uof-officer-experience': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return experienceBuckets(d.officerYearsOfService); },
    sortWith: function(d){ return parseInt(d.years); },
    x: 'years',
    xFunc: function(b){ return experienceBuckets(b[0].officerYearsOfService); },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'complaints-by-year': {
    chartType: 'lineChart',
    filter: function(rows, config){
      return allegationsToComplaints(rows, config);
    },
    keyFunc: function(d){ return d.date.getFullYear(); },
    dataMapAdjust: addMissingYears,
    x: 'year',
    xFunc: function(b){ return b[0].date.getFullYear(); },
    y: 'count',
    yFunc: function(b){ return b.length; },
    postDraw: function(){
      // add note to final year
    }
    },

  'complaints-by-month': {
    chartType: 'mountainHistogram',
    filter: function(rows, config){
      return allegationsToComplaints(last12Months(rows, config), config);
    },
    keyFunc: function(d){ return d3.time.format('%Y %m')(d.date); },
    sortWith: function(d){ return d.month; },
    x: 'month',
    xFunc: function(b){ return d3.time.month.floor(b[0].date); },
    xTickFormat: function(d){
      var fmt = d3.time.format('%b %Y');
      return fmt(new Date(d));
    },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'complaints-by-allegation': {
    filter: last12Months,
    chartType: 'flagHistogram',
    keyFunc: function(d){ return d.allegation; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].allegation; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  'complaints-by-allegation-type': {
    filter: last12Months,
    chartType: 'flagHistogram',
    keyFunc: function(d){ return d.allegationType; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].allegationType; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  'complaints-by-precinct': {
    filter: last12Months,
    chartType: 'flagHistogram',
    keyFunc: function(d){ return d.district; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].district; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  'complaints-by-assignment': {
    filter: last12Months,
    chartType: 'flagHistogram',
    keyFunc: function(d){ return d.assignment; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].assignment; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  'complaints-by-finding': {
    filter: last12Months,
    chartType: 'flagHistogram',
    removeBlankX: true,
    keyFunc: function(d){ return d.finding; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].finding; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'complaints-by-disposition': {
    filter: last12Months,
    chartType: 'flagHistogram',
    removeBlankX: true,
    keyFunc: function(d){ return d.disposition; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].disposition; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  'complaints-by-demographic': {
    filter: last12Months,
    chartType: 'matrix',
    dataFunc: raceMatrix,
    xAxisTitle: "Resident",
    yAxisTitle: "Officer",
  },

  'complaints-by-officer': {
    chartType: 'flagHistogram',
    x: "label",
    y: "count",
    dataFunc: officerComplaintsCount,
  },

  'ois-by-inc-district': {
    chartType: 'flagHistogram',
    // TODO: temporary for testing
    // filter: last12Months,
    filter: uniqueForKeysInLast12Months('id', 'district'),
    keyFunc: function(d){ return d.district; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].district; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: false,
    },

  'ois-by-assignment': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){ return d.assignment; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].assignment; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: false,
    },

  'ois-weapon-type': {
    chartType: 'flagHistogram',
    filter: last12Months,
    keyFunc: function(d){return d.officerWeaponUsed; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){  return b[0].officerWeaponUsed; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: false,
    },

  'ois-race': {
    filter: last12Months,
    chartType: 'matrix',
    dataFunc: raceMatrix,
    xAxisTitle: "Resident",
    yAxisTitle: "Officer",
    },

};

// Running the all the code that draws the charts
d3.csv(
  csv_url,
  function(error, rows){
    // parse the raw csv data
    var parsed_rows = parseData(rows);

    allRows = rows;
    allRows.dateSpan = d3.extent(rows, function(d){ return d.date; });

    // deal with each chart configuration
    charts.forEach(function(name){

      // get configuration
      var config = configs[name];

      if( config.chartType ){
        // get class name for parent div
        config.parent = '.' + name;
        config.brick = '#' + name;
        drawChart(parsed_rows, config);
      }

    });
    markLoadTimeWithGoogleAnalytics();
  }
);

function markLoadTimeWithGoogleAnalytics(){
  if (window.performance) {
    // Gets the number of milliseconds since page load
    // (and rounds the result since the value must be an integer).
    var timeSincePageLoad = Math.round(performance.now());

    // Sends the timing hit to Google Analytics.
    ga('send', 'timing', 'Charts', 'drawn', timeSincePageLoad);
  }
}
