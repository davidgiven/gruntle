(function()
{
    "use strict";
    
	var defaultduration = 300;
	var defaulteasing = "easeInOutQuad";
	
	var fadeIn = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);
		
		return s.fadeIn(
    			{
    				duration: defaultduration,
    				easing: defaulteasing
    			}
    		);
	};

	var fadeInSlow = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);
		
		return s.fadeIn(
    			{
    				duration: defaultduration*2,
    				easing: defaulteasing
    			}
    		);
	};

	var fadeOut = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);
		
		return s.fadeOut(
    			{
    				duration: defaultduration,
    				easing: defaulteasing
    			}
    		);
	};

	var fadeOutAndRemove = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);
		
		return s.fadeOut(
    			{
    				duration: defaultduration,
    				easing: defaulteasing,
    				complete:
    					function()
    					{
    						s.remove();
    					}
    			}
    		);
	};

	var slideUp = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);

		return s.slideUp(
    			{
    				duration: defaultduration,
    				easing: defaulteasing
    			}
    		);
	};
	
	var slideDown = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);

		return s.slideDown(
    			{
    				duration: defaultduration,
    				easing: defaulteasing
    			}
    		);
	};
	
	var slideDownShow = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);

    	return s.show(
    		{
    			effect: "slide",
    			easing: defaulteasing,
    			duration: defaultduration,
    			direction: "down",
    		}
    	);
	};

	var slideDownHide = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);

    	return s.hide(
    		{
    			effect: "slide",
    			easing: defaulteasing,
    			duration: defaultduration,
    			direction: "down",
    		}
    	);
	};

    W.Effects =
    {
    	DefaultDuration: defaultduration,
    	DefaultEasing: defaulteasing,
    	
    	FadeIn: fadeIn,
    	FadeInSlow: fadeInSlow,
    	FadeOut: fadeOut,
    	
    	ShowPage: fadeInSlow,
    	HidePage: fadeOut,
    	
    	ShowDialogue: fadeIn,
    	HideDialogue: fadeOut,
    	
    	NewText: fadeInSlow,
    	HideText: slideUp,
    	ShowText: slideDown,
    	
    	ShowButton: fadeIn,
    	RemoveButton: fadeOutAndRemove,
    	
    	ShowActions: slideDownShow,
    	HideActions: slideDownHide
    };
}
)();
