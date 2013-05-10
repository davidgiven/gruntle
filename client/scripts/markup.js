(function()
{
    "use strict";

    var markups =
    {
    	player: function (o, markup)
    	{
   			var s = $("<span/>").text(markup.name);
    		s.css('color', W.Markup.PlayerColour(markup.name));
    		s.appendTo(o.accumulator);
    	},
    	
    	room: function (o, markup)
    	{
    		$("<span/>").text(markup.title).appendTo(o.accumulator);
    	},
    	
    	realm: function (o, markup)
    	{
    		$("<span/>").text(markup.name).appendTo(o.accumulator);
    	},
    	
    	instance: function (o, markup)
    	{
    		$("<span/>").text(markup.name).appendTo(o.accumulator);
    	},

    	group: function (o, markup)
    	{
			$.each(markup.values,
				function(_, m)
				{
					append(o, m);
				}
			);
    	},

    	action: function (o, markup)
    	{
			var a = makemarkup(markup.markup, "<a href='#'/>", "<span/>");
       		a.click(
       		    function()
       		    {
       		        W.GamePage.PerformActionConsequence(markup.markup,
						markup.id);
					return false;
       		    }
       		);
			a.appendTo(o.accumulator);
    	},

    	error: function (o, markup)
    	{
    	    newline(o, "<div class='realmerror'/>");

    	    o.accumulator.addClass("realmerror");
    	    W.Markup.ToParagraphs(markup.message).appendTo(o.accumulator);
        	var bq = $("<blockquote/>")
        	$.each(markup.details,
        		function (_, s)
        		{
        			$("<div/>").text(s).appendTo(bq);
        		}
        	);
        	bq.appendTo(o.accumulator);

        	newline(o);
    	}
    };

	var newline = function(o, e)
	{
		if (!e)
			e = o.elementtype;

		if (o.accumulator.length == 0)
		{
			o.accumulator.replaceWith($(e));
		}
		else
		{
			o.accumulator = $(e);
			o.accumulator.appendTo(o.root);
		}
	}

    var append = function(o, markup)
    {
		if (typeof(markup) == "string")
		{
			var ss = [];
			$.each(markup.split(/\n[ \t]*\n/),
				function(_, m)
				{
					ss.push($("<span/>").text(m));
				}
			);

			for (var i=0; i<(ss.length-1); i++)
			{
				ss[i].appendTo(o.accumulator);
				newline(o);
			}
			ss[ss.length-1].appendTo(o.accumulator);
		}
		else if (markup.length)
		{
			$.each(markup,
				function(_, m)
				{
					append(o, m);
				}
			);
		}
		else
		{
			var m = markups[markup.type];
			if (m)
				m(o, markup);
			else
				console.log("unknown markup: " + $.toJSON(markup));
		}
    };

	var makemarkup = function(markup, r, s)
	{
		var o = {
			root: $(r),
			elementtype: s,
			accumulator: $(s)
		};

		o.accumulator.appendTo(o.root);
		append(o, markup);
		jsprettify.prettifyHtml(o.root[0]);
		return o.root;
	};

    W.Markup =
    {
    	ToSpan: function(markup)
    	{
    	    return makemarkup(markup, "<span/>", "<span/>");
    	},

    	ToParagraphs: function(markup)
    	{
    	    return makemarkup(markup, "<div/>", "<p/>");
    	},

    	PlayerColour: function(playername)
    	{
   			var c = playername.hashCode() % 360;
			return "hsl("+c+", 50%, 20%)";
    	}
    };
}
)();
