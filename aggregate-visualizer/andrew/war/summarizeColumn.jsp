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
<title>Summarizing Spreadsheet Column</title>
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
	String sumColName = request.getParameter("summarizeCol"); 
	String filterColName = request.getParameter("filterCol");
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
               	
	URL feedUri = new URL("http://spreadsheets.google.com/feeds/worksheets/"+key+"/private/full");

	WorksheetFeed listFeed = service.getFeed(feedUri, WorksheetFeed.class);
	List<WorksheetEntry> worksheets = listFeed.getEntries();//spreadsheetEntry.getWorksheets();
        	
    WorksheetEntry worksheetEntry = worksheets.get(0);
       	
    URL listFeedUrl = worksheetEntry.getListFeedUrl();
    
    ListQuery query = new ListQuery(listFeedUrl);
    // Only get the filtered stuff
	
	String filterQuery = ""; 
	
	if (filterColName == null){
		filterColName = "bah3"; 
	}
	
	if (!filterColName.equals("bah3")){
		filterQuery = filterColName + " = true"; 
	}
	
	query.setSpreadsheetQuery(filterQuery);
	ListFeed feed = service.query(query, ListFeed.class);
	
	// Now, I have a ListFeed; let's summarize it
    ListEntry firstRow = feed.getEntries().get(0);
	
%>


    <script type="text/javascript">  
      
     	 var data = new google.visualization.DataTable();
     	 var sumData = new google.visualization.DataTable(); 
<%        
		
		
		Map<String, Integer> questionAnswersAndCountsMap = new HashMap<String, Integer>(); 
		
		if (sumColName == null){
			Object[] tags = (feed.getEntries().get(0)).getCustomElements().getTags().toArray(); 
			sumColName = (String)tags[0];
		}
		
		System.out.println("sumColName: " + sumColName); 
		
		if ( !sumColName.equals("bah1")){ // we have a valid colName
		
			// Go through all the rows
			for (ListEntry entry : feed.getEntries()) {
			
				for (String tag : entry.getCustomElements().getTags()) {
				
					
					if (tag.equals(sumColName)){
			        	String val = entry.getCustomElements().getValue(tag);
			        	// If the val (response) is already in the map, increment; 
			        	// Else add it
			        	
			        	System.out.println("val: " + val); 
						if (val != null){
							val = val.replace("'", "*"); 
							System.out.println("clean val: " + val);
						}
			        	
			        	if (questionAnswersAndCountsMap.containsKey(val)){
			        		int count = ((Integer)questionAnswersAndCountsMap.get(val)).intValue(); 
			        		questionAnswersAndCountsMap.put(val, new Integer(count + 1)); 
			        	}
			        	else{
			        		questionAnswersAndCountsMap.put(val, new Integer(1)); 
			        	}	    
			        }
			 	} // for tag
		 	}// For ListEntry/row
		 	
		 	// Now we have the counts, let's dump 'em 
		 	
		  out.println("data.addColumn('string', '"+ sumColName +"');");
		  out.println("data.addColumn('number', 'count');");
		  
		  
		  out.println("data.addRows("+questionAnswersAndCountsMap.keySet().size()+");");
		  
		  int curRow = 0; 
		  
		  for(String answer : questionAnswersAndCountsMap.keySet()){
		  	int val = ((Integer)questionAnswersAndCountsMap.get(answer)).intValue(); 
		  	
		  	out.println("data.setValue("+curRow+", 0, '" + answer + "');");
			out.println("data.setValue("+curRow+", 1, " + val+ ");"); 	
		  	
		  	curRow++;
		  }
		 	
		 	
	    } // If we have valid column name	
		
		 
		 out.println("\n\nvar newBaseUrl = \"" + baseUrl +"\";" );
		 out.println("\n\nvar sumColumnName = \"" + sumColName +"\";" );
		 out.println("var filterColumnName = \"" + filterColName +"\";" );
		 
		 boolean drawChart = true;  
		 
		 out.println("var doDrawChart = "+ drawChart + ";"); 
		 
%>		  

      var curChartViz = 1; 
      var colType1 = 1; 
      var colType2 = 2; 
      
      function drawChart() {
      	  if (doDrawChart)
      	  {
      	  	 
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
      

	  function reloadWithNewParams(){
	     
	  	newUrl = newBaseUrl + "&summarizeCol=" + sumColumnName + "&filterCol="+filterColumnName;
	  	window.location = newUrl; 
	  }
	  
 	  function vizChanged(whichVizDropDown){
	  	curChartViz = whichVizDropDown.options[whichVizDropDown.selectedIndex].value;  
	    drawChart(); 
	  }
	  
	  function setSumColName(dropDown){
        sumColumnName = dropDown.options[dropDown.selectedIndex].value; 
      }
      
      function setFilterColName(dropDown){
      	filterColumnName = dropDown.options[dropDown.selectedIndex].value; 
      }

    </script>
</head>




<BODY onload="drawChart();">

<div id="container">
    

<div>
<P>
<H1>Spreadsheet name: <%= sheetName %></H1>
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
	Column to summarize:
	<P>
	<FORM  onChange="setSumColName(this.blah)" ID="chooseCol1">
	<SELECT NAME="blah">
	
<%	   		        			
	   // Go through the tags/elements
	   
	   // Write out an option tag for each one
	   
	   // If one is the col to be summarized, select it by default 
	   
	   for (String tag : firstRow.getCustomElements().getTags()) {
			String entryValue = firstRow.getCustomElements().getValue(tag);
			
			if (tag.equalsIgnoreCase(sumColName)){
				out.println("<OPTION SELECTED VALUE=\""+tag+"\">"+tag ); 
			}
			else{
				out.println("<OPTION VALUE=\""+tag+"\">"+tag ); 
			}
	  } // for tag
%> 
	</SELECT>
	</FORM>
<P>

	Filter column: (must be a column of TRUE or FALSE values in the spreadsheet)
<%	
	   Set<String> filterStrings = new HashSet(); 
	   
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
		        		
%>

	<FORM  onChange="setFilterColName(this.blah)" ID="filterCol">
	<SELECT NAME="blah">
	
<%	   		        			
	   
	   for (String tag : filterStrings) {
			
			if (tag.equalsIgnoreCase(filterColName)){
				out.println("<OPTION SELECTED VALUE=\""+tag+"\">"+tag ); 
			}
			else{
				out.println("<OPTION VALUE=\""+tag+"\">"+tag ); 
			}
	  } // for tag
	  
	  // Add the null filter choice
	  if (filterColName.equalsIgnoreCase("bah3")){
	  	out.println("<OPTION SELECTED VALUE=\"bah3\">no filter" ); 
	  }
	  else{
	    out.println("<OPTION VALUE=\"bah3\">no filter" );
	  }
%> 
    
	</SELECT>
	</FORM>

<input type="button" id="updateColButton" value="Update chart" onClick="reloadWithNewParams();" /> 
	 
	 
	   
</P>

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