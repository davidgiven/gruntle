(function()
{
    "use strict";
    
    W.Socket =
    {
    	Connect: function(uri)
    	{
        	/* This is the input buffer from the server. It's an array of
        	 * bytes expressed as a string. Blame Javascript. */
        	
        	var buffer = "";
        	
        	var check_buffer = function()
        	{
        		for (;;)
        		{
            		/* We only bother to decode the buffer if there's a complete
            		 * line of text in it --- that way we don't need to care
            		 * about fragmented UTF-8. */
            		
        			var eol = buffer.indexOf("\n");
            		if (eol == -1)
            			return;
            		
            		/* Extract the line. */
            		
            		var s = buffer.slice(0, eol-1);
            		
            		/* Now use a rather evil trick to decode it. This decodes
            		 * the UTF-8 and gives us valid Javascript string. See:
            		 * 
            		 * http://ecmanaut.blogspot.ca/2006/07/encoding-decoding-utf8-in-javascript.html
            		 */
            		
            		s = decodeURIComponent(escape(s)).trim();
            		
            		/* Process the message now it's been decoded. This will
            		 * always be one complete line from the server. */
            		
            		if (s.length > 0)
            		{
            			if (s[0] != "{")
            			{
            				/* Whoops --- the server has sent us an out-of-band
            				 * message (which is naughty of it). Fake up a
            				 * message packet to put it in. */
            				
            				W.OnMessageReceived(
            					{
            						event: "outofband",
            						message: s
            					}
            				);
            			}
            			else
            			{
            				/* Otherwise it must be a JSON message. */
            				
            				W.OnMessageReceived($.evalJSON(s));
            			}
            		}
            		
            		/* Remove the bit of the buffer that we just processed
            		 * and go round again. */
            		
            		buffer = buffer.slice(eol+1, buffer.length);
        		}
        	};
        	
        	W.WS = new WebSocket(uri, "binary");
        	W.WS.binaryType = "arraybuffer";
        
        	W.WS.onopen = function()
        	{
        		W.OnSocketOpened();
        	};

        	W.WS.onclose = function()
        	{
        		W.OnSocketClosed();
        	};
        	
        	W.WS.onmessage = function(event)
            {
        		var incoming = new Uint8Array(event.data);
        		
        		/* Append all the data in the packet to the buffer. Note
        		 * whether we saw a newline. */
        		
        		var newline = false;
        		for (var i=0; i<incoming.length; i++)
        		{
        			var b = incoming[i];
        			if (b === 10)
        				newline = true;
        			buffer += String.fromCharCode(b);
        		}

        		/* If we saw a newline, then there might be a complete line
        		 * of input from the server. */
        		
        		if (newline)
        			check_buffer();
            };
            
            W.WS.onerror = function(event)
            {
            	W.OnSocketError(event);
            };
    	},
    	
    	Send: function(msg)
    	{
    		var json = $.toJSON(msg);
    		console.log(">message ", msg.command, ": ", json);
    		W.WS.send(json + "\r\n");
    	},
    	
    	Disconnect: function()
    	{
    		W.WS.close();
    	}
    };
}
)();
