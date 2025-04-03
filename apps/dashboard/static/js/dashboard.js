$(function () {
  setgraphdata();
  setlinechart();
});

function setgraphdata() {
  // //Better to construct options first and then pass it as a parameter
  // var options = {
  //   title: {
  //     text: ""
  //   },
  //   data: [
  //     {
  //       // Change type to "doughnut", "line", "splineArea", etc.
  //       type: "column",
  //       dataPoints: [
  //         { label: "Registred Users", y: 30 },
  //         { label: "Guides", y: 10 },
  //         { label: "Travel Agencies", y: 25 },
  //         { label: "Pending Approvals", y: 5 },
  //         { label: "App Instalations", y: 15 },
  //         { label: "Admin Users", y: 4 }
  //       ]
  //     }
  //   ]
  // };

  // $("#graphicalSummaryDiv").CanvasJSChart(options);
  var options = {
    animationEnabled: true,
    title: {
      text: ""
    },
    data: [
      {
        type: "doughnut", // Changed from "column" to "doughnut"
        indexLabel: "{label}: {y}", // Label inside chart
        yValueFormatString: "#,##0",
        showInLegend: true,
        legendText: "{label}",
        dataPoints: [
          { label: "Registered Users", y: 30 },
          { label: "Guides", y: 10 },
          { label: "Travel Agencies", y: 25 },
          { label: "Pending Approvals", y: 5 },
          { label: "App Installations", y: 15 },
          { label: "Admin Users", y: 4 }
        ]
      }
    ]
  };
  
  $("#graphicalSummaryDiv").CanvasJSChart(options);
}

function setlinechart()
{
  var options = {
		animationEnabled: true,
		theme: "light2",
		title:{
			text: ""
		},
		axisX:{
			title: "Day",
			valueFormatString: "DDD"
		},
		axisY: {
			title: "Count",
			suffix: "",
			minimum: 0
		},
		toolTip:{
			shared:true
		},  
		legend:{
			cursor:"pointer",
			verticalAlign: "bottom",
			horizontalAlign: "left",
			dockInsidePlotArea: true,
			itemclick: toggleDataSeries
		},
		data: [{
			type: "line",
			showInLegend: true,
			name: "App Installations",
			markerType: "circle",
			color: "#4F81BC",
			dataPoints: [
				{ x: new Date(2025, 2, 17), y: 150 }, // Monday
				{ x: new Date(2025, 2, 18), y: 180 }, // Tuesday
				{ x: new Date(2025, 2, 19), y: 200 }, // Wednesday
				{ x: new Date(2025, 2, 20), y: 220 }, // Thursday
				{ x: new Date(2025, 2, 21), y: 250 }, // Friday
				{ x: new Date(2025, 2, 22), y: 300 }, // Saturday
				{ x: new Date(2025, 2, 23), y: 280 }  // Sunday
			]
		},
		{
			type: "line",
			showInLegend: true,
			name: "User Registrations",
			lineDashType: "dash",
			color: "#C0504E",
			dataPoints: [
				{ x: new Date(2025, 2, 17), y: 100 }, // Monday
				{ x: new Date(2025, 2, 18), y: 120 }, // Tuesday
				{ x: new Date(2025, 2, 19), y: 140 }, // Wednesday
				{ x: new Date(2025, 2, 20), y: 160 }, // Thursday
				{ x: new Date(2025, 2, 21), y: 190 }, // Friday
				{ x: new Date(2025, 2, 22), y: 210 }, // Saturday
				{ x: new Date(2025, 2, 23), y: 200 }  // Sunday
			]
		}]
	};
	$("#chartContainer").CanvasJSChart(options);
}


function toggleDataSeries(e){
  if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
    e.dataSeries.visible = false;
  } else{
    e.dataSeries.visible = true;
  }
  e.chart.render();
}