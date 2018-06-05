<p align="center"><img src="art/K1.png" alt="Media Kraken" height="200px"></p>

<B>What is it?</B>
Yet another media streaming server and client application suite. Also includes media management and remote conrol software to run on a tablet.<BR>
<BR>
This program is still quite alpha.<BR>
<BR>

 <ul style="color:white;">
        <li><b>mkdev - redid internet speed test, improved chromecast playback, fixed Twitch
        playback, much improved search, misc fixes, Lightgallery 1.6.11, Nginx 1.14.0 - Current
        Dev
        branch</b>
        <li><i>castnow - improved Chromecast device discovery, PostgreSQL 10.4, FFMPEG 4.0
        <li>videojs - 6.8 and update other plugins, letter navigation start, alot of misc fixes
        <li>dev - Redis 4.0.9, FFMPEG version bumps, base images on 3.7 Alpine, RabbitMQ 3.7.4, Lightgallery 1.6.9, JQuery 3.3.1, Bootstrap 4.1, Wireshark container
        <li>0.7.11 - PostgreSQL 10.3, ELK cleanup, more Jenkins build, redid how docker compose and "one-off" containers are built/launched
        <li>0.7.10 - pyspeedtest, better automated testing, Jenkins CI, PGAdmin4, PostgreSQL 9.6.7
        <li>0.7.9/elk - Clean up disc read, basic videojs resume, base SoundCloud videojs, base Frame by Frame videojs, background videojs, base chapter videojs, libnfs support, scanning support via Sane, WebOS control, basic Samsung TV control via SOAP, basic pioneer control, basic Discogs support, basic TheSubDB support
        <li>0.7.8 - Base Excel code, Base Xbox Live code, lazy load images, base Soundcloud code, base Instragram code, base BeautifulHue code, ID3 tagging, base OpenSubtitles search, base Twilio support, YT api v3
        <li>0.7.7 - Redis 3.2.11, Nginx 1.13.6, PostgreSQL 9.6.6, different theaters (controller, thin, etc), bad bot blocker, base lms code, base weather code, base translation code
        <li>0.7.6 - Playback in client, control Samsung tv
        <li>0.7.5 - Listview for Kivy media list, parallel queries in PostgreSQL
        <li>0.7.4 - Read DVD/Bluray info, PostgreSQL 9.6.5
        <li>0.7.3 - Tasks instead of cron, Youtube playback, basic Youtube support, alot of search code, base LCD code
        <li>0.7.2 - Mail server, Calibre, base search code, PostgreSQL 9.6.4
        <li>0.7.1 - Better url link support, NVidia Cuda base code, basic control of Marantz equipment over network
        <li>0.7.0 - NGINX SSL Proxy to webserver, code cleanup, pika to metadata programs, ssl key reuse for server and website
        <li>0.6.x - Kivy update, use Twisted line reactor in server and client via Crochet, many metadata view fixes, use json for Twisted messages
        <li>0.5.0 - Fixes
        <li>0.4.x - More pika code and playback of media via Chromecast
        <li>0.3.x - Tons of fixes and network refactor along with Docker swarm and RabbitMQ
        <li>0.2.1 - Lots of metadata fixes
        <li>0.2.0 - Full blown Docker instances
        <li>0.1.13 - Many docker fixes, admin user
        <li>0.1.12 - Docker build
        <li>0.1.11 - TV limiter, autobuild of lxc in Proxmox for distribution builds, more build scripts
        <li>0.1.10 - Finish movie limiter
        <li>0.1.9 - Image proxy begin
        <li>0.1.8 - Complete movie limiter refactor
        <li>0.1.7 - More PEP8 compliance, merge build code
        <li>0.1.6 - Rebranding, thousands of changes for PEP8 compliance, movie api limiter code
        <li>0.1.5 - Refactor movie and tv metadata match, TwitchTV stream playback
        <li>0.1.4 - Begin automated test suite (400+ unit tests), dictcursor, cleanup, basic TwitchTV support
        <li>0.1.3 - Ubuntu 16.04, begin proper limiter for API calls to metadata providers, different thread pool
        <li>0.1.1 - and 0.1.2 Lots of code fixes and cleanup
        <li>0.1.0 - Hundreds of fixes, better logging, sync/conversion support, more metadata providers, db upgrade to Postgresql 9.5
        <li>0.0.9 - Youtube, vimeo and HLS streaming, server linking
        <li>0.0.8 - UNC/SMB scanning support, progress indicators, many fixes, synology and chromecast discovery, hdhomerun basic support, API engine
        <li>0.0.7 - TV metadata
        <li>0.0.6 - Movie metadata, movie matching and sports metadata
        <li>0.0.5 - Fetch and process of metadata
        <li>0.0.3 - Tons of fixes
        <li>0.0.2 - Alot of base code
        <li>0.0.1 - New beginings...</i>
        </ul>

# MediaKraken_Deployment<BR>
git clone https://github.com/MediaKraken/MediaKraken_Deployment<BR>
git submodule update --init --recursive<BR>
git pull --recurse-submodules<BR>
