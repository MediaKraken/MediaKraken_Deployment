
# program will scan for blank images....and auto drop sections < 60 seconds
# ffmpeg -ss 213 -i MySourceMovie.m4v -c:v copy -c:a copy testoutput.m4v
# ffmpeg -ss "00:00:00.000" -i "movie.m4v" -to "00:15:18" -c:v copy -c:a copy "result.pt1.m4v"
# ffmpeg -ss "00:22:29.500" -i "movie.m4v" -to "00:18:58" -c:v copy -c:a copy "result.pt2.m4v"
# ffmpeg -ss "00:50:24.500" -i "movie.m4v" -to "00:16:12" -c:v copy -c:a copy "result.pt3.m4v"
# ffmpeg -ss "01:14:48.500" -i "movie.m4v" -to "00:18:44" -c:v copy -c:a copy "result.pt4.m4v"
# ffmpeg -ss "01:41:35.000" -i "movie.m4v" -to "00:18:08" -c:v copy -c:a copy "result.pt5.m4v"

# ffmpeg -i inputfile.mp4 -vf blackframe=d=0.1:pix_th=.1 -f rawvideo -y /dev/null
# ffmpeg -i test.avi -vf blackdetect=d=1:pic_th=0.70:pix_th=0.10 -an -f null -

# this work?
# ffmpeg -i "$1" -vf blackframe -an -f null - 2>&1 | ack "(?<=frame:)[0-9]*(?= )" -oh > blacks.txt
# ffmpeg -i '/home/spoot/nfsmount/TV_Shows_Misc/Wilfred (2007)/s1e4.avi'
# -vf blackframe -an -f null - 2>&1 | ack "(?<=frame:)[0-9]*(?= )" -oh > blacks.txt
# cat blacks.txt | while read a; do
# printf "not(eq(n\,$a))*"
# done
# rm blacks.txt
# ffmpeg -f concat -i ace-files.txt -c copy ace.tvshow

