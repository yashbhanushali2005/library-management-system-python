pipeline {
    agent any

   stage('Verify Python') {
    steps {
        bat '''
        where python
        python --version
        pip --version
        '''
    }
}
    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Unit Testing') {
            steps {
                bat 'pytest'
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

        stage('Login to DockerHub & Push Image') {
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
            echo '✅ CI/CD Pipeline completed successfully 🎉'
        }
        failure {
            echo '❌ Pipeline failed. Check logs 🚨'
        }
    }
}
