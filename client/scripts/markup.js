(function()
{
    "use strict";
    
    var markups =
    {
    	player: function (markup)
    	{
    		return $("<span/>").text(markup.name);
    	},
    	
    	room: function (markup)
    	{
    		return $("<span/>").text(markup.title);
    	},
    	
    	realm: function (markup)
    	{
    		return $("<span/>").text(markup.name);
    	},
    	
    	instance: function (markup)
    	{
    		return $("<span/>").text(markup.name);
    	}
    };
    
    W.Markup =
    {
    	ToDOM: function(markup)
    	{
    		if (typeof(markup) == "string")
    			return $("<span/>").text(markup);
    		else if (markup.length)
    		{
    			var s = $("<span/>");
    			$.each(markup,
    				function(_, m)
    				{
    					s.append(W.Markup.ToDOM(m));
    				}
    			);
    			return s;
    		}
    		else
    		{
    			var m = markups[markup.type];
    			if (m)
    				return m(markup);
    			console.log("unknown markup: " + $.toJSON(markup));
    			return "";
    		}
    	}
    };
}
)();
