(function()
{
    "use strict";

    var attempt_login_cb = function()
    {
        var username = $("#username").prop("value");
        var password = $("#password").prop("value");

        W.Socket.Send(
        	{
        		command: "connect",
        		username: username,
        		password: password
        	}
        );
    };
    
    W.LoginPage =
    {
        Show: function ()
        {
            $("#page").load("login.html",
            	function ()
            	{
                    $("#username").keydown(
                        function (event)
                        {
                            if (event.keyCode === 13)
        	                    $("#password").focus();
                        }
                    );
                    
                    $("#password").keydown(
                        function (event)
                        {
                            if (event.keyCode === 13)
                                attempt_login_cb();
                        }
                    );
                            
                    $("#register").button()
                        .click(
                            function (event)
                            {
                            	W.RegisterPage.Show();
                            }
                        );
                        
                    $("#login").button()
                        .click(attempt_login_cb);
            	}
            );
        }
    };
}
)();
