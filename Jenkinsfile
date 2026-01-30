pipeline {
    agent any

    options {
        timestamps()
        durabilityHint('PERFORMANCE_OPTIMIZED')
    }

    environment {
        APP_NAME = "library-app"
        IMAGE_NAME = "yashbhanu2005/library-ms:1.0"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Trivy Security Scan') {
            steps {
                bat '''
                docker run --rm ^
                  -v //var/run/docker.sock:/var/run/docker.sock ^
                  aquasec/trivy:latest ^
                  image --severity HIGH,CRITICAL %IMAGE_NAME%
                '''
            }
        }

        stage('Login to DockerHub & Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                    docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    docker push %IMAGE_NAME%
                    '''
                }
            }
        }

        stage('Deploy Application (Docker Monitoring)') {
            steps {
                bat '''
                docker stop %APP_NAME% || exit 0
                docker rm %APP_NAME% || exit 0

                docker run -d ^
                  --restart unless-stopped ^
                  --name %APP_NAME% ^
                  %IMAGE_NAME%

                docker ps | findstr %APP_NAME%
                '''
            }
        }
    }

    post {

        success {
            echo '✅ CI/CD Pipeline completed successfully 🎉'
            echo '📊 Jenkins metrics scraped by Prometheus'
            echo '📈 Visualized in Grafana'
        }

        failure {
            echo '❌ Pipeline failed. Metrics still available in Grafana 🚨'
        }
    }
}
