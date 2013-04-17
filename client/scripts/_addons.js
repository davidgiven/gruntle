(function()
{
    "use strict";

    $.fn.textEditor =
    	function ()
    	{
    		var self = this;
    		
    		
    	};
    	
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
						if (commit_cb)
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
    	function (newtext)
    	{
    		if (newtext)
    		{
    			/* Set */
    			
    			this.empty();
            	var paras = newtext.split("\n");
            	for (var i = 0; i < paras.length; i++)
            		this.append($("<p/>").text(paras[i]));
    		}
    		else
    		{
    			/* Get */
    			
        		var st = [];
        		
        		var c = this.children();
        		if (c.length == 0)
        			return this.text();
        		
        		c.each(
        			function(i, e)
        			{
        				var s = $(e).text().trim();
        				if (s !== "")
        					st.push(s);
        			}
        		);
        		
        		return st.join("\n");
    		}
    	};
    	
	String.prototype.hashCode = function()
	{
	    var hash = 0, i, char;
	    if (this.length == 0)
	    	return hash;
	    for (i = 0; i < this.length; i++)
	    {
	        char = this.charCodeAt(i);
	        hash = ((hash<<5)-hash)+char;
	        hash = hash & hash; // Convert to 32bit integer
	    }
	    return (hash & 0x7fffffff);
	};
}
)();
