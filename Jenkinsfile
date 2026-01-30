pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = 'dockerhub-creds'
        IMAGE_NAME = 'yashbhanu2005/library-ms'
        IMAGE_TAG = '1.0'
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
            }
        }

        stage('Trivy Security Scan') {
            steps {
                bat '''
                docker run --rm ^
                  -v //var/run/docker.sock:/var/run/docker.sock ^
                  aquasec/trivy:latest ^
                  image --severity HIGH,CRITICAL %IMAGE_NAME%:%IMAGE_TAG%
                '''
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    '''
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                bat "docker push %IMAGE_NAME%:%IMAGE_TAG%"
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed & pushed to DockerHub 🎉'
        }
        failure {
            echo 'Pipeline failed 🚨'
        }
    }
}
