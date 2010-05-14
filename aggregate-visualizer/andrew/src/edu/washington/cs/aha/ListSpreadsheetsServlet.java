package edu.washington.cs.aha;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.security.GeneralSecurityException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.jdo.PersistenceManager;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.gdata.client.docs.DocsService;
import com.google.gdata.client.http.AuthSubUtil;
import com.google.gdata.client.spreadsheet.SpreadsheetService;
import com.google.gdata.data.docs.DocumentListFeed;
import com.google.gdata.data.spreadsheet.SpreadsheetEntry;
import com.google.gdata.data.spreadsheet.SpreadsheetFeed;
import com.google.gdata.util.AuthenticationException;
import com.google.gdata.util.ServiceException;

public class ListSpreadsheetsServlet extends ServletUtilBase {
	public void doGet(HttpServletRequest request, HttpServletResponse resp)
	throws IOException {
		// verify Log in? 

		resp.getWriter().print("<HTML>\n<HEAD>\n<TITLE>Spreadsheet List</TITLE>\n" +
				"<link rel=\"stylesheet\" href=\"styles.css\" type=\"text/css\" />" +
				"</HEAD>\n\n<BODY>");


		// If not authenticated/logged in, write out a URL to do the log-in. 
		// If authenticated, there will be a token in the link? 
		// When authenticating, have this be the "next" URL

		// Otherwise, show a list of spreadsheets to choose from (?) 
		// Have the URLs for each spreadsheet include the user auth token 

		resp.getWriter().print("you're logged in. That's great!");
		
		resp.getWriter().print("<P>Sometimes I have connection time out issues. Try reloading. It might be worse if you have many spreadsheets.</P>");

		String docSessionToken = getParameter(request, ServletConsts.DOC_AUTH);
		String spreadSessionToken = getParameter(request, ServletConsts.SPREAD_AUTH);


		// Create a new Spreadsheet service
		SpreadsheetService myService = new SpreadsheetService("UWCSE-ahaTestApp-1");
		DocsService docListService = new DocsService("");

		docListService.setAuthSubToken(docSessionToken, null);
		URL feedUri = new URL("http://docs.google.com/feeds/default/private/full/");

		try{
			DocumentListFeed listFeed = docListService.getFeed(feedUri, DocumentListFeed.class);
		}
		catch(Exception e){
			resp.getWriter().print("<P>DocumentListFeed error: couldn't get docListFeed</P>");

		}

		try{
			myService.setAuthSubToken(spreadSessionToken);

			// Get a list of all entries
			URL metafeedUrl = new URL("http://spreadsheets.google.com/feeds/spreadsheets/private/full");
			// System.out.println("Getting Spreadsheet entries...\n");
			SpreadsheetFeed resultFeed = myService.getFeed(metafeedUrl, SpreadsheetFeed.class);
			
			resp.getWriter().print("<UL>\n"); 


			List<SpreadsheetEntry> entries = resultFeed.getEntries();
			for(int i=0; i<entries.size(); i++) {
				SpreadsheetEntry entry = entries.get(i);
				System.out.println("\t" + entry.getTitle().getPlainText());
				resp.getWriter().print("<LI><B>"+entry.getTitle().getPlainText() + "</B>"); 


				Map<String, String> params = new HashMap<String, String>();
				//    params.put(ServletConsts.SPREADSHEET_NAME_PARAM, spreadsheetName);
				//    params.put(ServletConsts.ODK_FORM_KEY, odkFormKey);
				params.put(ServletConsts.DOC_AUTH, docSessionToken);
				params.put(ServletConsts.SPREAD_AUTH, spreadSessionToken);
				params.put("key", entry.getKey());
				params.put("sheetName", entry.getTitle().getPlainText()); 
				
				
				// Do Summary URL
				String summUrl = 
					"http://" +
					HtmlUtil.createLinkWithProperties(getServerURL(request) + "/summarizeColumn.jsp", params);


				String summHtml =
					HtmlUtil.wrapWithHtmlTags(HtmlConsts.P, " "
							+ HtmlUtil.createHref(summUrl, "Go to summary view"));

				// HtmlUtil.createHref("", entry.getTitle().getPlainText()); 
				resp.getWriter().print(summHtml);
				
				params.put("col1", "bah1");
				params.put("col2", "bah2"); 
				params.put("col3", "bah3"); 
				params.put("col1type", "bah1");
				params.put("col2type", "bah2");

				/*     String returnUrl =
	              "http://"
	                  + HtmlUtil.createLinkWithProperties(getServerURL(request) + "/chooseCols", params);
				 */

				String returnUrl = 
					"http://" +
					HtmlUtil.createLinkWithProperties(getServerURL(request) + "/testVizAndSpreadsheet.jsp", params);


				String loginHtml =
					HtmlUtil.wrapWithHtmlTags(HtmlConsts.P, " "
							+ HtmlUtil.createHref(returnUrl, "Show in AhaViz"));

				// HtmlUtil.createHref("", entry.getTitle().getPlainText()); 
				resp.getWriter().print(loginHtml);
				
				String koosUrl = "http://" + 
						HtmlUtil.createLinkWithProperties(getServerURL(request) + "/chooseCols", params);
				String koosHtml = 
						HtmlUtil.wrapWithHtmlTags(HtmlConsts.P, HtmlUtil.createHref(koosUrl, "Go to choose Columns"));
				resp.getWriter().print(koosHtml);
				
				resp.getWriter().print("</LI>\n");



			}



			resp.getWriter().print("<UL>\n"); 

		}
		catch(AuthenticationException e) {
			System.err.println("Authentication exception;");
		}
		catch(MalformedURLException e) {
			e.printStackTrace();
		}
		catch(ServiceException e) {
			System.err.println("Service Exception");
		}
		catch(IOException e) {
			e.printStackTrace();
		}


		resp.getWriter().print("</BODY>");

	}


}

