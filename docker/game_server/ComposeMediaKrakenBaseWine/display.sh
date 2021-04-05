export DISPLAY=:99
Xvfb :99 -screen 0 1000x1000x16 &
xrandr –query
sleep 5
nohup startxfce4 &
sleep 10
xdotool mousemove 493 539 click 1
xrandr –query
winetricks -q msxml4 msxml6 corefonts vcrun2010 vcrun2013 vcrun2017 dotnet46