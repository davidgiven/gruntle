(function()
{
	"use strict";

	var fail = function (message)
	{
		S.Dialogue(message);
	};
	
    var attempt_registration_cb = function()
    {
    	var username = $("#username").prop("value");
    	var empirename = $("#empirename").prop("value");
        var email = $("#email").prop("value");
        var password = $("#password").prop("value");
        var password2 = $("#password2").prop("value");
        
        if (!username)
        	return fail("You must specify a valid username.");
        if (!email)
        	return fail("You must specify a valid email address.");
        if (!password)
        	return fail("An empty password —-- really?");
        if (password !== password2)
        	return fail("Your passwords don't match.");
        
        W.Socket.Send(
        	{
        		command: "createplayer",
        		username: username,
        		password: password
        	}
        );
    };
    
    W.RegisterPage =
    {
        Show: function ()
        {
            $("#page").load("register.html",
            	function ()
            	{
            		W.StandardMarkup();
            		
                    $("#username").keydown(
                        function (event)
                        {
                            if (event.keyCode === 13)
        	                    $("#email").focus();
                        }
                    );

                    $("#email").keydown(
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
                                $("#password2").focus();
                        }
                    );
                            
                    $("#password2").keydown(
                        function (event)
                        {
                            if (event.keyCode === 13)
                            {
                            	W.Effects.HidePage($("#page"))
                            		.promise()
                            		.done(attempt_registration_cb);
                            }
                        }
                    );
                            
                    $("#cancel").button()
                        .click(
                            function (event)
                            {
                            	W.Effects.HidePage($("#page"))
                            		.promise()
                            		.done(W.LoginPage.Show);
                            }
                        );
                        
                    $("#register").button()
                        .click(attempt_registration_cb);
                    
                    $("#registerdialogue").show();
                    $("#page").hide();
                    W.Effects.ShowPage($("#page"));
            	}
            );
        }
    };
}
)();
