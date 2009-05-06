google.load("jquery", "1.3.2");
google.load("feeds", "1");

function handletictoc()
{
	$("head").append('<link rel="stylesheet" type="text/css" href="/screens/jquery.cluetip.css" />');
	var tooltip = true; //if WebBridge is disabled, display a tooltip 
	var tictoclabel = "Table of Contents";
	//Test if WebBridge div id=tictoc exists
	var tictoc = $("#tictoc");
	if (tictoc.length == 0) {
		var issn = $("tr > td.bibInfoLabel:contains('ISSN') + td.bibInfoData").text().replace(/^\s+|\s+$/g, "");

		var jtitle = $("tr > td.bibInfoLabel:contains('Title')").filter(function() {
  			return $(this).text() == 'Title';
		}).eq(0).next("td.bibInfoData").text().replace(/^\s+|\s+$/g, "");

	} else {
		var issn = tictoc.attr("issn");
		var jtitle = tictoc.attr("jtitle");
		var tooltip = tictoc.attr("tooltip") == "true";
	}
	
	var titleclause = "?title=" + encodeURIComponent(jtitle);
	
	function whendatareceived(data) {
		if (data.records.length == 0) 
        	return;
		
		if (tictoc.length == 0) { //WebBridge disabled
			$("tr > td.bibInfoLabel:contains('ISSN')").parent()
			.after('<tr><td class="bibInfoLabel">' + tictoclabel 
			 + '</td><td class="bibInfoData"><a id="tictocrssdata" title="' + tictoclabel + ' for ' + data.records[0].title 
		 	 + '" href="' + data.records[0].rssfeed + '">'  
		 	 + data.records[0].title 
		 	 + '&nbsp;<img src="http://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Feed-icon.svg/16px-Feed-icon.svg.png"/></a></td></tr>');
			tictoc = $('#tictocrssdata');
		} else {
			tictoc.append('<a title="' + tictoclabel + ' for ' + data.records[0].title 
		 	 + '" href="' + data.records[0].rssfeed + '">' + tictoclabel + ' for ' 
		 	 + data.records[0].title 
		 	 + '&nbsp;<img src="http://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Feed-icon.svg/16px-Feed-icon.svg.png"/></a><br />');
		}
		
		if (tooltip) {
			tictoc.attr("rel", "<div></div>");
			tictoc.cluetip({sticky: true, closePosition: 'title', arrows: true,
				onShow: function ($cluetip, $cluetipInner) {
					//$cluetipInner is a jquery that has selected the inner content of the cluetip as it is shown
					// for CSS, see
					// http://code.google.com/apis/ajaxfeeds/documentation/reference.html#FeedControl
					feedControl = new google.feeds.FeedControl();
					feedControl.setNumEntries(5);
					feedControl.addFeed(data.records[0].rssfeed, data.records[0].title);
					feedControl.draw($cluetipInner[0]);
				}
			});
		}
		
		$('head').append('<link rel="alternate" type="application/rss+xml" title="Table of Content for ' 
		 + data.records[0].title + '" href="' + data.records[0].rssfeed + '"/>');
		
	}
    
	if (issn != "") {
		$.getJSON("http://tictoclookup.appspot.com/" + issn + titleclause + "&jsoncallback=?", whendatareceived);
	}
}

google.setOnLoadCallback(handletictoc);