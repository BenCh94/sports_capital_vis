var data = JSON.parse(grant_data);

var ndx = crossfilter(data);

var locationDim = ndx.dimension(function(d) {return d.County});
var fundingDim = ndx.dimension(function(d) {return d.allocated_value});
var orgDim = ndx.dimension(function(d) {return d['Organisation Type']});
var SportDim = ndx.dimension(function(d) {return d['Sport Type']});

var total_allocated = fundingDim.group().reduceSum(dc.pluck('gain_los'));
var county = dateDim.group().reduceSum(dc.pluck('sp_gain_loss'));
var sport = shareDim.group().reduceSum(dc.pluck('invested'));
var daysIn = shareDim.groupAll();