cd ~/ffmpeg_sources
# Download and unzip the NVIDIA Video Codec SDK from https://developer.nvidia.com/nvidia-video-codec-sdk
wget https://developer.nvidia.com/video-sdk-601
unzip nvidia_video_sdk_6.0.1.zip
# Copy the headers files from the SDK so FFmpeg can find them
sudo cp nvidia_video_sdk_6.0.1/Samples/common/inc/*.h /usr/local/include/

cd ~/ffmpeg_sources
https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda_8.0.61_375.26_linux-run
sh cuda_8.0.61_375.26_linux.run

cd ~/ffmpeg_sources
http://us.download.nvidia.com/XFree86/Linux-x86_64/381.22/NVIDIA-Linux-x86_64-381.22.run
sh NVIDIA-Linux-x86_64-381.22.run
