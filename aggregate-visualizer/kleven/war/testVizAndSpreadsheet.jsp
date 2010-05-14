<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List" %>
<%@ page import="java.util.Map" %>
<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.Set" %>
<%@ page import="java.util.HashSet" %>
<%@ page import="java.net.URL" %>
<%@ page import="javax.jdo.PersistenceManager" %>
<%@ page import="com.google.gdata.client.spreadsheet.SpreadsheetService"%>
<%@ page import="com.google.gdata.data.spreadsheet.SpreadsheetEntry"%>
<%@ page import="com.google.gdata.data.spreadsheet.SpreadsheetFeed"%>
<%@ page import="com.google.gdata.util.AuthenticationException"%>
<%@ page import="com.google.gdata.util.ServiceException"%>
<%@ page import="com.google.gdata.data.spreadsheet.ListEntry"%>
<%@ page import="com.google.gdata.client.spreadsheet.ListQuery"%>
<%@ page import="com.google.gdata.data.spreadsheet.ListFeed"%>
<%@ page import="com.google.gdata.data.spreadsheet.WorksheetEntry"%>
<%@ page import="com.google.gdata.data.spreadsheet.WorksheetFeed"%>
<%@ page import="edu.washington.cs.aha.HtmlUtil"%>
<%@ page import="edu.washington.cs.aha.ServletUtilBase"%>

<html>
<head>
<title>Basic Viz & Filter</title>
<link rel="stylesheet" href="styles.css" type="text/css" />

	<script type="text/javascript" src="http://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["barchart"]});
      google.load("visualization", "1", {packages:["columnchart"]});
      google.load("visualization", "1", {packages:["linechart"]});
      google.load("visualization", "1", {packages:["piechart"]});
      
    </script>

<%

	SpreadsheetService service = new SpreadsheetService("");
	String key = request.getParameter("key");
	
	String spreadAuth = request.getParameter("spreadAuth");
	String docAuth = request.getParameter("docAuth"); 
	String col1name = request.getParameter("col1"); 
	String col2name = request.getParameter("col2"); 
	String col3name = request.getParameter("col3"); 
	String col1type = request.getParameter("col1type"); 
	String col2type = request.getParameter("col2type"); 
	String sheetName = request.getParameter("sheetName"); 
	service.setAuthSubToken(spreadAuth, null);
	
	Map<String, String> params = new HashMap<String, String>(); 
	params.put("spreadAuth", spreadAuth); 
	params.put("docAuth", docAuth); 
	params.put("key", key); 
	params.put("sheetName", sheetName); 
	
	
	// Saving this for use later
	String baseUrl = HtmlUtil.createLinkWithProperties(//ServletUtilBase.getServerURL(request) + 
                            request.getRequestURI(), params);
    String sumBaseUrl = HtmlUtil.createLinkWithProperties(//ServletUtilBase.getServerURL(request) + 
                            "summarizeColumn.jsp", params);               	
               	
	URL feedUri = new URL("http://spreadsheets.google.com/feeds/worksheets/"+key+"/private/full");

	WorksheetFeed listFeed = service.getFeed(feedUri, WorksheetFeed.class);
	List<WorksheetEntry> worksheets = listFeed.getEntries();//spreadsheetEntry.getWorksheets();
        	
    WorksheetEntry worksheetEntry = worksheets.get(0);
       	
    URL listFeedUrl = worksheetEntry.getListFeedUrl();
    
    ListQuery query = new ListQuery(listFeedUrl);
    // Only get the filtered stuff
	
	String filterQuery = ""; 
	if (!col3name.equals("bah3")){
		filterQuery = col3name + " = true"; 
	}
	
	query.setSpreadsheetQuery(filterQuery);
	ListFeed feed = service.query(query, ListFeed.class);
	
	
    ListEntry firstRow = feed.getEntries().get(0);
	
%>


    <script type="text/javascript">  
      
     	 var data = new google.visualization.DataTable();
