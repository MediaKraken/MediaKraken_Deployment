<p align="center"><img src="art/K1.png" alt="Media Kraken" height="200px"></p>

<B>What is it?</B>
Yet another media streaming server and client application suite. Also includes media management and remote conrol software to run on a tablet.<BR>
<BR>
This program is still quite alpha.<BR>
<BR>
Please see the WIKI for documentation.<BR>
<BR>
    <h2 style="color:white;">Why does this app exist?</h2>
    <p style="color:white;" class="indent">I've tried many media managers and streamers. They all seemed to lack one thing....one cohesive environment. Plugin's for this and that...some update, some don't. Biggest issue I had was plugins only supporting one patch level and trying to keep everything in sync across my servers and workstations along with 100% linux support. As they say the rest is history and I starting cutting code......</p>
<h2 style="color:white;">Features (in progress):</h2>
<UL style="color:white">
<LI>100% Open Source, no "premium", paid betas, restricted access or other nonsense.
<LI>Native server will run under MacOSX, Linux and Windows via Docker
<LI>Native client support for Android, iOS, MacOSX, Linux and Windows
<LI>"Slave" servers for streaming to balance the load with many clients streaming at once via Docker Swarm
	<ul>
	<li>GPU acceleration supported via CUDA
	</ul>
<li>"Link" servers together so they can display each others media
<LI>Central database implemented via PostgreSQL
<li>Remote control software to run on a touch tablet/phone
<LI>Dedicated OS builds for the following:
<ul>
<LI>Client:
    <UL>
    <li>img file for Raspberry Pi 1/2/3 (Linux based)
    <li>ISO/img for install on dedicated client hardware (Linux based)
    </UL>
<LI>Server: Most server images are simply Alpine Linux with Docker and Docker Compose with the images downloaded for immediate use.
    <UL>
    <li>OVA for VMWare 5.x or 6.x
    <li>OVA for Proxmox VE 5.x
    <li>64-bit ISO/img for install on dedicated server hardware
    </ul>
<li>Offsite Storage Support
</u>
</UL>
</ul>
<h2 style="color:white";>Privacy Policy: This program collects NO data on users.</h2>
<h1 align="center" style="color:white;">Feel like donating for inspiration and pizza?  <a href="http://PayPal.Me/SpootDev">Paypal</a></h1>
