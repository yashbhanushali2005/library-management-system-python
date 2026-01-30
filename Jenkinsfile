pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t yashbhanu2005/library-ms:1.0 .'
            }
        }

        stage('Trivy Security Scan') {
            steps {
                bat '''
                docker run --rm ^
                  -v //var/run/docker.sock:/var/run/docker.sock ^
                  aquasec/trivy:latest ^
                  image --severity HIGH,CRITICAL yashbhanu2005/library-ms:1.0
                '''
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                    docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    docker push yashbhanu2005/library-ms:1.0
                    '''
                }
            }
        }

        stage('Deploy Application') {
            steps {
                bat '''
                docker stop library-app || exit 0
                docker rm library-app || exit 0

                docker run -d ^
                  -p 5000:5000 ^
                  --name library-app ^
                  yashbhanu2005/library-ms:1.0
                '''
            }
        }

        // 🔥 GRAFANA STAGE (THIS GIVES ✔️)
        stage('Grafana Monitoring') {
            steps {
                bat '''
                docker start grafana || docker run -d ^
                  --name grafana ^
                  -p 3000:3000 ^
                  grafana/grafana

                echo Checking Grafana Health...
                curl http://localhost:3000/api/health
                '''
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD + Monitoring pipeline completed successfully'
        }
        failure {
            echo '❌ Pipeline failed'
        }
    }
}
