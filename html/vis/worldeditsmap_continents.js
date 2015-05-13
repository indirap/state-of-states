// Script for World Map - Continents

var width = 800;
	height = 480;

// var colors = ["#ECF9D8", "#CFF09E", "#A8DBA8", "#79BD9A", "#6DAA8B", "#3B8686", "#0B486B", "#093A56"];

var colors = ["#ECF9D8", "#A8DBA8", "#79BD9A", "#6DAA8B", "#3B8686", "#093A56"];

// The intervals were determined so that the countries would be divided evenly into 8
// intervals, so that it would be aesthetically pleasing (i.e. colors spread evenly). 

// var intervals = [0.00018011, 0.0003363, 0.0005137, 0.0008364, 0.001467, 0.003209, 0.012256]; // Edits per population
// var intervals = [255009, 969725, 2057170, 4445249, 8395512, 19092981, 56532728]; // GDP per edits
// var intervals = [3000, 4000, 5021, 6569, 8541, 11571, 14454]; // Edits

var cintervals = [5000, 6000, 7000, 10000, 11000];

var continentcolor = d3.scale.threshold()
	.domain(cintervals)
	.range(colors);

var projection = d3.geo.kavrayskiy7()
		.scale(150)
		.translate([width / 2, height / 2])
		.precision(.1);

var path = d3.geo.path()
		.projection(projection);

var graticule = d3.geo.graticule();

var csvg = d3.select("#c-map").append("svg")
		.attr("width", width)
		.attr("height", height);

csvg.append("defs").append("path")
		.datum({type: "mercator"})
		.attr("id", "sphere")
		.attr("d", path);

csvg.append("use")
		.attr("class", "stroke")
		.attr("xlink:href", "#sphere");

csvg.append("use")
		.attr("class", "fill")
		.attr("xlink:href", "#sphere");

var clegend = d3.select("#c-legend").append("svg")
	.data(colors)
	.attr("width", width)
	.attr("height", 70);

// Load data before proceeding.
queue()
	.defer(d3.json, "html/vis/world-50m.json")
	.defer(d3.tsv, "html/vis/continent_data.tsv")
	.await(ready);

function ready(error, world, countrycodes) {
	var rateById = {};
	var getContinent = {};
	var getName = {};

	countrycodes.forEach(function(d) {
		rateById[d.id] = d.average_edits;
		getContinent[d.id] = d.continent;
		getName[d.id] = d.country;
	});

	var countries = topojson.feature(world, world.objects.countries).features,
		neighbors = topojson.neighbors(world.objects.countries.geometries);

	csvg.selectAll(".country")
			.data(countries)
		.enter().insert("path", ".graticule")
			.attr("class", function(d) {
				return "country " + getContinent[d.id];
			})
			.attr("d", path)
			.style("fill", function(d) {
				// Display based on the interval
				return continentcolor(rateById[d.id]);
			})
			.on('mouseover', function(d) {
				// When moused over, change the color of the country to gray.
				// d3.select(this).style("fill", "#bcbcbc");
				d3.selectAll("." + getContinent[d.id]).style("fill", "#bcbcbc");

				// Get this bar's x/y values, then augment for the tooltip
				var xPosition = d3.event.pageX;
				var yPosition = d3.event.pageY;

				// Update the tooltip position and value
				d3.select("#tooltip")
				  .style("left", (xPosition - 60) + "px")
				  .style("top", (yPosition - 30) + "px")
				  .select("#value")
				  .text(function() {
					if (getName[d.id] == "") {
						return "N/A";
					}
					if (rateById[d.id] == "") {
						// There are countries on the map which we do not have data for.
						// In that case, say that data is not available.
						return getContinent[d.id] + " - data N/A";
					}
					return getContinent[d.id] + " - " + rateById[d.id] + " edits";
				  });

				d3.select("#tooltip").classed("hidden", false);
				})
			.on('mouseout', function(d) {
				// On mouse out, return color back to normal and remove tooltip.
				// d3.select(this).style("fill", function(d) {
				// 	return color(rateById[d.id]);
				// });

				d3.selectAll("." + getContinent[d.id]).style("fill", function(d) {
					return continentcolor(rateById[d.id]);
				});

				d3.select("#tooltip").classed("hidden", true);
			});

	csvg.insert("path", ".graticule")
		.datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
		.attr("class", "boundary")
		.attr("d", path);

	// Code for the legend. 
	clegend.append("rect")
		.attr("x", 0)
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#ECF9D8");

	clegend.append("rect")
		.attr("x", (800/7))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#CFF09E");

	clegend.append("rect")
		.attr("x", (800/7*2))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#A8DBA8");

	clegend.append("rect")
		.attr("x", (800/7*3))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#79BD9A");

	clegend.append("rect")
		.attr("x", (800/7*4))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#3B8686");

	clegend.append("rect")
		.attr("x", (800/7*5))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#0B486B");

	clegend.append("rect")
		.attr("x", (800/7*6))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#093A56");

	clegend.append("text")
		.text("≥ 3000 edits")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", 10)
		.attr("y", 40);

	clegend.append("text")
		.text("≥ 4000 edits")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7) + 10)
		.attr("y", 40);

	clegend.append("text")
		.text("≥ 5021 edits")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*2) + 10)
		.attr("y", 40);

	clegend.append("text")
		.text("≥ 6569 edits")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*3) + 10)
		.attr("y", 40);

	clegend.append("text")
		.text("≥ 8541 edits")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*4) + 10)
		.attr("y", 40);

	clegend.append("text")
		.text("≥ 11571 edits")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*5) + 10)
		.attr("y", 40);

	clegend.append("text")
		.text("≥ 14454 edits")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*6) + 10)
		.attr("y", 40);	
}