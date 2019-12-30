# Blender Single Image Network Render


### Introduction

As my Final Work for school I made blender single image network render as I found other implementations lacking. I have been able to run the addon on both Windows and Linux (as I do not own a Mac or Hackintosh I have not been able to test it for that platform), using 2 HP Zbooks running Ubuntu 18.04 I was able to consistently cut the render time in half each time for the BMW and Classroom benchmarks.

### Prerequisites

In order to use the sender addon you first need to get the PIL python module installed for blender, there is also [a reciever addon](https://github.com/chrisvannooten/blendernetworkimagereciever) that is used simply for machines that serve as renderers.

First check in the Python console of Blender (NOT YOUR OS!), what version of Python is being used.
After you have your Python version download [the PIL module from pypi](https://pypi.org/project/Pillow/#files) corresponding to your Python version and OS e.g.(Pillow=6.2.1-cp37-cp37m-win\_amd64.whl for Windows 10 64bit with Blender 2.81a).
After that make a folder (call it whatever you like) and make 3 folders within that folder called 'addons','modules' and 'startup'.
Extract the Pillow.whl file in the 'modules' folder using a program like winrar.
Then in Blender open Preferences go to File path (lowest tab on the left) and set the Scripts folder to the folder where the 'modules' folder resides, open and close Blender just to be sure it takes effect.
After all that you can install the addon which should be the files in this repository in a zip.

If you want to simply use the machine as rendermachine download [the Network Render Receiver](https://github.com/chrisvannooten/blendernetworkimagereciever) instead.
It doesn't need the PIL library in order to function.

### Usage
First save your blender file, the addon can't send something if it isn't saved.

In the properties window under the Render tab you will now find the a new submenu called 'Server Panel'.
In the server panel you have the option to:
* Local Render: here you can set whether or not the device will help rendering itself
* Add new server: here you add a server machine by typing their Ipv4 server

The auto calculate percentage currently just divides up any remaining percentage so if you have 2 devices with auto calculate on it will give each 50% or if you have 1 device with 30% the other will be assigned 70% if it has auto calculate percentage on.

After you have set your servers up you simply press the 'Render File' button, I have noticed on Windows the program says not responding but after 3 minutes I still got the BMW benchmark in its entirety.

### Notes

Using Wifi is disadviced especially for larger projects as it will affect total render time. 
Currently you also have to pack all your external data into the blend file (which you do by going File->ExternalData->Automatically pack into .blend file)


### Todo

* Add better error handling
* Keep track of render time (PIL is fast, meaning the total render time usually comes down to the longest + data transfer time)
