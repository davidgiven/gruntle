(function()
{
    "use strict";

	var USERNAME_COOKIE = "com.cowlark.thickishstring.username";
	var PASSWORD_COOKIE = "com.cowlark.thickishstring.password";

    var attempt_login_cb = function()
    {
        var username = $("#username").prop("value");
        var password = $("#password").prop("value");
        var autologin = $("#autologin").prop("value");

        if (autologin)
        {
            /* Save credentials for the next time. */

            $.cookie(USERNAME_COOKIE, username, { expires: 60 });
            $.cookie(PASSWORD_COOKIE, password, { expires: 60 });
		}

    	W.Effects.HidePage($("#page"))
    		.promise()
    		.done(
    			function()
    			{
                    W.Socket.Send(
                    	{
                    		command: "connect",
                    		username: username,
                    		password: password
                    	}
                    );
    			}
    		);
    };
    
    W.LoginPage =
    {
        Show: function ()
        {
            /* If we have a login cookie, don't bother showing the
             * dialogue. */

			var saved_username = $.cookie(USERNAME_COOKIE);
			var saved_password = $.cookie(PASSWORD_COOKIE);
			if (saved_username && saved_password)
			{
				W.Socket.Send(
					{
						command: "connect",
						username: saved_username,
						password: saved_password
					}
				);
			}

			/* Otherwise show the dialogue. */

            $("#page").load("login.html",
            	function ()
            	{
            		W.StandardMarkup();
            		
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
                            	W.Effects.HidePage($("#page"))
                            		.promise()
                            		.done(W.RegisterPage.Show);
                            }
                        );
                        
                    $("#guest").button()
                        .click(
                            function (event)
                            {
                            	W.Effects.HidePage($("#page"))
                            		.promise()
                            		.done(
                            			function()
                            			{
                            				W.Socket.Send(
                            					{
                            						command: "guest"
                            					}
                            				);
                            			}
                            		);
                            }
                        );
                        
                    $("#login").button()
                        .click(attempt_login_cb);
                 
                    $("#logindialogue").show();
                    $("#page").hide();
                    W.Effects.ShowPage($("#page"));
            	}
            );
        },
        
        AuthenticationFailedEvent: function(message)
        {
            W.LoginPage.RemoveLoginCookie();

        	W.Dialogue(
        		{
        			message: "Authentication failed. (Either you are using an "+
        				"incorrect password, or that user does not exist, "+
        				"or both.)",
            		positive: "OK",
            		positivecb: W.LoginPage.Show
        		}
        	);
        },

        RemoveLoginCookie: function()
        {
            $.removeCookie(USERNAME_COOKIE);
            $.removeCookie(PASSWORD_COOKIE);
        }
    };
}
)();
