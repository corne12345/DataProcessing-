// Corné Heijnen
// 12230170
// NB: Since I've been ill for a few days, I wasn't able to finish the project entirely. This version
// contains everything up until the legend part. There has also been little work done in terms of layout
// of the html page or the graph and the code has not been optimized yet.

var width = 500;
var height = 500;
var padding = 50;
var svg;

window.onload = function() {
  // Only countries with no missing data are added in this list (Netherlands, Great Britain and Germany are taken out)
  var linkData = "https://stats.oecd.org/SDMX-JSON/data/MSTI_PUB/TH_WRXRS.FRA+KOR+PRT/all?startTime=2007&endTime=2015"
  var consConf = "https://stats.oecd.org/SDMX-JSON/data/HH_DASH/FRA+KOR+PRT.COCONF.A/all?startTime=2007&endTime=2015"
  var response = [d3.json(linkData), d3.json(consConf)]

  Promise.all(response).then(function(response) {
    let dataArray = [];

    for (var count = 0; count < response.length; count++) {
      var data = transformResponse(response[count]);
      dataArray.push(data);
    }
    var dataset = createDataset(dataArray);
    console.log(dataset);
    createSVG(dataset);

  }).catch(function(e){
      throw(e);
  });

  // Function provided by https://data.mprog.nl/course/10%20Homework/100%20D3%20Scatterplot/scripts/transformResponseV1.js
  function transformResponse(data){

    // access data property of the response
    let dataHere = data.dataSets[0].series;

    // access variables in the response and save length for later
    let series = data.structure.dimensions.series;
    let seriesLength = series.length;

    // set up array of variables and array of lengths
    let varArray = [];
    let lenArray = [];

    series.forEach(function(serie){
        varArray.push(serie);
        lenArray.push(serie.values.length);
    });

    // get the time periods in the dataset
    let observation = data.structure.dimensions.observation[0];

    // add time periods to the variables, but since it's not included in the
    // 0:0:0 format it's not included in the array of lengths
    varArray.push(observation);

    // create array with all possible combinations of the 0:0:0 format
    let strings = Object.keys(dataHere);

    // set up output array, an array of objects, each containing a single datapoint
    // and the descriptors for that datapoint
    let dataArray = [];

    // for each string that we created
    strings.forEach(function(string){
        // for each observation and its index
        observation.values.forEach(function(obs, index){
            let data = dataHere[string].observations[index];
            if (data != undefined){

                // set up temporary object
                let tempObj = {};

                let tempString = string.split(":").slice(0, -1);
                tempString.forEach(function(s, indexi){
                    tempObj[varArray[indexi].name] = varArray[indexi].values[s].name;
                });

                // every datapoint has a time and ofcourse a datapoint
                tempObj["time"] = obs.name;
                tempObj["datapoint"] = data[0];
                dataArray.push(tempObj);
            }
        });
    });

    // return the finished product!
    return dataArray;
}

function createDataset (dataArray){
  var confiArray = dataArray[1];
  var womArray = dataArray[0];
  let dataset = []
    for (var count = 0; count < dataArray[0].length; count++){
      var temArray = [confiArray[count].time, confiArray[count].Country, confiArray[count].datapoint, womArray[count].datapoint]
      dataset.push(temArray);
    }
    return dataset
}

function createSVG(dataset){

  var x_values = [];
  var y_values = [];
  dataset.forEach(function(element){
    var x = element[2];
    x_values.push(x);

    var y = element[3];
    y_values.push(y);
  })
  var yMin = Math.min(... y_values);
  var yMax = Math.max(... y_values);

  var xMin = Math.min(... x_values);
  var xMax = Math.max(... x_values);

  // ColorBrewer was used to select hte colors (http://colorbrewer2.org/#type=qualitative&scheme=Paired&n=9)
  var colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "fdbf6f", "ff7f00", "#cab2d6"];

  //Create SVG element
  var svg = d3.select("body")
              .append("svg")
              .attr("width", width)
              .attr("height", height);

  svg.selectAll("circle")
  .data(dataset)
  .enter()
  .append("circle")
  .attr("cx", function(d) {
          return ((d[2]-xMin)/(xMax-xMin)) * (width - 2 * padding) + padding;
    })
    .attr("cy", function(d) {
         return ((d[3]-yMin)/(yMax-yMin)) * (width - 2 * padding) + padding;
    })
    .attr("r", 5)
    .attr("fill", function (d) {return colors[d[0] - 2007]});

    var xScale = d3.scaleLinear()
                   .domain([xMin, xMax])
                   .range([padding, width - padding]);

    var yScale = d3.scaleLinear()
                   .domain([yMin, yMax])
                   .range([height - padding, padding]);

    var xAxis = d3.axisBottom(xScale);
    var yAxis = d3.axisLeft(yScale);


    // Create xAxis on sVG
    svg.append("g")
       .attr("transform", "translate(0," + (height - padding) + ")")
       .attr("class", "text")
       .call(xAxis);

    // Create xAxis label
    svg.append("text")
       .attr("transform", "translate(" + (width/2) + "," + (height - padding + 40) + ")")
       .attr("class", "text")
       .text("Consumer Confidence");

    // Create yAxis on SVG
    svg.append("g")
    .attr("transform", "translate(" + padding + "," + "-" + 0 + " )")
       .attr("class", "text")
       .call(yAxis);

    // Create yAxis Label
    svg.append("text")
       .attr("transform", "rotate(-90)")
       .attr("y", 0 + 20)
       .attr("x", 0 - (height- 150))
       .attr("class", "text")
       .text("% Female researchers");

    // Create title
    svg.append("text")
       .attr("y", 20)
       .attr("x", width / 2 - 100)
       .attr("class", "text")
       .text("Female researchers vs. consumer confidence")

    const legend = svg.append("g")
                      .attr("transform",
           "translate(" + (width + padding) +
           "," + (height / 2) + ")"
         );


}
}
