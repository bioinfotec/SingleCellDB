var singledata = [];
var cell_type = [];
// 读取数据
fetch(singledataUrl)
  .then((res) => res.text())
  .then((testString) => {
    const rawdata = testString.split("\r\n").map((item) => item.split(","));
    header = [rawdata[0][5], rawdata[0][6], rawdata[0][1]];

    //singledata.push(header)
    for (var i = 1; i < rawdata.length; i++) {
      singledata.push([
        parseFloat(rawdata[i][5]),
        parseFloat(rawdata[i][6]),
        rawdata[i][1],
      ]);
      cell_type.push(rawdata[i][1]);
    }
    cell_type = Array.from(new Set(cell_type));
    cell_type.pop(); // echarts绘图
    var chart = echarts.init(document.getElementById("Scatter"));
    //配置颜色
    var pieces = [];
    var COLOR_ALL = [
      "#5B8FF9",
      "#61DDAA",
      "#F6BD16",
      "#7262FD",
      "#78D3F8",
      "#9661BC",
      "#F6903D",
      "#008685",
      "#F08BB4",
      "#F5EBC8",
      "#6DC8EC",
      "#9270CA",
      "#FF9D4D",
      "#269A99",
      "#5B8FF9",
      "#CD69C9",
      "#F6BD16",
      "#6DC8EC",
      "#F6903D",
      "#008685",
      "#F08BB4",
      "#F5EBC8",
      "#78D3F8",
      "#9270CA",
      "#FF9D4D",
      "#269A99",
      "#FF99C3",
      "#0084FF",
      "#D60000",
      "#008080",
      "#D6A300",
      "#AAAAAA",
    ];
    var color = [];
    for (var i = 0; i < cell_type.length; i++) {
      color.push(COLOR_ALL[i]);
    }
    // 指定图表的配置项和数据
    option = {
      title: {
        text: "UMAP",
        left: "center",
        top: "3%",
      },
      xAxis: {
        name: "UMAP_X",
        nameLocation: "middle",
        nameGap: 25,
        nameTextStyle: {
          fontSize: 18,
        },
        axisLine: {
          onZero: false,
        },
        splitLine: { show: false },
      },
      yAxis: {
        name: "UMAP_Y",
        nameLocation: "middle",
        nameGap: 25,
        nameTextStyle: {
          fontSize: 18,
        },
        axisLine: {
          onZero: false,
        },
        splitLine: { show: false },
      },
      tooltip: {
        position: "top",
        formatter: function (params) {
          var data = params.data;
          var formattedTooltip =
            "Cell: " + data[2] + "<br>X: " + data[0] + "<br>Y: " + data[1];
          return formattedTooltip;
        },
      },
      grid: {
        left: "5%",
        right: "15%",
        // show: true,
      },
      dataset: [
        {
          source: singledata,
        },
      ],
      visualMap: [
        {
          left: "right",
          top: "60",
          inRange: {
            color: color,
          },
          dimension: 2,
          categories: cell_type,
          align: "auto",
          hoverLink: false,
        },
      ],
      series: {
        type: "scatter",
        data: singledata,
        symbolSize: 2.5,
        // encode: { tooltip: [0, 1, 2] },
      },
    };
    // 使用刚指定的配置项和数据显示图表。
    chart.setOption(option);
  });
