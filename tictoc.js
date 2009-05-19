google.load("feeds", "1");

function handletictocspans()
{
	$("head").append('<link rel="stylesheet" type="text/css" href="http://libx.lib.vt.edu/services/jquery-plugins/cluetip/jquery.cluetip.css" />');
	
	var tictocspans = $("span[class*='tictoc-']");
	tictocspans.each(function () {
        var issn = "";
        var jtitle = "";
		var title = this.getAttribute ('title');
		var match = title.match(/ISSN:(\d{4}\-?\d{3}[xX\d]):(.*)/);
		if (match) {
			issn = match[1];
			jtitle = match[2];
		} else if (title == "ISSN:millennium.issnandtitle") {
			issn = $("tr > td.bibInfoLabel:contains('ISSN') + td.bibInfoData").text().replace(/^\s+|\s+$/g, "");
			jtitle = $("tr > td.bibInfoLabel:contains('Title')").filter(function() {
				return $(this).text() == 'Title';
			}).eq(0).next("td.bibInfoData").text().replace(/^\s+|\s+$/g, "");
		}
		
		if (issn == "")
			return;
		
		var titleclause = "?title=" + encodeURIComponent(jtitle);		
		var $span = $(this);
		
		function whendatareceived (data) {
			if (data.records.length == 0) 
				return;
				
			var tictocresult = data.records[0];
			if ($span.hasClass ("tictoc-append-title")) {
				$span.append(tictocresult.title);
			}
			
			if ($span.hasClass ("tictoc-link")) {
				$span.wrap('<a href="' + tictocresult.rssfeed + '"></a>');
				$span.attr('title', '');
				//place in own class
				$('head').append('<link rel="alternate" type="application/rss+xml" title="Table of Contents for ' 
				+ tictocresult.title + '" href="' + tictocresult.rssfeed + '"/>');
			}
			
			if ($span.hasClass ("tictoc-preview")) {
				$span.attr("rel", "<div></div>");
				$span.cluetip({width: '500px', sticky: true, closePosition: 'title', arrows: true, local: true,
					onShow: function ($cluetip, $cluetipInner) {
						//$cluetipInner is a jquery that has selected the inner content of the cluetip as it is shown
						// for CSS, see
						// http://code.google.com/apis/ajaxfeeds/documentation/reference.html#FeedControl
						var feedControl = new google.feeds.FeedControl();
						feedControl.setNumEntries(5);
						feedControl.addFeed(tictocresult.rssfeed, tictocresult.title);
						feedControl.draw($cluetipInner[0]);
					}
				});
			}
			
			$span.parents().andSelf().show();
		}
		
		$.getJSON("http://tictoclookup.appspot.com/" + issn + titleclause + "&jsoncallback=?", whendatareceived);
	});
}

google.setOnLoadCallback(handletictocspans, true);

// remove 1x1 image placed by syndetics.com
$(window).load(function () {
	$("img[src*='syndetics.com']").filter(function () {
		return $(this).height() == 1 && $(this).width() == 1;
	}).remove();
});
