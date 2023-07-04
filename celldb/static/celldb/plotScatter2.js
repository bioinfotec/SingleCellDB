fetch("api/tran/all")
  .then((res) => res.json())
  .then((testString) => {
    var chartDom = document.getElementById("Scatter");
    var myChart = echarts.init(chartDom);
    var option;
    // 处理数据
    var cell_type = [];
    plotdata = testString.map(function (value, index) {
      if (cell_type.indexOf(value.cell_type) === -1) {
        cell_type.push(value.cell_type);
      }
      return [
        parseFloat(value.umap_x).toFixed(2),
        parseFloat(value.umap_y).toFixed(2),
        value.cell_type,
      ];
    });
    // 生成transform_option
    var transform_option = [];
    for (var i = 0; i < cell_type.length; i++) {
      transform_option.push({
        transform: {
          type: "filter",
          config: { dimension: "cell_type", "=": cell_type[i] },
        },
      });
    }
    // 生成多个series
    var series = [];
    for (var i = 0; i < cell_type.length; i++) {
      series.push({
        name: cell_type[i],
        type: "scatter",
        emphasis: {
          focus: "series",
        },
        datasetIndex: i + 1,
        symbolSize: 2,
        encode: {
          x: "x",
          y: "y",
        },
      });
    }
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
        max: 20,
        min: -20,
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
        max: 20,
        min: -20,
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

      legend: {
        data: cell_type, // 初始为空数组，用于存储动态生成的图例项
        orient: "vertical",
        right: "5%",
        type: "scroll",
        selected: {
          ...cell_type.reduce((acc, type) => {
            acc[type] = true;
            return acc;
          }, {}),
        },
      },
      dataset: [
        {
          dimensions: ["x", "y", "cell_type"],
          source: plotdata,
        },
        ...transform_option,
      ],
      series: [...series],
    };
    option && myChart.setOption(option);
    // 下拉框
    var cellTypeSelect = document.getElementById("cellTypeSelect");
    ["ALL"].concat(cell_type).forEach(function (type) {
      var option = document.createElement("option");
      option.value = type;
      option.text = type;
      cellTypeSelect.appendChild(option);
    });

    // 监听下拉框事件
    cellTypeSelect.addEventListener("change", function (event) {
      var selectedCellType = event.target.value;
      var legendSelected = {};

      // 更新图例选中状态
      if (selectedCellType === "ALL") {
        cell_type.forEach(function (type) {
          legendSelected[type] = true;
        });
      } else {
        cell_type.forEach(function (type) {
          legendSelected[type] = type === selectedCellType;
        });
      }
      myChart.setOption({
        legend: {
          selected: legendSelected,
        },
      });
    });
  });
