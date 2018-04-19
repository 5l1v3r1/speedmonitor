function drawLineChart() {
    var jsonData = $.ajax({
	url: '/ajaxCb.php?action=getSpeedData',
	method: 'GET',
	dataType: 'json',
	success: function(result) {
    	    renderGraph(result);
	}
    });
}

function renderGraph(data) {
    ctx = document.getElementById("canvas").getContext("2d");

    var lineChartData = {
      labels: data.label,
      datasets: [{
	    borderColor: window.chartColors.red,
	    backgroundColor: window.chartColors.red,          
	    data: data.upload,
	    fill: false,
	    label: 'Upload'
	}, {
	    borderColor: window.chartColors.blue,
	    backgroundColor: window.chartColors.blue,          
	    data: data.download,
	    fill: false,
	    label: 'Download'
	}]
    };

    var lineChartOptions = {
    };

    var myChart = new Chart(ctx, {
	type: 'line',
	data: lineChartData,
	options: lineChartOptions
    });
}

$(document).ready(function(){
    drawLineChart();
});