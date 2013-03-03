(function()
{
    "use strict";

    $.fn.singleLineEditor =
    	function (commit_cb)
    	{
    		var self = this;
    		
    		self.attr("contenteditable", "true");
            self.keydown(
                function (event)
                {
					if (event.which == 13)
					{
						commit_cb(this);
						event.preventDefault();
					}
					else
						self.addClass("urgent");
                }
            );
            return self;
       	};

    $.fn.textWithBreaks =
    	function ()
    	{
    		var st = [];
    		
    		this.children().each(
    			function(i, e)
    			{
    				var s = $(e).text().trim();
    				if (s !== "")
    					st.push(s);
    			}
    		);
    		
    		return st.join("\n");
    	};
}
)();
