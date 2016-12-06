** Project completed. Pending final review. **


PyHdHomeRun
-----------

The HDHomeRun (HDHR) TV tuner is a neat, standalone tuner-device that 
communicates the video signals to your system over the network. A cheap one 
will have a couple of separate tuners built-in, but the more expensive ones 
will have at least three-tuners and will even accept a cable-card to decrypt 
your service-provider's channels directly (thus bypassing the need for a cable
-box).

HDHomeRun makes the code available for the libraries, but this project wraps 
those with Python to make them far more intuitive to interact with. Obviously, 
any rendering should still be done in C, but there's no rule that we can't 
hook it all together with Python and speed-up development a bit.

I saw a couple of other projects that either directly exposed the dynamic 
libraries through Python or invoked the command. I wanted an intuitive 
interface that interacted with the dynamic libraries without being too coupled 
with them, and encapsulated the entire breadth of typical usage. The 
individual calls should be basic primitives that can plug-in nicely to the 
predefined tuner interface of another DVR or TV application.

The goals of this project were as follows:

> Be able to discover the device(s) on the local network.
> Be able to poll for status.
> Be able to list channels.
> Be able to scan channels.
> For a tuner to be able to set the channel and acquire a lock.
> To be able to instruct a tuner to start sending video back.

All goals have all been completed.


Requirements
------------

> The HDHomeRun library. As my own distribution (Ubuntu) had a version that was 
  too old, you might have to download these from the website: 
  
    http://www.silicondust.com/support/hdhomerun/downloads/linux

  If you have the build-tools installed, all you have to do is "make" from the 
  directory that you extracted the files to. Then, just make sure the library 
  "libhdhomerun.so" is either in the directory of this project, or in the 
  library search-path.

