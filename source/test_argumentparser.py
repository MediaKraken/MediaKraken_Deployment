import argparse

parser = argparse.ArgumentParser(description='This program build and deploys MediaKraken')
parser.add_argument('-b', '--base', metavar='base', required=False, help='Base images only')
# set build_only variable if entered - ex. ComposeMediaKrakenBaseFFMPEG
parser.add_argument('-i', '--image', metavar='image', required=False, help='Image to build')
parser.add_argument('-r', '--release', metavar='release', required=False, help='Push to DockerHub')
parser.add_argument('-t', '--type', metavar='type', required=True, help='The build type dev/prod')
args = parser.parse_args()

print(args)
