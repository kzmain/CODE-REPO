// 每年/各季度对比情况
/* Chart code */
// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

/**
 * This is a copy of a chart created by Antti Lipponen: https://twitter.com/anttilip?lang=en Thanks a lot!
 */

// disclaimer: this data is not accuarate, don't use it for any puroposes
// first temperature is average for 1973-1980 period

var seasons = {
  "Autumn": [
    ["Oct,Nov,Dec", 0, 43029658, 40302293, 43357150, 41505876, 43235942, 43832950, 64658465, 73637730, 86710989, 96756008],
    ],

    "Winter": [
    ["Jan,Feb,Mar", 0, 40187922, 37583503, 41341748, 44290160, 43075426, 44078225, 51162584, 65934352, 74598494, 89809010],
    ],
  
  "Spring": [
    ["Apr,May,Jun", 0, 41915955, 43737968, 43386711, 44248428, 42755638, 45615731, 54887829, 70316948, 77955927, 92895524],
    ],

  "Summer": [
    ["Jul,Aug,Sep", 0, 40112186, 41047087, 40826226, 41513240, 39480476, 41593872, 53782591, 67803018, 76384849, 91216685],
    ],
}

var startYear = 2009;
var endYear = 2018;
var currentYear = 2009;
var colorSet = new am4core.ColorSet();

var chart = am4core.create("chartdiv", am4charts.RadarChart);
// chart.numberFormatter.numberFormat = "+#.0°C|#.0°C|0.0°C";
chart.hiddenState.properties.opacity = 0;

chart.startAngle = 270 - 180;
chart.endAngle = 270 + 180;

// radius & inner radius
chart.padding(5, 15, 5, 10)
chart.radius = am4core.percent(65);
chart.innerRadius = am4core.percent(25);   

// year label goes in the middle   2009-2018
var yearLabel = chart.radarContainer.createChild(am4core.Label);
yearLabel.horizontalCenter = "middle";
yearLabel.verticalCenter = "middle";
yearLabel.fill = am4core.color("#673AB7");
yearLabel.fontSize = 30;
yearLabel.text = String(currentYear);

// zoomout button 
var zoomOutButton = chart.zoomOutButton;
zoomOutButton.dx = 0;
zoomOutButton.dy = 0;
zoomOutButton.marginBottom = 15;
zoomOutButton.parent = chart.rightAxesContainer;

// scrollbar  (on the right)
chart.scrollbarX = new am4core.Scrollbar();
chart.scrollbarX.parent = chart.rightAxesContainer;
chart.scrollbarX.orientation = "vertical";
chart.scrollbarX.align = "center";
chart.scrollbarX.exportable = false;

// vertical orientation for zoom out button and scrollbar to be positioned properly
chart.rightAxesContainer.layout = "vertical";
chart.rightAxesContainer.padding(120, 20, 120, 20);

// category axis  与显示出的圆圈（图有关）
var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.dataFields.category = "years";

var categoryAxisRenderer = categoryAxis.renderer;
var categoryAxisLabel = categoryAxisRenderer.labels.template;
categoryAxisLabel.location = 0.5;
categoryAxisLabel.radius = 28;    // 国家名与外层圆圈的距离
categoryAxisLabel.relativeRotation = 90;   //国家名显示的角度 - 90度 垂直

categoryAxisRenderer.fontSize = 14;  //国家名字体大小
categoryAxisRenderer.minGridDistance = 10;
categoryAxisRenderer.grid.template.radius = -25;
categoryAxisRenderer.grid.template.strokeOpacity = 0.05;
categoryAxisRenderer.grid.template.interactionsEnabled = false;

categoryAxisRenderer.ticks.template.disabled = true;
categoryAxisRenderer.axisFills.template.disabled = true;
categoryAxisRenderer.line.disabled = true;

categoryAxisRenderer.tooltipLocation = 0.5;
categoryAxis.tooltip.defaultState.properties.opacity = 0;

// value axis
var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.min = 0;
valueAxis.max = 100000000;     //最大最小值范围（坐标）
valueAxis.strictMinMax = true;
valueAxis.tooltip.defaultState.properties.opacity = 0;
valueAxis.tooltip.animationDuration = 0;
valueAxis.cursorTooltipEnabled = true;
valueAxis.zIndex = 10;

var valueAxisRenderer = valueAxis.renderer;
valueAxisRenderer.axisFills.template.disabled = true;
valueAxisRenderer.ticks.template.disabled = true;
valueAxisRenderer.minGridDistance = 15;   //内外之间格子宽度
valueAxisRenderer.grid.template.strokeOpacity = 0.05;  //刻度线


