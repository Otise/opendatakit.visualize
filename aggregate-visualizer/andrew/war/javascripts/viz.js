
//load google's stuff...
google.load('visualization', '1', {'packages':['piechart','barchart','linechart']});

google.setOnLoadCallback(initViz);



//makes n selectors for n variables
function makeForm( n ){
	columnSelectorOptions = document.getElementById("columnselector").innerHTML;
	variableSelection = document.getElementById("variableselection");
	
	//clear out the variableSelection
	while (variableSelection.hasChildNodes()) 
		variableSelection.removeChild(variableSelection.firstChild);
	
	//put new selectors in...
	for ( var i = 0; i <= n  ; i++){
		var select = document.createElement("select");
		var label = document.createElement("label");
		
		if(i < n) select.name = "variable" + i;
		//else if (i == n) select.name = "groupby";
		else if (i == n) select.name = "filter";
		
		select.id = select.name;
		select.innerHTML = columnSelectorOptions;
		
		label.innerHTML = select.name;
		label.setAttribute("for", select.name);
		
		variableSelection.appendChild(label);
		variableSelection.appendChild(select);
		variableSelection.appendChild(document.createElement("br"));
	}
	
	//create a way to select different charts
	var chartSelect = document.createElement("select");
	chartSelect.name = "chartselect";
	chartSelect.id = "chartselect";
	
	var chartTypes = ['piechart', 'barchart', 'linechart'];
	
	for ( i in chartTypes){
		var chartOption = document.createElement("option");
		chartOption.value = chartTypes[i];
		chartOption.innerHTML = chartTypes[i];
		chartSelect.appendChild(chartOption);
	}
	
	variableSelection.appendChild(chartSelect);
	
	var hiddenCount = document.createElement("input");
	hiddenCount.type = "hidden";
	hiddenCount.name = "variablecount";
	hiddenCount.id = "variablecount";
	hiddenCount.value = n;
	
	variableSelection.appendChild(hiddenCount);
	
	//the following is for mapping data...
	var mapForm = document.getElementById("mapform");
	
	var latSelect = document.createElement("select");
	latSelect.name = "latitude";
	latSelect.id = "latitude";
	latSelect.innerHTML = columnSelectorOptions;
	
	var lonSelect = document.createElement("select");
	lonSelect.name = "longitude";
	lonSelect.id = "longitude";
	lonSelect.innerHTML = columnSelectorOptions;
	
	var valSelect = document.createElement("select");
	valSelect.name = "mapvalue";
	valSelect.id = "mapvalue";
	valSelect.innerHTML = columnSelectorOptions;
	
	var filterSelect = document.createElement("select");
	filterSelect.name = "mapfilter";
	filterSelect.id = "mapfilter";
	filterSelect.innerHTML = columnSelectorOptions;
	
	var latLabel = document.createElement("label");
	latLabel.setAttribute("for", latSelect.name);
	latLabel.innerHTML = latSelect.name;
	
	var lonLabel = document.createElement("label");
	lonLabel.setAttribute("for", lonSelect.name);
	lonLabel.innerHTML = lonSelect.name;
	
	var valLabel = document.createElement("label");
	valLabel.setAttribute("for", valSelect.name);
	valLabel.innerHTML = valSelect.name;
	
	var filterLabel = document.createElement("label");
	valLabel.setAttribute("for", filterSelect.name);
	valLabel.innerHTML = filterSelect.name;
	
	var submit = document.createElement("input");
	submit.setAttribute("type", "submit");
	
	mapForm.appendChild(latLabel);
	mapForm.appendChild(latSelect);
	mapForm.appendChild(document.createElement("br"));
	
	mapForm.appendChild(lonLabel);
	mapForm.appendChild(lonSelect);
	mapForm.appendChild(document.createElement("br"));
	
	mapForm.appendChild(valLabel);
	mapForm.appendChild(valSelect);
	mapForm.appendChild(document.createElement("br"));
	
	mapForm.appendChild(filterLabel);
	mapForm.appendChild(filterSelect);
	mapForm.appendChild(document.createElement("br"));
	
	mapForm.appendChild(submit);
		
}

//parse the chart form and get values from selects
function doCharting(){
	//get the hidden count of variables
	var n = document.getElementById("variablecount").getAttribute("value");
	
	//get the doc uri
	var spreadsheetURI = //document.getElementById("spreadsheeturi").getAttribute("value");
		"http://spreadsheets.google.com/ccc?key=0AqQYrqEwPtYldEVreklPQ21FYXVMYmtVdFlybUlGWlE&hl=en";

	//get the columns
	var varArray = new Array();
	var groupby, filter;
	for (var i = 0; i <= n; i++){
		if(i < n) varArray[i] = document.getElementById("variable" + i).value;
		//else if (i == n) grouby = document.getElementById("groupby").value;
		else if (i == n) filter = document.getElementById("filter").value;
	}
	
	// Replace the data source URL on next line with your data source URL.
	var query = new google.visualization.Query(spreadsheetURI);
  
	var qString = 'select ';
	
	for(var i in varArray){
		qString += varArray[i];
		if( i < varArray.length - 1) qString += ", ";
	}
	
	qString += " WHERE " + filter + " = true ";
	query.setQuery(qString);
	
	alert(qString);
		
	query.send(handleChartQueryResponse);
	//query.send(handleMapQueryResponse);
}

//parse the map form and get values from selects
function doMapping(){
	
	//get the doc uri
	var spreadsheetURI = //document.getElementById("spreadsheeturi").getAttribute("value");
		"http://spreadsheets.google.com/ccc?key=0AqQYrqEwPtYldEVreklPQ21FYXVMYmtVdFlybUlGWlE&hl=en";

	//get the columns
	var lat, lon, val;
	
	lat = document.getElementById("latitude").value;
	lon = document.getElementById("longitude").value;
	val = document.getElementById("mapvalue").value;
	fil = document.getElementById("mapfilter").value;
	
	// Replace the data source URL on next line with your data source URL.
	var query = new google.visualization.Query(spreadsheetURI);
  
	var qString = 'SELECT ' + lat + ', ' + lon + ', ' + val + ' WHERE ' + fil + " = true";
	
	query.setQuery(qString);
	
	alert(qString);
	query.send(handleMapQueryResponse);
}



function handleChartQueryResponse(response) {

	if (response.isError()) {
		alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
		return;
	}

	var data = response.getDataTable();
	
	var chartFunction = google.visualization.PieChart;
	
	switch(document.getElementById("chartselect").value){
		case "barchart" :
			chartFunction = google.visualization.BarChart;
			break;
		case "piechart" :
			chartFunction = google.visualization.PieChart;
			break;
		case "linechart" :
			chartFunction = google.visualization.LineChart;
			break;
		default:
			break;
	}
	
	var chart = new chartFunction(document.getElementById('chart_div'));
	chart.draw(data, {width: 400, height: 240, is3D: true});
}


function handleMapQueryResponse(response) {

	if (response.isError()) {
		alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
		return;
	}

	var data = response.getDataTable();
	
	var map = new GMap2(document.getElementById("map_div"));
	map.setUIToDefault();
	map.setCenter(new GLatLng(data.getFormattedValue(0,0), data.getFormattedValue(0,1)), 13);

	
	for (var row = 0; row < data.getNumberOfRows(); row++){		
		var point = new GLatLng(data.getFormattedValue(row, 0),
								data.getFormattedValue(row, 1));
		map.addOverlay(new GMarker(point));
	}
}



function initViz(){
	makeForm(2);
}
