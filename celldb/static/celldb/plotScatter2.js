fetch(singledataUrl)
.then(res => res.text())
.then(testString =>{
    var chartDom = document.getElementById('Scatter');
    var myChart = echarts.init(chartDom);
    var option;
    const rawdata = testString.split('\r\n').map(item => item.split(','))
    let singledata = [];
    let cell_type = [];
    for (var i = 1; i < rawdata.length; i++) {
        singledata.push([parseFloat(rawdata[i][5]), parseFloat(rawdata[i][6]), rawdata[i][1]]);      
        cell_type.push(rawdata[i][1]);
    }
    cell_type = Array.from(new Set(cell_type));
    cell_type.pop();
    option = {
    dataset: [{
        source: singledata,
        },
        {
            transform: {
                type: 'filter',
                config: {
                    dimension: 2, value:cell_type[0]
                }
            }
        },
        {
            transform: {
                type: 'filter',
                config: {
                    dimension: 2, value:cell_type[1]
                }
            }
        },
        {
            transform: {
                type: 'filter',
                config: {
                    dimension: 2, value:cell_type[2]
                }
            }
        }

        ],
    title: {
        text: 'SingleCellUMAP',
        left: '5%',
        top: '3%'
    },
    legend: {
        right: '10%',
        top: '3%',
        data: [cell_type[0], cell_type[1], cell_type[2]]
    },
    grid: {
        left: '8%',
        top: '10%'
    },
    xAxis: {

    },
    yAxis: {
        
    },
    series: [
        {
        name: cell_type[0],
        datasetIndex: 1,
        type: 'scatter',
        symbolSize: 2,
        emphasis: {
            focus: 'series',
            label: {
            show: true,
            // formatter: function (param) {
            //     return param.data[2];
            // },
            position: 'top'
            }
        },
        itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(120, 36, 50, 0.5)',
            shadowOffsetY: 5,
            color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [
            {
                offset: 0,
                color: 'rgb(251, 118, 123)'
            },
            {
                offset: 1,
                color: 'rgb(204, 46, 72)'
            }
            ])
        }
        },
        {
        name: cell_type[1],
        datasetIndex: 2,
        type: 'scatter',
        symbolSize: 2,
        emphasis: {
            focus: 'series',
            label: {
            show: true,
            // formatter: function (param) {
            //     return param.data[2];
            // },
            position: 'top'
            }
        },
        itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(25, 100, 150, 0.5)',
            shadowOffsetY: 5,
            color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [
            {
                offset: 0,
                color: 'rgb(129, 227, 238)'
            },
            {
                offset: 1,
                color: 'rgb(25, 183, 207)'
            }
            ])
        }
        },
        {
        name: cell_type[2],
        datasetIndex: 2,
        type: 'scatter',
        symbolSize: 2,
        emphasis: {
            focus: 'series',
            label: {
            show: true,
            // formatter: function (param) {
            //     return param.data[2];
            // },
            position: 'top'
            }
        },
        itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(25, 100, 150, 0.5)',
            shadowOffsetY: 5,
            color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [
            {
                offset: 0,
                color: 'rgb(129, 227, 238)'
            },
            {
                offset: 1,
                color: 'rgb(25, 183, 207)'
            }
            ])
        }
        }
    ]
    };

    option && myChart.setOption(option);
})