<%        
		
		if ( (!col1name.equals("bah1")) && 
			 (!col2name.equals("bah2"))){
		
		  out.println("data.addColumn('string', '"+ col1name +"');");
		  out.println("data.addColumn('"+col2type+"', '"+ col2name +"');");

		  out.println("data.addRows("+feed.getEntries().size()+");");//worksheetEntry.getColCount()-1+");");
		  
		  // label = col1, value=col2
		  int curRow = 0; 
		  for (ListEntry entry : feed.getEntries()) {

			String entryLabel = ""; 
			String entryValue = ""; 
			
			for (String tag : entry.getCustomElements().getTags()) {
			
				if (tag.equals(col1name)){
		        	entryLabel = entry.getCustomElements().getValue(tag);	    
		        }
		        if (tag.equals(col2name)){
		        	entryValue = entry.getCustomElements().getValue(tag); 
		        }
		 	} // for tag
		 	
		 	if (entryLabel != null && entryValue != null){
			 	out.println("data.setValue("+curRow+", 0, '" + entryLabel + "');");
			 	
			 	if (col2type == "string"){
			 		out.println("data.setValue("+curRow+", 1, '" + entryValue+ "');");
			 	}
			 	else{
			 		out.println("data.setValue("+curRow+", 1, " + entryValue+ ");"); // no quotes 
			 	}
			 	  
			 	
			 	
			 	curRow++;
		 	}// for if
		 	
		 }// for entry
		 }// if cols
		 
		 out.println("\n\nvar newBaseUrl = \"" + baseUrl +"\";" );
		 
		 
		 out.println("\n\nvar summarizeBaseUrl = \"" + sumBaseUrl +"\";" );
		 
		 
		 out.println("\n\nvar col1Name = \"" + col1name +"\";" );
		 out.println("var col2Name = \"" + col2name +"\";" );
		 out.println("var col3Name = \"" + col3name +"\";" ); 
		 
		 boolean drawChart = (!col1name.equals("bah1")) && (!col2name.equals("bah2")); 
		 
		 out.println("var doDrawChart = "+ drawChart + ";"); 
		 
%>		  

      var curChartViz = 2; 
      var colType1 = 1; 
      var colType2 = 2; 
      
      function drawChart() {
      	  alert("deciding whether to draw chart");
      	  if (doDrawChart)
      	  {
      	  	alert("updating chart. curChartViz: " + curChartViz); 
	        var chart;  
	        
	        document.getElementById('chart_div').innerHTML = '';
	        
		    switch(curChartViz){
		    	case 1:
		    		chart = new google.visualization.BarChart(document.getElementById('chart_div'));
		    	break; 
		    	case '1':
		    		chart = new google.visualization.BarChart(document.getElementById('chart_div'));
		    	break;
		    	case 2:
		    		chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
		    	break; 
		    	case '2':
		    		chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
		    	break;
		    	case 3:
		    		chart = new google.visualization.LineChart(document.getElementById('chart_div'));
		    	break; 
		    	case '3':
		    		chart = new google.visualization.LineChart(document.getElementById('chart_div'));
		    	break; 
		    	case 4:
		    		chart = new google.visualization.PieChart(document.getElementById('chart_div'));
		    	break; 
		    	case '4':
		    		chart = new google.visualization.PieChart(document.getElementById('chart_div'));
		    	break; 
		    	default: 
		    		chart = new google.visualization.PieChart(document.getElementById('chart_div'));
	    	}

        	chart.draw(data, {width: 800, height: 480, min: 0});
          }
      }
      
      function setCol1Name(dropDown){
        col1Name = dropDown.options[dropDown.selectedIndex].value; 
      }
      
      function setCol2Name(dropDown){
      	col2Name = dropDown.options[dropDown.selectedIndex].value; 
      }
      
      function setCol3Name(dropDown){
      	col3Name = dropDown.options[dropDown.selectedIndex].value; 
      }

	  function reloadWithNewParams(){
	    alert("reloading. NEWbaseUrl: " + newBaseUrl); 
	  	newUrl = newBaseUrl + "&col1=" + col1Name + "&col2="+col2Name + "&col3="+col3Name + "&col1type=" + colType1+"&col2type="+colType2;
	  	alert("newUrl: " + newUrl); 
	  	window.location = newUrl; 
	  }
	  
	  function summarize(){
	  	newUrl = summarizeBaseUrl + "&summarizeCol=" + col1Name + "&filterCol="+col3Name;
	  	alert("newUrl: " + newUrl); 
	  	window.location = newUrl; 
	  }
	  
 	  function vizChanged(whichVizDropDown){
	  	curChartViz = whichVizDropDown.options[whichVizDropDown.selectedIndex].value;  
	    drawChart(); 
	  }

	  function colTypeChanged(whichChooseTypeDropDown, whichCol){
	  	if(whichCol == 1){
	  		colType1 = whichChooseTypeDropDown.options[whichChooseTypeDropDown.selectedIndex].value;
	  	}
	  	else if(whichCol == 2){
	  		colType2 = whichChooseTypeDropDown.options[whichChooseTypeDropDown.selectedIndex].value;
	  	}
	  }

    </script>
