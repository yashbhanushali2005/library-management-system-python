pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {

        stage('GitHub Integration') {
            steps {
                echo 'Code fetched from GitHub Repository'
            }
        }

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

        stage('Push to DockerHub') {
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
    }

    post {
        success {
            echo 'Pipeline Completed Successfully'
        }

        failure {
            echo 'Pipeline Failed'
        }
    }
}
