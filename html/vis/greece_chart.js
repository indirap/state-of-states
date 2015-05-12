var chart = c3.generate({
	bindto: '.greece',
	color: {
	  pattern: ['#CFF09E', '#3B8686']
	},
	data: {
		x: 'x',
	  columns: [
		['x', 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013],
		['File Size', 44478, 38068, 39665, 41367, 44124, 49240, 56255, 62617, 68816, 74452, 80173, 85495, 89335],
		['GDP', 212611721758, 219335821022, 233894807367, 245478738870, 247665771278, 262068232726, 271338832139, 270133049794, 258260896384, 244189836218, 222545123738, 207919209322, 201025631249]
	  ],
	  axes: {
		GDP: 'y2' // ADD
	  }
	},
	axis: {
	  y: {
		label: { // ADD
		  text: 'Average File Size',
		  position: 'outer-middle'
		}
	  },
	  y2: {
		show: true,
		label: { // ADD
		  text: 'GDP (2005 US$)',
		  position: 'outer-middle'
		},
		tick: {
		  format: d3.format("$,") // ADD
		}
	  }
	}
	});