(function()
{
	"use strict";

	var update_game_page = function()
	{
	};
	
    W.GamePage =
    {
        Show: function ()
        {
            $("#page").load("game.html",
            	function ()
            	{
            		update_game_page();
            	}
            );
        }
    };
}
)();
