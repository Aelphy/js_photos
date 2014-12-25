$.get('data.csv', function(data) {
  var options = {
    chart: {
      type: 'scatter',
      zoomType: 'xy'
    },
    title: {
      text: 'Photos per day'
    },
    subtitle: {
      text: 'Shipulina Ekaterina, 2014'
    },
    xAxis: {
      type: 'datetime',
      dateTimeLabelFormats: { // don't display the dummy year
      month: '%e. %b',
      year: '%b'
      },
      title: {
        text: 'Date'
      }
    },
    yAxis: {
      title: {
        text: 'Photos'
      }
    },
    legend: {
      layout: 'vertical',
      align: 'left',
      verticalAlign: 'top',
      x: 700,
      y: 70,
      floating: true,
      backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
      borderWidth: 1
    },
    tooltip: {
      useHTML: true,
      formatter: function () {
        return '<img class="friends_photo_img" src=' + this.point.name + '/>';
      }
    },
    plotOptions: {
      series: {
        turboThreshold: 0
      },
      scatter: {
        marker: {
          radius: 5,
          states: {
            hover: {
              enabled: true,
              lineColor: 'rgb(100,100,100)'
            }
          }
        },
        states: {
          hover: {
            marker: {
              enabled: false
            }
          }
        }
      }
    },
    series: [{
      data: []
    }]
  };

  // Split the lines
  var lines = data.split('\n');

  // Iterate over the lines and add series
  $.each(lines, function(lineNo, line) {
    var items = line.split(',');

    // the rest of the lines contain data with their name in the first
    // position
    data = {};

    time = items[0].split(':');

    data.name = items[1];
    data.color = items[2];
    data.x = Date.UTC(time[0], time[1], time[2]);
    data.y = parseFloat(items[3]);

    options.series[0].data.push(data);
  });

  // Create the chart
  $('#container').highcharts(options);
});
