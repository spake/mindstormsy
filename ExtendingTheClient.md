If you don't own an NXT robot and want to modify the client to use a different robotics platform, then you can use MindstormsyAPI to create your own client.
MindstormsyAPI provides an easy way to connect to a Mindstormsy-Robot instance on the Google App Engine and retrieve the action string for a certain Wave ID.

You can look over mindstormsy-client/mindstormsy-client.py for an example on how to use the API, or check out this sample code:

```
import mindstormyapi

client = mindstormsyapi.MindstormsyClient() # Create a client object with the default robot (mindstormsy-robot.appspot.com)
waveId = raw_input("Wave ID: ") # Get the Wave ID from the user
timeout = 1

while 1:
  action = client.poll(waveId, timeout) # Polls the client and returns the action (or an error)
  if action == mindstormsyapi.SERVER_ERROR: # Server-side error
    print "Poll failed (server error)"
  elif action == mindstormsyapi.UNKNOWN_ERROR: # Client-side error
    print "Poll failed (client error)"
    # If you are required to display a more detailed error description to the user,
    # then check client.lastError, and compare it to the constants found in mindstormsyapi.py
  else:
    print "Current action: %s" % action
```

The API can be found at mindstormsy-client/mindstormsyapi.py. If you're having trouble, look in the file itself: it's not too long, and there's lots of helpful comments and docstrings to help you get acquainted with it!