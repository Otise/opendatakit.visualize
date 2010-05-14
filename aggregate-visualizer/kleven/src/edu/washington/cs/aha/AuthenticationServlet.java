package edu.washington.cs.aha;

import java.io.IOException;
import java.net.URL;
import java.security.GeneralSecurityException;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;
import com.google.gdata.client.docs.DocsService;
import com.google.gdata.client.http.AuthSubUtil;
import com.google.gdata.client.spreadsheet.SpreadsheetService;
import com.google.gdata.data.PlainTextConstruct;
import com.google.gdata.data.docs.DocumentListEntry;
import com.google.gdata.data.docs.SpreadsheetEntry;
import com.google.gdata.util.AuthenticationException;

public class AuthenticationServlet extends ServletUtilBase {
	

	  private static final String TOKEN_TYPE = "tokenType";

	
	public void doGet(HttpServletRequest req, HttpServletResponse resp)
	throws IOException {
	
		
		/*aha:
		// verify user is logged in
	    UserService userService = UserServiceFactory.getUserService();
	    if (!userService.isUserLoggedIn()) {
	      beginBasicHtmlResponse("Login Required", resp, request, false);
	      String returnUrl = request.getRequestURI() + ServletConsts.BEGIN_PARAM + request.getQueryString();
	      String loginHtml =
	          HtmlUtil.wrapWithHtmlTags(HtmlConsts.P, "Please "
	              + HtmlUtil.createHref(AuthSubUtil.getRequestUrl(returnUrl, 
	      				"", 
	    				false, 
	    				true), "log in"));
	      resp.getWriter().print(loginHtml);
	      finishBasicHtmlResponse(resp);
	      return; 
	    }
		*/
	    
	    // verify user is logged in
	    if (!verifyCredentials(req, resp)) {
	      return;
	    }

	    // get parameter
	 //   String spreadsheetName = getParameter(req, ServletConsts.SPREADSHEET_NAME_PARAM);
	 //   String odkFormKey = getParameter(req, ServletConsts.ODK_FORM_KEY);
	    String docSessionToken = getParameter(req, ServletConsts.DOC_AUTH);
	    String spreadSessionToken = getParameter(req, ServletConsts.SPREAD_AUTH);
	    String esType = getParameter(req, ServletConsts.EXTERNAL_SERVICE_TYPE);
	    String tokenTypeString = getParameter(req, TOKEN_TYPE);

	    Map<String, String> params = new HashMap<String, String>();
	//    params.put(ServletConsts.SPREADSHEET_NAME_PARAM, spreadsheetName);
	//    params.put(ServletConsts.ODK_FORM_KEY, odkFormKey);
	    params.put(ServletConsts.DOC_AUTH, docSessionToken);
	    params.put(ServletConsts.SPREAD_AUTH, spreadSessionToken);
	    params.put(ServletConsts.EXTERNAL_SERVICE_TYPE, esType);

	/*    if (spreadsheetName == null || odkFormKey == null) {
	      resp.sendError(HttpServletResponse.SC_BAD_REQUEST, ErrorConsts.MISSING_FORM_INFO);
	      return;
	    }
*/
	    TokenType tokenType = TokenType.NONE;

	    if (tokenTypeString != null) {
	      tokenType = TokenType.valueOf(tokenTypeString);
	    }


	      if (tokenType.equals(TokenType.DOC)) {
	        try {
	          docSessionToken = verifyGDataAuthorization(req, resp, ServletConsts.DOCS_SCOPE);
	          params.put(ServletConsts.DOC_AUTH, docSessionToken);
	        } catch (Exception e) {
	          return; // verifyGDataAuthroization function formats response
	        } 
	      }
	      if (tokenType.equals(TokenType.SPREAD)) {
	        try {
	          spreadSessionToken = verifyGDataAuthorization(req, resp, ServletConsts.SPREADSHEET_SCOPE);
	          params.put(ServletConsts.SPREAD_AUTH, spreadSessionToken);
	        } catch (Exception e) {
	          return; // verifyGDataAuthroization function formats response
	        } 
	      }

	      // still need to obtain more authorizations
	      if (docSessionToken == null || spreadSessionToken == null) {
	        beginBasicHtmlResponse("Authenticate for spreadsheet", resp, req, true); // header info
	        if (docSessionToken == null) {
	          params.put(TOKEN_TYPE, TokenType.DOC.toString());
	          String authButton =
	              generateAuthButton(ServletConsts.DOCS_SCOPE,
	                  ServletConsts.AUTHORIZE_SPREADSHEET_CREATION, params, req, resp);
	          resp.getWriter().print(authButton);
	        } else {
	          resp.getWriter().print("Completed Doc Authorization <br>");
	        }

	        if (spreadSessionToken == null) {
	          params.put(TOKEN_TYPE, TokenType.SPREAD.toString());
	          String authButton =
	              generateAuthButton(ServletConsts.SPREADSHEET_SCOPE,
	                  ServletConsts.AUTHORIZE_DATA_TRANSFER_BUTTON_TXT, params, req, resp);
	          resp.getWriter().print(authButton);
	        } else {
	          resp.getWriter().print("Completed Spreadsheet Authorization <br>");
	        }

	        finishBasicHtmlResponse(resp);
	        return;
	      }



	      // setup service
	/*      DocsService service =
	          new DocsService(this.getServletContext().getInitParameter("application_name"));
	      service.setAuthSubToken(docSessionToken, null);

	      // create spreadsheet
	      DocumentListEntry createdEntry = new SpreadsheetEntry();
	      createdEntry.setTitle(new PlainTextConstruct(spreadsheetName));

	      DocumentListEntry updatedEntry =
	          service.insert(new URL(ServletConsts.DOC_FEED), createdEntry);

	      // get key
	      String docKey = updatedEntry.getKey();
	      String sheetKey =
	          docKey.substring(docKey.lastIndexOf(ServletConsts.DOCS_PRE_KEY)
	              + ServletConsts.DOCS_PRE_KEY.length());
*/
	      // get form
	 /*     EntityManager em = EMFactory.get().createEntityManager();
	      Key formKey = KeyFactory.stringToKey(odkFormKey);
	      Form form = em.getReference(Form.class, formKey);
*/
	      // create spreadsheet
/*	      GoogleSpreadsheet spreadsheet = new GoogleSpreadsheet(spreadsheetName, sheetKey);
	      spreadsheet.setAuthToken(spreadSessionToken);

	      form.addGoogleSpreadsheet(spreadsheet);
	      em.close();

	      TaskOptions task = TaskOptions.Builder.url("/" + WorksheetServlet.ADDR);
	      task.method(TaskOptions.Method.GET);
	      task.countdownMillis(DELAY);
	      task.param(ServletConsts.SPREADSHEET_NAME_PARAM, spreadsheetName);
	      task.param(ServletConsts.ODK_FORM_KEY, odkFormKey);
	      task.param(ServletConsts.EXTERNAL_SERVICE_TYPE, esType);


	      Queue queue = QueueFactory.getDefaultQueue();
	      try {
	        queue.add(task);
	      } catch (Exception e) {
	        System.out.println("PROBLEM WITH TASK");
	        e.printStackTrace();
	      }

	      // remove docs permission no longer needed
	      try {
	        AuthSubUtil.revokeToken(docSessionToken, null);
	      } catch (GeneralSecurityException e) {
	        // TODO Auto-generated catch block
	        e.printStackTrace();
	      }
	   
	    } catch (AuthenticationException e) {
	      // TODO Auto-generated catch block
	      e.printStackTrace();
	    } catch (ServiceException e) {
	      // TODO Auto-generated catch block
	      e.printStackTrace();
	    }

	    resp.sendRedirect(ServletConsts.WEB_ROOT);
*/
	      
	      String returnUrl =
              "http://"
                  + HtmlUtil.createLinkWithProperties(getServerURL(req) + "/listSpreadsheets", params);
     
	      
	      
	      beginBasicHtmlResponse("auth page", resp, req, true);
	      String loginHtml =
	          HtmlUtil.wrapWithHtmlTags(HtmlConsts.P, "You are logged in. Please continue!  "
	              + HtmlUtil.createHref(returnUrl, "List Spreadsheets"));
	      resp.getWriter().print(loginHtml);
	      
	      finishBasicHtmlResponse(resp);
	      
	      
	      /*
	       * for spreadsheet feeds:
  http://spreadsheets.google.com/feeds/spreadsheets/private/full
for a worksheet list feed:
  http://spreadsheets.google.com/feeds/
for doc feeds (e.g. list of spreadsheets in a named folder):
  http://docs.google.com/feeds/documents/private/full

Concatenate those into a single string with a space between them
and then pass it to GenerateAuthSubURL() to get an AuthSub multi-
token
that can be used to access all of the feeds.

Regards, 
	       */
	}
	private enum TokenType {
	    NONE, DOC, SPREAD;
	  }	

}

