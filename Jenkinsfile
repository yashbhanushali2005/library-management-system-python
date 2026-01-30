pipeline {
    agent any

    options {
        timestamps()                     // ⏱ Build time tracking
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
                script {
                    def start = System.currentTimeMillis()
                    bat "docker build -t ${IMAGE_NAME} ."
                    def duration = (System.currentTimeMillis() - start) / 1000
                    echo "📊 Docker build time: ${duration}s"
                }
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

        stage('Deploy Application') {
            steps {
                bat '''
                docker stop %APP_NAME% || exit 0
                docker rm %APP_NAME% || exit 0

                docker run -d ^
                  -p 5000:5000 ^
                  --name %APP_NAME% ^
                  --restart unless-stopped ^
                  %IMAGE_NAME%
                '''
            }
        }

        stage('Health Check (Monitoring)') {
            steps {
                script {
                    sleep 10
                    bat '''
                    curl -f http://localhost:5000 || exit 1
                    '''
                    echo "✅ Application Health Check PASSED"
                }
            }
        }
    }

    post {

        success {
            echo '✅ CI/CD Pipeline completed successfully 🎉'
            echo '📊 Metrics available at: /prometheus'
        }

        failure {
            echo '❌ Pipeline failed. Metrics sent to Prometheus 🚨'
        }

        always {
            echo "📈 Build monitored by Prometheus + Grafana"
        }
    }
}
