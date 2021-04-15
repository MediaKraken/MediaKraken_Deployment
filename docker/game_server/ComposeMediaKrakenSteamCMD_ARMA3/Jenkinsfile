def ARMADocker

node ('Docker') {
	stage ('Checkout') {
		checkout scm
	}
	stage ('Build Docker Image') {
		ARMADocker=docker.build 'gameservers/arma3:latest'
	}

	stage ('push to Dockerhub') {
		withDockerRegistry([credentialsId: '611e19af-5b46-435b-9613-57825c983940']) {
			ARMADocker.push 'latest'
		}
	}

	stage ('Start server on gs1.uk.steamlug.org') {
		withCredentials([usernamePassword(credentialsId: '141a5d20-730f-466f-b7b0-4e6118cf2f96', passwordVariable: 'SECRETKEY', usernameVariable: 'ACCESSKEY')]) {
			sh 'wget -q https://releases.rancher.com/compose/v0.12.0/rancher-compose-linux-amd64-v0.12.0.tar.gz'
			sh 'tar xf rancher-compose-linux-amd64-v0.12.0.tar.gz'
			sh 'rancher-compose-v0.12.0/rancher-compose --access-key $ACCESSKEY --secret-key $SECRETKEY --url http://gs1.uk.steamlug.org:8080/v2-beta/projects/1a5/stacks/1st23 -p ARMA3 up --force-upgrade --confirm-upgrade -d'
		}
	}
}
