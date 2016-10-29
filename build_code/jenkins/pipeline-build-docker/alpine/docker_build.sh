# build base image
cd /home/spoot/MediaKraken_Deployment/build_code/jenkins/pipeline-build-docker/alpine/ComposeMediaKrakenBase
docker build -t mediakraken/mkbase:dev-0.1.12 .

# build slave image
cd /home/spoot/MediaKraken_Deployment/build_code/jenkins/pipeline-build-docker/alpine/ComposeMediaKrakenSlave
docker build -t mediakraken/mkslave:dev-0.1.12 .

# build server
cd /home/spoot/MediaKraken_Deployment/build_code/jenkins/pipeline-build-docker/alpine/ComposeMediaKrakenServer
docker build -t mediakraken/mkserver:dev-0.1.12 .

# build database
cd /home/spoot/MediaKraken_Deployment/build_code/jenkins/pipeline-build-docker/alpine/ComposeMediaKrakenDatabase
docker build -t mediakraken/mkdatabase:dev-0.1.12 .
docker run  -e POSTGRES_PASSWORD=mysecretpassword -p 5433:5432 -d mediakraken/mkdatabase:dev-0.1.12

# build metadata
cd /home/spoot/MediaKraken_Deployment/build_code/jenkins/pipeline-build-docker/alpine/ComposeMediaKrakenServerMetadata
docker build -t mediakraken/mkmetadata:dev-0.1.12 .

# nginx
cd /home/spoot/MediaKraken_Deployment/build_code/jenkins/pipeline-build-docker/alpine/ComposeMediaKrakenNginx
docker build -t mediakraken/mknginx:dev-0.1.12 .

