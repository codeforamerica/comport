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

  // officer demographics
  'officer-demographics': {
    hideDate: true,
    chartType: 'symmetricalFlags',
    dataFunc: function(){ return DEMOGRAPHICS; }
    },

  //
  // USE OF FORCE
  //

  // unique use of force incidents per month
  'uof-by-month': {
    chartType: 'mountainHistogram',
    filter: uniqueForKeysInLast12Months('id', 'date'),
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

  // unique types of force used by officers
  // will be more types of force used than incidents
  'uof-force-type': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'officerIdentifier', 'officerForceType'),
    keyFunc: function(d){ return d.officerForceType; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].officerForceType; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique types of force used by incident only, when no officer identifier is availalbe
  // will be more types of force used than incidents
  // (SRPD only)
  'uof-incident-force-type': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'officerForceType'),
    keyFunc: function(d){ return d.officerForceType; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].officerForceType; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    otherLabel: 'Additional Types of Force',
    },

  // unique use of force incidents by district
  // (IMPD only)
  'uof-by-inc-district': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'district'),
    keyFunc: function(d){ return d.district; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].district; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique use of force incidents by assignment
  // (BPD only)
  'uof-by-assignment': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'assignment'),
    keyFunc: function(d){ return d.assignment; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].assignment; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique use of force incidents by team
  // (SRPD only)
  'uof-by-team': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'team'),
    keyFunc: function(d){ return d.team; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].team; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique use of force incidents by division
  // (LMPD only)
  'uof-by-division': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'division'),
    keyFunc: function(d){ return d.division; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].division; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // racial breakdown in use of force incidents
  'uof-race': {
    filter: last12Months,
    chartType: 'matrix',
    dataFunc: raceMatrix,
    xAxisTitle: "Resident",
    yAxisTitle: "Officer",
    },

  //
  // COMPLAINTS
  //

  // unique complaints per month
  'complaints-by-month': {
    chartType: 'mountainHistogram',
    filter: function(rows, config){
      return complaintsGroupedByID(last12Months(rows, config), config);
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

  // unique complaints by allegation
  'complaints-by-allegation': {
    filter: uniqueForKeysInLast12Months('id', 'allegation'),
    chartType: 'flagHistogram',
    keyFunc: function(d){ return d.allegation; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].allegation; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique complaints by allegation type
  'complaints-by-allegation-type': {
    filter: uniqueForKeysInLast12Months('id', 'allegationType'),
    chartType: 'flagHistogram',
    keyFunc: function(d){ return d.allegationType; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].allegationType; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique complaints by finding
  // (IMPD only)
  'complaints-by-finding': {
    filter: uniqueForKeysInLast12Months('id', 'finding'),
    chartType: 'flagHistogram',
    removeBlankX: true,
    keyFunc: function(d){ return d.finding; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].finding; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  // unique complaints by disposition
  // (BPD only)
  'complaints-by-disposition': {
    filter: uniqueForKeysInLast12Months('id', 'disposition'),
    chartType: 'flagHistogram',
    removeBlankX: true,
    keyFunc: function(d){ return d.disposition; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].disposition; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    },

  // unique complaints by district
  // (IMPD only)
  'complaints-by-precinct': {
    filter: uniqueForKeysInLast12Months('id', 'district'),
    chartType: 'flagHistogram',
    keyFunc: function(d){ return d.district; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].district; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique complaints by assignment
  // (BPD only)
  'complaints-by-assignment': {
    filter: uniqueForKeysInLast12Months('id', 'assignment'),
    chartType: 'flagHistogram',
    keyFunc: function(d){ return d.assignment; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].assignment; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique complaints by assignment
  // (SRPD only)
  'complaints-by-team': {
    filter: uniqueForKeysInLast12Months('id', 'team'),
    chartType: 'flagHistogram',
    keyFunc: function(d){ return d.team; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].team; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
  },

  // complaints by race of complainants and officers
  'complaints-by-demographic': {
    filter: last12Months,
    chartType: 'matrix',
    dataFunc: raceMatrix,
    xAxisTitle: "Resident",
    yAxisTitle: "Officer",
  },

  // unique complaints by officer
  'complaints-by-officer': {
    chartType: 'flagHistogram',
    x: "label",
    y: "count",
    dataFunc: officerComplaintsCount,
  },

  // unique complaints by officer, with a maximum
  'complaints-by-officer-with-cap': {
    chartType: 'flagHistogram',
    x: "label",
    y: "count",
    dataFunc: officerComplaintsCount,
    maxComplaints: 4,
  },

  //
  // OFFICER-INVOLVED SHOOTINGS
  //

  // unique officer-involved shootings by incident and district
  // (IMPD only)
  'ois-by-inc-district': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'district'),
    keyFunc: function(d){ return d.district; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].district; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: false,
    },

  // unique officer-involved shootings per month
  'ois-by-month': {
    chartType: 'mountainHistogram',
    filter: uniqueForKeysInLast12Months('id', 'date'),
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

  // unique officer-involved shootings by assignment
  // (BPD only)
  'ois-by-assignment': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'assignment'),
    keyFunc: function(d){ return d.assignment; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].assignment; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: false,
    },

  // unique officer-involved shootings by discharge type
  // (SRPD only)
  'ois-by-type': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'dischargeType'),
    keyFunc: function(d){ return d.dischargeType; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].dischargeType; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: false,
  },

  // unique officer-involved shootings by team
  // (SRPD only)
  'ois-by-team': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'team'),
    keyFunc: function(d){ return d.team; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].team; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: false,
  },

  // weapons used by officers in officer-involved shootings
  // there may be more than one weapon per incident
  'ois-weapon-type': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'officerIdentifier', 'officerWeaponUsed'),
    keyFunc: function(d){return d.officerWeaponUsed; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){  return b[0].officerWeaponUsed; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: false,
    },

  // officer-involved shootings by officer and resident race
  'ois-race': {
    filter: last12Months,
    chartType: 'matrix',
    dataFunc: raceMatrix,
    xAxisTitle: "Resident",
    yAxisTitle: "Officer",
    },

  //
  // PURSUITS
  //

  // unique use of force incidents per month
  'pursuits-by-month': {
    chartType: 'mountainHistogram',
    filter: uniqueForKeysInLast12Months('id', 'date'),
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

  // unique pursuit incidents by team
  'pursuits-by-team': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'team'),
    keyFunc: function(d){ return d.team; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].team; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique pursuit incidents by reason
  'pursuits-by-reason': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'reason'),
    keyFunc: function(d){ return d.reason; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].reason; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

  // unique pursuit incidents by distance
  'pursuits-by-distance': {
    chartType: 'flagHistogram',
    filter: uniqueForKeysInLast12Months('id', 'distance'),
    keyFunc: function(d){ return d.distance; },
    sortWith: function(d){ return -d.count; },
    x: 'type',
    xFunc: function(b){ return b[0].distance; },
    y: 'count',
    yFunc: function(b){ return b.length; },
    addOther: true,
    },

};

// Run the code that draws the charts
d3.csv(
  csv_url,
  function(error, rows){
    // figure out the best date key to use
    var dateCheckKeys = ["receivedDate", "occurredDate"];
    // default to the fallback
    var dateKey = dateCheckKeys[dateCheckKeys.length - 1];
    for (var i = 0; i < dateCheckKeys.length; i++) {
      if (dateCheckKeys[i] in rows[0]) {
        // we found a working key, stop checking
        dateKey = dateCheckKeys[i];
        break;
      }
    }
    // parse the raw csv data
    var parsed_rows = parseData(rows, dateKey);

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
