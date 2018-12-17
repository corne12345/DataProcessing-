// Corné Heijnen
// 12230170
// DataProcessing (Linked Views: World happiness)
// This script is based on http://bl.ocks.org/micahstubbs/8e15870eb432a21f0bc4d3d527b2d14f

var format = d3.format(",");

// Set tooltips
var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
              return "<strong>Country: </strong><span class='details'>" + d.properties.name + "<br></span>" + "<strong>Happiness: </strong><span class='details'>" + format(d.happiness.Happiness) +"<br></span>" + "<strong>Position worldwide: </strong><span class='details'>" + format(d.happiness.Position) +"</span>";
            })

var margin = {top: 0, right: 0, bottom: 0, left: 0},
            width = 960 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

var thresholdScale = d3.scaleQuantize ()
    .domain([ 0, 11 ])
    .range(["#FF0000", "#FF1100", "#FF2200", "#FF3300", "#FF5500", "#FFBE00","#FFFF00","#D7FF00","#9BFF00","#78FF00","#00FF00", "#000000"])

var path = d3.geoPath();

var svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append('g')
            .attr('class', 'map');

            var colorLegend = d3.legendColor()
              .labelFormat(d3.format(".0f"))
              .scale(thresholdScale)
              .shapePadding(5)
              .shapeWidth(50)
              .shapeHeight(20)
              .labelOffset(12);

            svg.append("g")
              .attr("transform", "translate(20, 225)")
              .call(colorLegend);


var projection = d3.geoMercator()
                   .scale(130)
                  .translate( [width / 2, height / 1.5]);

var path = d3.geoPath().projection(projection);

svg.call(tip);

queue()
    .defer(d3.json, "world_countries.json")
    .defer(d3.json, "data.json")
    .await(ready);

function ready(error, data, happiness) {
  data.features.forEach(function(d) { d.id = d.properties.name});

  // Own interprestation of above mentioned code
  var happinessByName = {};
  var parameters = {};
  happiness.forEach(function(d) {parameters = {"Position": d.Happiness_Rank, "Happiness": d.Happiness_Score, "Details" :{"Economy": d.Economy, "Family": d.Family, "Health": d.Health, "Freedom": d.Freedom, "Trust": d.Trust, "Generosity": d.Generosity, "Residual": d.Dystopia_Residual}}; happinessByName[d.Country] = parameters});
  data.features.forEach(function(d) { d.happiness = happinessByName[d.id]})


  svg.append("g")
      .attr("class", "countries")
    .selectAll("path")
      .data(data.features)
    .enter().append("path")
      .attr("d", path)
      .style("fill", function(d){try{var temp = happinessByName[d.id]; return thresholdScale(temp["Happiness"])} catch{return thresholdScale(99)}})
      .style('stroke', 'white')
      .style('stroke-width', 1.5)
      .style("opacity",0.8)
      // tooltips
        .style("stroke","white")
        .style('stroke-width', 0.3)
        .on('mouseover',function(d){
          tip.show(d);

          d3.select(this)
            .style("opacity", 1)
            .style("stroke","white")
            .style("stroke-width",3);
        })
        .on('mouseout', function(d){
          tip.hide(d);

          d3.select(this)
            .style("opacity", 0.8)
            .style("stroke","white")
            .style("stroke-width",0.3);
        })
        .on("click", function(t){console.log(t);

          var svgNew=d3.select("body")
          .append("svg")
          .attr("width",width)
          .attr("height", height)
          var g = svgNew.append("g")
          .attr("transform", "translate(" + width / 2 + "," + height / 2 +")")

          var arc = d3.arc()
          	.innerRadius(0)
          	.outerRadius(240)
          	.cornerRadius(0)

          var temp = t["happiness"];
          var country = t["id"]
          var total = temp["Happiness"]
          var data = Object.values(temp["Details"]);
      		var arcs = d3.pie()(data);
          var colors = d3.scaleOrdinal()
                         .domain(["Economy", "Family", "Health", "Freedom", "Trust", "Generosity", "Residual" ])
                         .range(["#98abc5", "#8a89a6", "#7b6888", "#5b486b", "#a05d56", "#d0743c", "#ff8c00"]);

          var background = g.selectAll("path")
          		.data(arcs)
          		.enter()
          		.append("path")
              .style("fill", function(d,i){return d3.color("hsl(120, 80%, " + d.value   + "%)");})
              .style("fill", function(d,i){return d3.color("hsl(" + d.value * 1000 % 360 + ",50%, 50%)");})
      				.attr("d", arc)
              .append("text")
              .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
              .attr("dy", ".35em")
              .style("text-anchor", "middle")
              .text(function(d){return d})

              .on('mouseover', function(d){
                tip.show(d);
              })

      })

  svg.append("path")
      .datum(topojson.mesh(data.features, function(a, b) { return a.id !== b.id; }))
       // .datum(topojson.mesh(data.features, function(a, b) { return a !== b; }))
      .attr("class", "names")
      .attr("d", path);
}
