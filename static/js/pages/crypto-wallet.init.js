function getChartColorsArray(e){if(null!==document.getElementById(e)){e=document.getElementById(e).getAttribute("data-colors");if(e)return(e=JSON.parse(e)).map(function(e){var t=e.replace(" ","");return-1===t.indexOf(",")?getComputedStyle(document.documentElement).getPropertyValue(t)||t:2==(e=e.split(",")).length?"rgba("+getComputedStyle(document.documentElement).getPropertyValue(e[0])+","+e[1]+")":t})}}var options,chartOverview,overviewChartColors=getChartColorsArray("overview-chart");overviewChartColors&&(options={series:[{type:"area",name:"BTC",data:[87,57,74,99,75,38,62,47,82,56,45,47]},{type:"area",name:"ETH",data:[28,41,52,42,13,18,29,18,36,51,55,35]},{type:"line",name:"LTC",data:[45,52,38,24,33,65,45,75,54,18,28,10]}],chart:{height:240,type:"line",toolbar:{show:!1}},dataLabels:{enabled:!1},stroke:{curve:"smooth",width:2,dashArray:[0,0,3]},fill:{type:"solid",opacity:[.15,.05,1]},xaxis:{categories:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]},colors:overviewChartColors},(chartOverview=new ApexCharts(document.querySelector("#overview-chart"),options)).render(),$(document).ready(function(){$("#datatable").DataTable(),$(".dataTables_length select").addClass("form-select form-select-sm")}));