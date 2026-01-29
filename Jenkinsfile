pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies & Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t library-ms:1.0 .'
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                trivy image --severity HIGH,CRITICAL \
                --exit-code 1 library-ms:1.0
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully 🎉'
        }
        failure {
            echo 'Pipeline failed due to security or test issues 🚨'
        }
    }
}
