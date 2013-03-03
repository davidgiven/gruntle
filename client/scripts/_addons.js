(function()
{
    "use strict";

    $.fn.singleLineEditor =
    	function (commit_cb)
    	{
    		var self = this;
    		
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
}
)();