</head>




<BODY onload="drawChart();">

<div id="container">
    

<div>
<P>
<b>Spreadsheet name: (coming)</b>
</P>
<P>


<%
		

		String dropDownHtml1 = HtmlUtil.createDropDownForm("test", "setCol1Name(this.blah)", "blah", 
		        			firstRow.getCustomElements().getTags(), 
		        			firstRow.getCustomElements().getTags(), 
		        			"test",
		        			"chooseCol1");
		        			
	   String dropDownHtml2 = HtmlUtil.createDropDownForm("test", "setCol2Name(this.blah)", "blah", 
		        			firstRow.getCustomElements().getTags(), 
		        			firstRow.getCustomElements().getTags(), 
		        			"test",
		        			"chooseCol2");
		        			
	   
		        			
		        			
	  
	   		        			
%> 
	Y-axis column: (labels)
<%	   		        			
	   out.println(dropDownHtml1);
%> 
<P>
<FORM  onChange="colTypeChanged(this.chooseType2, 2)" ID="chooseColType2">
<SELECT NAME="chooseType2">
<OPTION VALUE="boolean">boolean
<OPTION VALUE="number">number
<OPTION VALUE="string">string
<OPTION VALUE="date">date
<OPTION VALUE="datetime">datetime
<OPTION VALUE="timeofday">timeofday
</SELECT>
</FORM>	
<P>
<P>

	X-axis column: (values)
</P>
<%	
	   out.println(dropDownHtml2);
%> 
<P>
<FORM  onChange="colTypeChanged(this.chooseType2, 2)" ID="chooseColType2">
<SELECT NAME="chooseType2">
<OPTION VALUE="boolean">boolean
<OPTION VALUE="number">number
<OPTION VALUE="string">string
<OPTION VALUE="date">date
<OPTION VALUE="datetime">datetime
<OPTION VALUE="timeofday">timeofday
</SELECT>
</FORM>	
<P>

	Filter column: (must be a column of TRUE or FALSE values in the spreadsheet)
<%	
	   Set<String> filterStrings = new HashSet(); 
	   //filterStrings.addAll(firstRow.getCustomElements().getTags()); 
	   filterStrings.add("bah3"); 
	   
	   System.out.println("firstRow: " + firstRow);
	   
	   for (String tag : firstRow.getCustomElements().getTags()) {
			String entryValue = firstRow.getCustomElements().getValue(tag);
			System.out.println("entryValue: " + entryValue); 
			
			if (entryValue != null){
			
				String cleanString = (entryValue.toLowerCase()).trim();  
			    
				if (cleanString.equals("true") || cleanString.equals("false")){
			    	filterStrings.add(tag); 
			    }	    
		    }
	  } // for tag		        		
		        		
		        			
	   String dropDownHtml3 = HtmlUtil.createDropDownForm("test", "setCol3Name(this.blah)", "blah", 
		        			filterStrings, 
		        			filterStrings, 
		        			"test", 
		        			"chooseCol3");

	   out.println(dropDownHtml3); 
   
	   
%>
<input type="button" id="updateColButton" value="Update columns" onClick="reloadWithNewParams();" /> 
	 
	 
	   
</P>

<HR>

<A HREF="javascript:summarize()">See summary</A>

<HR>

<P>
<FORM  onChange="vizChanged(this.chooseViz)" ID="chooseVizType">
<SELECT NAME="chooseViz">
<OPTION VALUE="1">Bar Chart
<OPTION VALUE="2">Column Chart
<OPTION VALUE="3">Line Chart
<OPTION VALUE="4">Pie Chart
</SELECT>
</FORM>


</P>


</div>


<div id="chart_div">
</div>
<div id="map_div">
</div>

</BODY>
</HTML>