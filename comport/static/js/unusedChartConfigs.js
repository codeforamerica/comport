
// These are chart configs that were developed at one time but aren't currently in use on the live site.
// See chartConfigs.js for charts that are currently in use.

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
      return complaintsGroupedByID(rows, config);
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

