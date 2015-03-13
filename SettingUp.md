# Prerequisites #

Requirements for NXT robot control:
  * Python (tested with 2.6), download from http://www.python.org
  * PySerial (tested with v2.5), download from http://pyserial.sourceforge.net
  * A PC with either an internal or external Bluetooth adapter (tested on Mac OS X 10.6)
  * A LEGO Mindstorms NXT robot
  * A Google Wave account (Sandbox is fine)

Requirements for the live video feed (optional):
  * A smartphone with video streaming software installed
  * An account on a video streaming website such as Ustream (http://ustream.com)
  * A rubber band to hold the smartphone to your NXT robot

# Setting Up (Mac) #

  1. Turn on your NXT robot and enable Bluetooth (check the LEGO manual for info on how to do this).
  1. On your Mac, go to the Bluetooth menu in the top right corner of the screen and turn on Bluetooth.
  1. In the Bluetooth menu, choose 'Set Up Bluetooth Device' and follow the instructions to pair your computer with the robot (hint: the robot is usually called NXT).
  1. Head into System Preferences and click on Bluetooth. Highlight your robot in the sidebar, click on the little gear at the bottom of the list, and choose 'Edit Serial Ports'. Wait for the port name to load, and note down what's written next to 'Path'. Mine was /dev/tty.NXT-DevB, and yours will probably be similar.
  1. Click here (https://wave.google.com/wave/#restored:wave:googlewave.com!w%252BP48dCEWuB) and install the Mindstormsy Google Wave extension into your Wave account. Then make a new Wave, edit the root blip and click on the new 'M+' button on your toolbar.
  1. Click on 'Get Wave ID', and note down the result. Chances are it'll look something like 'googlewave.com!w+abc123'.
  1. Check out the contents of the mindstormsy-client folder from the source tree (click on the Source tab at the top of this page).
  1. Open up a Terminal window and cd into the mindstormsy-client folder that you downloaded.
  1. Type in: `chmod 755 mindstormsy-client.py`
  1. Followed by: `./mindstormsy-client.py --waveId=WAVEID --serialPort=PORT` where WAVEID is the ID from step 6, and PORT is the port from step 4.
  1. Hallelujah, you've started the client!...at least, it should have started.
  1. Now go back into Wave, invite all your friends to control the NXT robot, and edit the blip. You can add and remove buttons that correspond to actions. Clicking on these buttons will then send the actions to the NXT robot.
  1. If you sign up to a service such as Ustream, you can copy the video embed code into the gadget as well. Check out their website (http://ustream.com) for more information on retrieving the code.