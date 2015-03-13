Mindstormsy is a Google Wave extension that allows multiple users to collaboratively control a LEGO Mindstorms NXT robot from within a Wave. In addition, a video stream from a camera attached to the robot can be displayed.

The frontend to the extension is the gadget. Through the gadget, users can control the NXT robot and watch the live video feed from the camera.
When the blip containing the gadget is edited, the user is presented with a form. Using this form, they can pick a state for each of the three motors (forward, reverse or off/disabled), give it a name, and add it to the bottom of the gadget as a button.
Whenever one of these custom buttons is clicked, it updates the gadget's shared state with the actions that were defined when it was made.

The Wave robot listens for these state changes. Whenever it reads a new set of motor states, it stores them in a database under the gadget's Wave ID, and makes them accessible from a URL.

The Mindstormsy client runs on one of the users' PCs, and it continuously polls the Wave robot's URL for new motor states. When it discovers a change, it compiles a message using LEGO's NXT protocol and sends it to the robot, which turns on or off the appropriate motors.

If one of the users decides to mount a smartphone running an application such as Ustream or Qik on their NXT robot, the gadget can display a live video feed from the device. Signing up to and setting up these services is left to the user. Once they have set up, they can copy the video feed embed code from their service's web site and paste it into a text box in the gadget, which will embed it and present it to all members of the Wave.