// Script for World Map

var width = 800;
	height = 480;

var colors = ["#ECF9D8", "#CFF09E", "#A8DBA8", "#79BD9A", "#6DAA8B", "#3B8686", "#0B486B", "#093A56"];

// The intervals were determined so that the countries would be divided evenly into 8
// intervals, so that it would be aesthetically pleasing (i.e. colors spread evenly). 

var gdpintervals = [1624294250, 8307222087, 14791699008, 30956691627, 57868674297, 208796024645, 438283564814]; // GDP

var gdpcolor = d3.scale.threshold()
	.domain(gdpintervals)
	.range(colors);

var projection = d3.geo.kavrayskiy7()
		.scale(150)
		.translate([width / 2, height / 2])
		.precision(.1);

var path = d3.geo.path()
		.projection(projection);

var graticule = d3.geo.graticule();

var gdpsvg = d3.select("#gdp-map").append("svg")
		.attr("width", width)
		.attr("height", height);

gdpsvg.append("defs").append("path")
		.datum({type: "mercator"})
		.attr("id", "sphere")
		.attr("d", path);

gdpsvg.append("use")
		.attr("class", "stroke")
		.attr("xlink:href", "#sphere");

gdpsvg.append("use")
		.attr("class", "fill")
		.attr("xlink:href", "#sphere");

var gdplegend = d3.select("#gdp-legend").append("svg")
	.data(colors)
	.attr("width", width)
	.attr("height", 70);

// Load data before proceeding.
queue()
	.defer(d3.json, "html/vis/world-50m.json")
	.defer(d3.tsv, "html/vis/new_data.tsv")
	.await(ready);

function ready(error, world, countrycodes) {
	var rateById = {};
	var getName = {};

	countrycodes.forEach(function(d) {
		rateById[d.id] = d.gdp;
		getName[d.id] = d.country;
	});

	var countries = topojson.feature(world, world.objects.countries).features,
		neighbors = topojson.neighbors(world.objects.countries.geometries);

	gdpsvg.selectAll(".country")
			.data(countries)
		.enter().insert("path", ".graticule")
			.attr("class", "country")
			.attr("d", path)
			.style("fill", function(d) {
				// Display based on the interval
				return gdpcolor(rateById[d.id]);
			})
			.on('mouseover', function(d, i) {
				// When moused over, change the color of the country to gray.
				d3.select(this).style("fill", "#bcbcbc");

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
						return getName[d.id] + " - data N/A";
					}
					return getName[d.id] + " - " + rateById[d.id] + " US$";
				  });

				d3.select("#tooltip").classed("hidden", false);
				})
			.on('mouseout', function(d) {
				// On mouse out, return color back to normal and remove tooltip.
				d3.select(this).style("fill", function(d) {
					return gdpcolor(rateById[d.id]);
				});

				d3.select("#tooltip").classed("hidden", true);
			});

	gdpsvg.insert("path", ".graticule")
		.datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
		.attr("class", "boundary")
		.attr("d", path);

	// Code for the legend. 
	gdplegend.append("rect")
		.attr("x", 0)
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#ECF9D8");

	gdplegend.append("rect")
		.attr("x", (800/7))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#CFF09E");

	gdplegend.append("rect")
		.attr("x", (800/7*2))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#A8DBA8");

	gdplegend.append("rect")
		.attr("x", (800/7*3))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#79BD9A");

	gdplegend.append("rect")
		.attr("x", (800/7*4))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#3B8686");

	gdplegend.append("rect")
		.attr("x", (800/7*5))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#0B486B");

	gdplegend.append("rect")
		.attr("x", (800/7*6))
		.attr("y", 10)
		.attr("width", (800/7))
		.attr("height", 20)
		.style("fill", "#093A56");

	var gdpintervals = [1624294250, 8307222087, 14791699008, 30956691627, 57868674297, 208796024645, 438283564814];

	gdplegend.append("text")
		.text("≥ 1624294250 US$")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", 10)
		.attr("y", 40);

	gdplegend.append("text")
		.text("≥ 8307222087 US$")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7) + 10)
		.attr("y", 40);

	gdplegend.append("text")
		.text("≥ 14791699008 US$")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*2) + 10)
		.attr("y", 40);

	gdplegend.append("text")
		.text("≥ 30956691627 US$")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*3) + 10)
		.attr("y", 40);

	gdplegend.append("text")
		.text("≥ 57868674297 US$")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*4) + 10)
		.attr("y", 40);

	gdplegend.append("text")
		.text("≥ 208796024645 US$")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*5) + 10)
		.attr("y", 40);

	gdplegend.append("text")
		.text("≥ 438283564814 US$")
		.attr("font-family", "@font-family-base")
		.attr("font-size", "9px")
		.attr("x", (800/7*6) + 10)
		.attr("y", 40);	
}