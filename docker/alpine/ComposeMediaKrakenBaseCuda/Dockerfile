# Start with Alpine base image
FROM alpine:3.8

# download cuda
RUN apk update && apk add --update wget alpine-sdk perl && \
    wget http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_7.5.18_linux.run && \
    chmod +x cuda_*_linux.run && \
    ./cuda_*_linux.run --tar mxvf && \
    ./run_files/cuda-linux64-rel-*.run -noprompt && \
    rm -rf cuda_*_linux.run \
           /run_files \
           InstallUtils.pm \
           cuda-installer.pl \
           uninstall_cuda.pl \
   && apk del wget alpine-sdk perl \
   && rm -rf /var/cache/apk/*

# Add to path
ENV PATH=/usr/local/cuda-7.5/bin:$PATH LD_LIBRARY_PATH=/usr/local/cuda-7.5/lib64:$LD_LIBRARY_PATH

