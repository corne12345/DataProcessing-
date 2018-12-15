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

var color = d3.scaleThreshold()
    .domain([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 99])
    .range(["#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF5500", "#FFBE00","#FFFF00","#D7FF00","#9BFF00","#78FF00","#00FF00", "#000000"]);

var path = d3.geoPath();

var svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append('g')
            .attr('class', 'map');

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
  // data.features.forEach(function(d) {console.log(d)});

  // Own interprestation of above mentioned code
  var happinessByName = {};
  var parameters = {};
  // happiness.forEach(function(d) { happinessByName[d.Country] = [d.Happiness_Score]});
  happiness.forEach(function(d) {parameters = {"Position": d.Happiness_Rank, "Happiness": d.Happiness_Score, "Economy": d.Economy, "Family": d.Family, "Health": d.Health, "Freedom": d.Freedom, "Trust": d.Trust, "Generosity": d.Generosity, "Residual": d.Dystopia_Residual}; happinessByName[d.Country] = parameters});
  // happiness.forEach(function(d) {parameters = {"Happiness": d.Happiness_Score, "Economy": d.Economy, "Family": d.Family, "Health": d.Health, "Freedom": d.Freedom, "Trust": d.Trust, "Generosity": d.Generosity, "Residual": d.Dystopia_Residual}; happinessByName[d.Country] = parameters});
  console.log(happinessByName);
  data.features.forEach(function(d) { d.happiness = happinessByName[d.id]})

  svg.append("g")
      .attr("class", "countries")
    .selectAll("path")
      .data(data.features)
    .enter().append("path")
      .attr("d", path)
      .style("fill", function(d){try{var temp = happinessByName[d.id]; return color(temp["Happiness"])}catch{return color(99)}})
      .style('stroke', 'white')
      .style('stroke-width', 1.5)
      .style("opacity",0.8)
      // tooltips
        .style("stroke","white")
        .style('stroke-width', 0.3)
        .on("click", function(t){console.log(t);
          c=d3.select("body").append("svg").attr("width",width).attr("height", height)})
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
        });

  svg.append("path")
      .datum(topojson.mesh(data.features, function(a, b) { return a.id !== b.id; }))
       // .datum(topojson.mesh(data.features, function(a, b) { return a !== b; }))
      .attr("class", "names")
      .attr("d", path);
}