// series
var series = chart.series.push(new am4charts.RadarColumnSeries());
series.columns.template.width = am4core.percent(90);
series.columns.template.strokeOpacity = 0;
series.dataFields.valueY = "value" + currentYear;
series.dataFields.categoryX = "years";
series.tooltipText = "{categoryX}:{valueY.value}";

// this makes columns to be of a different color, depending on value
series.heatRules.push({ target: series.columns.template, property: "fill",maxValue: 50000000, max: am4core.color("#F44336"), dataField: "valueY" });

// cursor
var cursor = new am4charts.RadarCursor();
chart.cursor = cursor;
cursor.behavior = "zoomX";

cursor.xAxis = categoryAxis;
cursor.innerRadius = am4core.percent(40);
cursor.lineY.disabled = true;

cursor.lineX.fillOpacity = 0.2;
cursor.lineX.fill = am4core.color("#000000");
cursor.lineX.strokeOpacity = 0;
cursor.fullWidthLineX = true;

// year slider
var yearSliderContainer = chart.createChild(am4core.Container);
yearSliderContainer.layout = "vertical";
yearSliderContainer.padding(0, 38, 0, 38);
yearSliderContainer.width = am4core.percent(100);

var yearSlider = yearSliderContainer.createChild(am4core.Slider);
yearSlider.events.on("rangechanged", function() {
  updateRadarData(startYear + Math.round(yearSlider.start * (endYear - startYear)));
})
yearSlider.orientation = "horizontal";
yearSlider.start = 0.5;
yearSlider.exportable = false;

chart.data = generateRadarData();

function generateRadarData() {
  var data = [];
  var i = 0;
  for (var values in seasons) {
    var valuesData = seasons[values];

    valuesData.forEach(function(years) {
      var rawDataItem = { "years": years[0] }

      for (var y = 2; y < years.length; y++) {
        rawDataItem["value" + (startYear + y - 2)] = years[y];
      }

      data.push(rawDataItem);
    });

    createRange(values, valuesData, i);
    i++;

  }
  return data;
}


function updateRadarData(year) {
  if (currentYear != year) {
    currentYear = year;
    yearLabel.text = String(currentYear);
    series.dataFields.valueY = "value" + currentYear;
    chart.invalidateRawData();
  }
}

function createRange(name, valuesData, index) {

  var axisRange = categoryAxis.axisRanges.create();
  axisRange.axisFill.interactionsEnabled = true;
  axisRange.text = name;
  // first value
  axisRange.category = valuesData[0][0];
  // last value
  axisRange.endCategory = valuesData[valuesData.length - 1][0];

  // every 3rd color for a bigger contrast
  axisRange.axisFill.fill = colorSet.getIndex(index * 3);
  axisRange.grid.disabled = true;
  axisRange.label.interactionsEnabled = false;

  var axisFill = axisRange.axisFill;
  axisFill.innerRadius = -0.001; // almost the same as 100%, we set it in pixels as later we animate this property to some pixel value
  axisFill.radius = -20; // negative radius means it is calculated from max radius
  axisFill.disabled = false; // as regular fills are disabled, we need to enable this one
  axisFill.fillOpacity = 1;
  axisFill.togglable = true;

  axisFill.showSystemTooltip = true;
  axisFill.readerTitle = "click to zoom";
  axisFill.cursorOverStyle = am4core.MouseCursorStyle.pointer;

  axisFill.events.on("hit", function(event) {
    var dataItem = event.target.dataItem;
    if (!event.target.isActive) {
      categoryAxis.zoom({ start: 0, end: 1 });
    }
    else {
      categoryAxis.zoomToCategories(dataItem.category, dataItem.endCategory);
    }
  })

  // hover state
  var hoverState = axisFill.states.create("hover");
  hoverState.properties.innerRadius = -10;
  hoverState.properties.radius = -25;

  var axisLabel = axisRange.label;
  axisLabel.location = 0.5;
  axisLabel.fill = am4core.color("#ffffff");
  axisLabel.radius = 3;
  axisLabel.bent = true;
}

var slider = yearSliderContainer.createChild(am4core.Slider);
slider.start = 1;
slider.exportable = false;
slider.events.on("rangechanged", function() {
  var start = slider.start;

  chart.startAngle = 270 - start * 179 - 1;
  chart.endAngle = 270 + start * 179 + 1;

  valueAxis.renderer.axisAngle = chart.startAngle;
})