
# do the actual capture
filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + user + " - " \
           + (info['stream']).get("channel").get("status") + ".flv"
filename = format_filename(filename)
subprocess.call(shlex.split('./bin/streamlink twitch.tv/' + user + quality,
                            '-o \"' + filename + '\"'))

